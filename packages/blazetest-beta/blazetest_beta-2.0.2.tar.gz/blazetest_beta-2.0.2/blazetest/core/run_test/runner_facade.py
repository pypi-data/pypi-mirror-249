from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import logging
import time
from itertools import repeat
from typing import List, Optional

from blazetest.core.config import MAX_LAMBDA_WORKERS
from blazetest.core.project_config.project_config import BlazetestConfig
from blazetest.core.lambda_.invocation import Invocation
from blazetest.core.run_test.pytest_collect import collect_tests
from blazetest.core.run_test.result_model import (
    TestSessionResult,
    InvocationResult,
    JUnitXMLReport,
    ReportMergeResult,
    TestSessionResultManager,
)
from blazetest.core.utils.exceptions import (
    ReportNotAvailable,
    ReportNotUploaded,
    NoTestsToRun,
    ReportNotMerged,
)
from blazetest.core.utils.logging_config import ColoredOutput
from blazetest.core.utils.report_merger import ReportMerger
from blazetest.core.utils.utils import (
    remove_junit_report_path,
    FILTER_ALL,
    FILTER_FAILED,
    FILTER_FLAKY,
)

logger = logging.getLogger(__name__)


class TestRunner:
    """
    Class for running tests using Lambda functions.
    This class is responsible for collecting the test items,
    creating the report paths, and invoking the Lambda functions.

    Attributes:
        config (BlazetestConfig): Configuration for running the tests on AWS Lambda.
        lambda_function (Lambda):  Object responsible for interacting with AWS Lambda.

    Methods:
        run_tests(): Collects the test items, creates the report paths,
            and invokes the Lambda functions.
    """

    # Lambda function name, which will be invoked to run tests
    function_name: str = None

    # S3 bucket name, where the reports should be saved
    s3_bucket: str = None

    # Retry results from each retry attempt
    retry_test_results: List[InvocationResult] = []

    # (needed for rerun) Manager of the test results that is used to get the function name from the previous run
    tests_result_manager: TestSessionResultManager = None

    # List of test node IDs to be run
    node_ids: List[str] = []

    # Needed for aligning the log output
    longest_node_id_length: int = 0

    def __init__(
        self,
        config: BlazetestConfig,
        uuid: str,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
    ):
        """
        Initializes the class with the given config and creates a new Lambda Invocation and Report Merger objects.
        After, it collects tests and if nothing found, raises NoTestsToRun exception.

        :param config: Configuration for running the tests on AWS Lambda.
        :param uuid: Blazetest session UUID.
        :param test_session: TestSessionResult object from the previous run (used only for rerun).
        :param tests_filter: Filter for the tests to be rerun (used only for rerun). Can be: all | failed.
        """
        self.config = config
        self.uuid = uuid

        resource_prefix = self.config.cloud.aws.get_resource_name(uuid=self.uuid)

        self.lambda_function = Invocation(
            region=self.config.cloud.aws.region,
            resource_prefix=resource_prefix,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.report_merger = ReportMerger(
            region=self.config.cloud.aws.region,
            resource_prefix=resource_prefix,
            config=config,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.timestamp = self.__get_timestamp_now()

    def collect_tests(
        self, test_session: TestSessionResult = None, test_filter: str = FILTER_ALL
    ):
        if test_filter == FILTER_ALL:
            self.node_ids = self.get_collected_tests()
        elif test_filter == FILTER_FAILED:
            self.node_ids = test_session.failed_tests_ids
        elif test_filter == FILTER_FLAKY:
            self.node_ids = test_session.flaky_tests_ids

        if self.node_ids:
            logger.info(f"Found {len(self.node_ids)} tests to run")
        else:
            raise NoTestsToRun("Ending session as there are no tests to run")

        self.longest_node_id_length = max(len(node_id) for node_id in self.node_ids)

    def run_tests(
        self,
        flaky_test_retry_enabled: bool = True,
        rerun: bool = False,
    ) -> Optional[TestSessionResult]:
        """
        Creates the report paths, and invokes the Lambda functions in parallel.
        """
        self.set_function_name(rerun=rerun)

        logger.info(
            f"Lambda function: {self.function_name}, " f"S3 bucket: {self.s3_bucket}"
        )
        logger.info("Invoking tests and running in parallel..")

        invocation_result: InvocationResult = self.__run_in_parallel(
            node_ids=self.node_ids
        )

        reports = invocation_result.junit_xml_reports_paths

        if invocation_result.failed_tests_count > 0:
            self.retry(
                flaky_test_retry_enabled=flaky_test_retry_enabled,
                failed_tests=invocation_result.failed_tests_node_ids,
            )

        for retry_invocation_result in self.retry_test_results:
            reports += retry_invocation_result.junit_xml_reports_paths

        report_merge_result = self.__merge_reports(reports=reports)

        return TestSessionResult(
            uuid=self.uuid,
            lambda_function_name=self.function_name,
            tests_count=len(self.node_ids),
            tests_passed=report_merge_result.passed,
            failed_tests_count=invocation_result.failed_tests_count,
            failed_tests_ids=report_merge_result.failed_ids,
            flaky_tests_count=report_merge_result.flaky,
            flaky_tests_ids=report_merge_result.flaky_ids,
            flake_detected=self.report_merger.flake_detected,
            pytest_duration=invocation_result.pytest_duration,
            s3_bucket=self.s3_bucket,
            start_timestamp=self.timestamp,
            end_timestamp=self.__get_timestamp_now(),
            junit_report_path=report_merge_result.final_report_path,
            flake_report_path=report_merge_result.flake_report_path
            if self.report_merger.flake_detected
            else None,
            config=self.config,
        )

    def get_collected_tests(self):
        return collect_tests(pytest_args=self.config.framework.pytest.collection_args)

    def retry(
        self,
        flaky_test_retry_enabled: bool,
        failed_tests: List[str],
    ):
        if flaky_test_retry_enabled and failed_tests:
            logger.info(
                f"Retrying running {len(failed_tests)} failed tests "
                f"{self.config.general.flaky.failure_retry_attempts} times"
            )
            # saves the result of each retry in self.retry_test_results
            self.__retry_failed_tests(failed_tests=failed_tests)

    def __retry_failed_tests(self, failed_tests: List[str], retry_num: int = 0):
        if retry_num >= self.config.general.flaky.failure_retry_attempts:
            return

        retry_test_results = self.__run_in_parallel(
            node_ids=failed_tests,
            retry=True,
        )
        self.retry_test_results.append(retry_test_results)

        logger.info(
            f"Retry #{retry_num + 1}, failed: {retry_test_results.failed_tests_count} "
            f"out of {retry_test_results.passed_tests_count + retry_test_results.failed_tests_count}"
        )

        if (
            retry_test_results.failed_tests_count == 0
            and self.config.general.flaky.exit_on_flake_detection is True
        ):
            logger.info(
                f"All failed tests passed on retry attempt: {retry_num + 1}. Stopping retrying."
            )
            return

        self.__retry_failed_tests(
            failed_tests=(
                retry_test_results.failed_tests_node_ids
                if self.config.general.flaky.exit_on_flake_detection is True
                else failed_tests
            ),
            retry_num=retry_num + 1,
        )

    def __run_in_parallel(self, node_ids: List[str], retry: bool = False):
        start_time = time.time()

        print(
            f"* Observing {len(node_ids)} tests completion status "
            f"{ColoredOutput.GREEN.value}...{ColoredOutput.RESET.value}"
        )
        # TODO: is 1000 appropriate value for workers for threads? Move to async?
        with ThreadPoolExecutor(max_workers=MAX_LAMBDA_WORKERS) as executor:
            results = list(executor.map(self.invoke_lambda, node_ids, repeat(retry)))

        return InvocationResult.parse(results=results, start_time=start_time)

    def invoke_lambda(self, node_id: str, retry: bool = False):
        print(f"* [{node_id}] ... Running")

        report_path = self.__get_pytest_xml_report_path(node_id=node_id)
        pytest_args = remove_junit_report_path(
            self.config.framework.pytest.execution_args
        )

        invocation_result = self.lambda_function.invoke(
            function_name=self.function_name,
            session_uuid=self.uuid,
            node_id=node_id,
            pytest_args=pytest_args,
            report_path=report_path,
            timestamp=self.timestamp,
            retry=retry,
        )

        if invocation_result["test_result"]:
            print(
                f"* [{node_id:{self.longest_node_id_length}}] ... Finished "
                f"{ColoredOutput.GREEN.value}[passed]{ColoredOutput.RESET.value}"
            )
        else:
            print(
                f"* [{node_id:{self.longest_node_id_length}}] ... Finished "
                f"{ColoredOutput.RED.value}[failed]{ColoredOutput.RESET.value}"
            )

        return node_id, invocation_result

    def set_function_name(self, rerun: bool = False):
        if not rerun:
            self.function_name = (
                self.lambda_function.get_created_lambda_function_details()
            )
            return

        test_session = self.tests_result_manager.get_test_session_by_uuid(
            uuid=self.uuid,
        )

        if test_session is None:
            logger.error(f"No test session with the given UUID found: {self.uuid}")
            return None

        self.function_name = test_session.lambda_function_name
        self.s3_bucket = test_session.s3_bucket

    def __merge_reports(self, reports: List[JUnitXMLReport]) -> ReportMergeResult:
        """
        Merges the reports saved to s3 bucket using junitparser and saves the final result in the s3 bucket.

        :param reports: list of reports to be merged

        Returns the path to the merged report.
        """
        self.report_merger.set_s3_bucket_name(s3_bucket_name=self.s3_bucket)

        try:
            report_merge_result: ReportMergeResult = self.report_merger.merge_reports(
                reports=reports,
                timestamp=self.timestamp,
            )
        except (ReportNotAvailable, ReportNotUploaded) as e:
            raise ReportNotMerged(
                f"Error merging reports: {str(e)}. Try rerunning the session."
            )

        logger.info(
            f"Report merged and saved to s3://{self.s3_bucket}/{report_merge_result.final_report_path}"
        )
        return report_merge_result

    def set_s3_bucket_name(self, s3_bucket_name: str):
        self.s3_bucket = s3_bucket_name

    def set_tests_result_manager(self, tests_result_manager: TestSessionResultManager):
        self.tests_result_manager = tests_result_manager

    REPLACE_SYMBOLS = ["::", ".", "/"]
    REPLACE_TO = "-"
    TMP_REPORT_FOLDER = "/tmp/junitxml/{}.xml"
    FOLDER_NAME_TIMESTAMP = "%Y-%m-%d_%H-%M-%S"

    def __get_timestamp_now(self):
        return datetime.now().strftime(self.FOLDER_NAME_TIMESTAMP)

    def __get_pytest_xml_report_path(self, node_id: str) -> str:
        for symbol in self.REPLACE_SYMBOLS:
            node_id = node_id.replace(symbol, self.REPLACE_TO)

        return self.TMP_REPORT_FOLDER.format(node_id)
