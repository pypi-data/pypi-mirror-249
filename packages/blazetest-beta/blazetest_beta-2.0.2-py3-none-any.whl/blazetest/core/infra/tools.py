from abc import ABC, abstractmethod
import logging
from pulumi import automation as auto
from pulumi.automation import LocalWorkspaceOptions, ProjectBackend, ProjectSettings

from blazetest.core.config import CWD, LOKI_HOST, LOKI_USER, DOCKER_FILE_PATH
from blazetest.core.deployment.aws import AWSWorkflow

logger = logging.getLogger(__name__)


class InfraSetupTool(ABC):
    def __init__(
        self,
        aws_region: str,
        resource_prefix: str,
        s3_bucket_name: str,
        ecr_repository_prefix: str,
        lambda_function_timeout: int,
        lambda_function_memory_size: int,
        loki_api_key: str,
        tags: dict,
        debug: bool,
    ):
        self.aws_region = aws_region
        self.resource_prefix = resource_prefix
        self.s3_bucket_name = s3_bucket_name
        self.ecr_repository_prefix = ecr_repository_prefix
        self.lambda_function_timeout = lambda_function_timeout
        self.lambda_function_memory_size = lambda_function_memory_size
        self.loki_api_key = loki_api_key
        self.tags = tags
        self.debug = debug

    @abstractmethod
    def deploy(self) -> None:
        pass


def log_pulumi_event(event: str):
    logger.info(event)


class PulumiInfraSetup(InfraSetupTool):
    """
    Uses Pulumi (https://www.pulumi.com/docs/) Automation API to build and deploy artifacts to the cloud.
    """

    PROJECT_NAME = "blazetest"
    PROJECT_BACKEND_URL = "file:\\/\\/~"
    PROJECT_RUNTIME = "python"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def deploy(self) -> None:
        # TODO: User should pass env variable himself
        env_vars = {}

        workflow = AWSWorkflow(
            project_path=CWD,
            docker_file_path=DOCKER_FILE_PATH,
            resource_prefix=self.resource_prefix,
            s3_bucket_name=self.s3_bucket_name,
            ecr_repository_prefix=self.ecr_repository_prefix,
            lambda_function_timeout=self.lambda_function_timeout,
            lambda_function_memory_size=self.lambda_function_memory_size,
            loki_host=LOKI_HOST,
            loki_user=LOKI_USER,
            loki_api_key=self.loki_api_key,
            env_vars=env_vars,
            tags=self.tags,
        )

        stack = auto.create_stack(
            stack_name=self.resource_prefix,
            project_name="blazetest",
            program=workflow.deploy,
            opts=self.get_project_settings(),
        )

        logger.info("Installing plugins")

        # TODO: updated automatically to the stable version
        stack.workspace.install_plugin("aws", "v5.42.0")
        stack.workspace.install_plugin("docker", "v4.3.1")

        stack.set_config("aws:region", auto.ConfigValue(value=self.aws_region))
        stack.refresh(on_output=log_pulumi_event, show_secrets=False)

        logger.info("Deploying..")
        workflow_result = stack.up(  # noqa
            show_secrets=False, on_output=log_pulumi_event, debug=self.debug
        )

        logger.info(
            "Deploying has finished.",
        )

    def get_project_settings(self):
        return LocalWorkspaceOptions(
            project_settings=ProjectSettings(
                name=self.PROJECT_NAME,
                backend=ProjectBackend(url=self.PROJECT_BACKEND_URL),
                runtime=self.PROJECT_RUNTIME,
            ),
        )
