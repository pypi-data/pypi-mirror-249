import dataclasses
from typing import List, Dict, Optional

from blazetest.core.project_config.validators import (
    ValidationBase,
    ecr_repository_name_is_valid,
    resource_prefix_is_valid,
    s3_bucket_name_is_valid,
    lambda_function_memory_size_is_valid,
    lambda_function_timeout_is_valid,
    junit_results_file_link_is_valid,
)


@dataclasses.dataclass
class LicenceConfig(ValidationBase):
    license_key: Optional[str] = None
    license_file: Optional[str] = None


@dataclasses.dataclass
class FlakeDetectionConfig(ValidationBase):
    failure_retry_attempts: int = 0
    fail_on_flake: bool = True
    remove_flakes: bool = False
    exit_on_flake_detection: bool = True


@dataclasses.dataclass
class GeneralConfig(ValidationBase):
    junit_results_file_link: str = "private"

    license: LicenceConfig = dataclasses.field(default_factory=lambda: LicenceConfig())
    flaky: FlakeDetectionConfig = dataclasses.field(
        default_factory=lambda: FlakeDetectionConfig()
    )

    def get_validators(self) -> Dict:
        return {
            "junit_results_file_link": junit_results_file_link_is_valid,
        }


@dataclasses.dataclass
class AWSConfig(ValidationBase):
    region: str
    resource_prefix: str = "blazetest-stack"
    s3_bucket_prefix: str = "blazetest-s3"
    ecr_repository_prefix: str = "blazetest-repo"

    lambda_function_memory_size: int = 4096
    lambda_function_timeout: int = 900

    tags: dict = dataclasses.field(default_factory=lambda: {})

    def get_resource_name(self, uuid: str):
        return f"{self.resource_prefix}-{uuid}"

    def get_ecr_repository_prefix(self, uuid: str):
        return f"{self.ecr_repository_prefix}-{uuid}"

    def get_validators(self) -> Dict:
        return {
            "ecr_repository_prefix": ecr_repository_name_is_valid,
            "resource_prefix": resource_prefix_is_valid,
            "s3_bucket_prefix": s3_bucket_name_is_valid,
            "lambda_function_memory_size": lambda_function_memory_size_is_valid,
            "lambda_function_timeout": lambda_function_timeout_is_valid,
        }


@dataclasses.dataclass
class AzureConfig(ValidationBase):
    ...


@dataclasses.dataclass
class GCPConfig(ValidationBase):
    ...


@dataclasses.dataclass
class CloudConfig(ValidationBase):
    aws: AWSConfig
    azure: AzureConfig = dataclasses.field(default_factory=lambda: AzureConfig())
    gcp: GCPConfig = dataclasses.field(default_factory=lambda: GCPConfig())


@dataclasses.dataclass
class ChromeConfig(ValidationBase):
    version: str = "latest"


@dataclasses.dataclass
class FirefoxConfig(ValidationBase):
    version: str = "latest"


@dataclasses.dataclass
class EdgeConfig(ValidationBase):
    version: str = "latest"


@dataclasses.dataclass
class BrowserConfig(ValidationBase):
    """
    The list of supported browsers within blazetest docker image can be found at https://blazetest.io/browsers
    """

    firefox: FirefoxConfig = dataclasses.field(default_factory=lambda: FirefoxConfig())
    edge: EdgeConfig = dataclasses.field(default_factory=lambda: EdgeConfig())
    chrome: ChromeConfig = dataclasses.field(default_factory=lambda: ChromeConfig())


@dataclasses.dataclass
class PytestConfig(ValidationBase):
    collection_args: List[str] = dataclasses.field(default_factory=lambda: [])
    execution_args: List[str] = dataclasses.field(default_factory=lambda: [])


@dataclasses.dataclass
class JUnitConfig(ValidationBase):
    ...


@dataclasses.dataclass
class TestingConfig(ValidationBase):
    ...


@dataclasses.dataclass
class FrameworkConfig(ValidationBase):
    pytest: PytestConfig
    junit: JUnitConfig = dataclasses.field(default_factory=lambda: JUnitConfig())
    testing: TestingConfig = dataclasses.field(default_factory=lambda: TestingConfig())


@dataclasses.dataclass
class BlazetestConfig(ValidationBase):
    general: GeneralConfig
    cloud: CloudConfig
    framework: FrameworkConfig
    browser: BrowserConfig = dataclasses.field(default_factory=lambda: BrowserConfig())
