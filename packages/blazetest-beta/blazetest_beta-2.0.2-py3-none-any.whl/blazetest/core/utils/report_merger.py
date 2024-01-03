import logging
import os
from collections import defaultdict
from typing import List, Dict
from xml.dom.minidom import parseString

import boto3
import junitparser
from junitparser import JUnitXml, TestSuite
from xml.etree import ElementTree

from blazetest.core.config import CWD
from blazetest.core.project_config.model import BlazetestConfig
from blazetest.core.run_test.result_model import JUnitXMLReport, ReportMergeResult
from blazetest.core.utils.logging_config import ColoredOutput
from blazetest.core.utils.exceptions import ReportNotAvailable, ReportNotUploaded

logger = logging.getLogger(__name__)


class ReportMerger:
    """
    Merges reports from S3 Bucket into one file and saves back to the bucket.
    """

    FILE_ENCODING = "utf-8"

    flake_detected: bool = False

    FINAL_REPORT_FILEPATH = (
        "{timestamp}/target/merged/test-session-{resource_prefix}.xml"
    )
    FLAKE_REPORT_FILEPATH = (
        "{timestamp}/target/flake/test-session-{resource_prefix}.xml"
    )

    def __init__(
        self,
        resource_prefix: str,
        region: str,
        s3_bucket_name: str = None,
        config: BlazetestConfig = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
    ):
        self.s3_client = boto3.client(
            "s3",
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.s3_bucket_name = s3_bucket_name
        self.resource_prefix = resource_prefix
        self.config = config

    def set_s3_bucket_name(self, s3_bucket_name: str) -> None:
        self.s3_bucket_name = s3_bucket_name

    def merge_reports(
        self, reports: List[JUnitXMLReport], timestamp: str
    ) -> ReportMergeResult:
        print(
            f"\n* Downloading {len(reports)} test reports "
            f"{ColoredOutput.GREEN.value}...{ColoredOutput.RESET.value} ",
            end="",
        )
        tests_results = self.get_test_results_by_node_id(reports)
        print(f"{ColoredOutput.GREEN.value}Done{ColoredOutput.RESET.value}")

        print(
            f"* Merging test reports into single JUnitXML test report "
            f"{ColoredOutput.GREEN.value}...{ColoredOutput.RESET.value} ",
            end="",
        )
        merge_result = self.get_final_reports(tests_results)
        print(f"{ColoredOutput.GREEN.value}Done{ColoredOutput.RESET.value}")

        final_report_filepath = self.FINAL_REPORT_FILEPATH.format(
            timestamp=timestamp, resource_prefix=self.resource_prefix
        )
        flake_report_filepath = self.FLAKE_REPORT_FILEPATH.format(
            timestamp=timestamp, resource_prefix=self.resource_prefix
        )

        reports = [
            (merge_result["final_report"], final_report_filepath),
            (merge_result["flake_report"], flake_report_filepath),
        ]

        print(
            f"* Uploading merged JUnitXML test report to S3 bucket "
            f"{ColoredOutput.GREEN.value}...{ColoredOutput.RESET.value} ",
            end="",
        )
        for report, report_path in reports:
            self.__upload_report(
                body=self.formatted_xml_string(report),
                path=report_path,
            )
            with open(os.path.join(CWD, report_path.replace("/", "-")), "w") as f:
                f.write(self.formatted_xml_string(report))

        print(f"{ColoredOutput.GREEN.value}Done{ColoredOutput.RESET.value}\n")

        return ReportMergeResult(
            final_report_path=final_report_filepath,
            flake_report_path=flake_report_filepath,
            passed=merge_result["passed"],
            flaky=merge_result["flaky"],
            failed=merge_result["failed"],
            passed_ids=merge_result["passed_ids"],
            flaky_ids=merge_result["flaky_ids"],
            failed_ids=merge_result["failed_ids"],
        )

    def get_test_results_by_node_id(
        self, reports: List[JUnitXMLReport]
    ) -> Dict[str, dict]:
        tests_results = defaultdict(lambda: defaultdict(list))
        for report in reports:
            report_data = self.__download_report(report.report_path)
            junit_report = junitparser.JUnitXml.fromstring(report_data)

            if junit_report.failures or junit_report.errors:
                tests_results[report.test_node_id]["failed"].append(junit_report)
            else:
                tests_results[report.test_node_id]["passed"].append(junit_report)

        return tests_results

    @staticmethod
    def formatted_xml_string(junit_xml: JUnitXml) -> str:
        xml_str = junit_xml.tostring()
        root = ElementTree.fromstring(xml_str)
        rough_string = ElementTree.tostring(root, encoding="utf-8")
        re_parsed = parseString(rough_string)
        return re_parsed.toprettyxml(indent="  ")

    def get_final_reports(self, tests_results: Dict[str, dict]) -> Dict:
        final_report = junitparser.JUnitXml()
        flake_report = junitparser.JUnitXml()

        passed, flaky, failed = 0, 0, 0
        passed_ids, flaky_ids, failed_ids = [], [], []

        for node_id in tests_results:
            test_result = tests_results[node_id]

            if len(test_result["failed"]) == 0:
                final_report += test_result["passed"][0]
                passed += 1
                passed_ids.append(node_id)
                continue

            elif len(test_result["passed"]) > 0:
                report = self.get_test_suite_with_flake_property(
                    test_result=test_result
                )

                flake_report += report

                if self.config.general.flaky.remove_flakes is False:
                    final_report += report
                    flaky += 1
                    flaky_ids.append(node_id)
                    failed_ids.append(node_id)
                else:
                    failed += 1
                    failed_ids.append(node_id)

                self.flake_detected = True

            else:
                final_report += test_result["failed"][0]
                failed += 1
                failed_ids.append(node_id)

        return {
            "final_report": final_report,
            "flake_report": flake_report,
            "passed": passed,
            "passed_ids": passed_ids,
            "flaky": flaky,
            "flaky_ids": flaky_ids,
            "failed": failed,
            "failed_ids": failed_ids,
        }

    @staticmethod
    def get_test_suite_with_flake_property(test_result: dict):
        test_suites: JUnitXml = test_result["passed"][0]
        for test_suite in test_suites.iterchildren(TestSuite):
            test_suite.add_property("flake", True)
            tests_count = len(test_result["passed"]) + len(test_result["failed"])
            test_suite.add_property(
                "flake_rate", f"{len(test_result['passed'])}/{tests_count}"
            )
        return test_suites

    def __download_report(self, report_path: str) -> str:
        try:
            response = self.s3_client.get_object(
                Bucket=self.s3_bucket_name, Key=report_path
            )
            report_data = response["Body"].read().decode(self.FILE_ENCODING)
            return report_data
        except Exception as e:
            raise ReportNotAvailable(
                f"Error downloading report {report_path}: {str(e)}"
            )

    def __upload_report(self, body: str, path: str) -> None:
        try:
            self.s3_client.put_object(Body=body, Bucket=self.s3_bucket_name, Key=path)
        except Exception as e:
            raise ReportNotUploaded(f"Error uploading report {path} to S3: {str(e)}")
