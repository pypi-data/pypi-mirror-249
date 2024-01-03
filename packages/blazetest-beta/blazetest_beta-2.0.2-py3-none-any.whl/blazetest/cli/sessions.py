import click

from blazetest.cli.base import cli
from blazetest.core.project_config.project_config import ProjectConfiguration
from blazetest.core.run_test.result_model import TestSessionResultManager
from blazetest.core.utils.s3_manager import S3Manager
from blazetest.core.utils.utils import print_table

SESSIONS_TABLE_COLUMNS = [
    "UUID",
    "RERUN UUID",
    "STACK",
    "EXECUTED AT",
    "PASSED TESTS",
    "TAGS",
]


@cli.command()
@click.option(
    "-t",
    "--tags",
    help="Option to filter the sessions by tags. If not specified, all results are shown.",
)
@click.option(
    "-i",
    "--include",
    default="all",
    type=click.Choice(["all", "runs", "reruns"]),
    help="Which type of runs to include in the output of the history of sessions. Can be: all, runs, reruns. "
    "Default is all",
)
@click.option(
    "-config",
    "--config-path",
    help="Configuration path to the TOML file for the CLI. "
    "If not specified -> searches the project's root folder for the file blazetest.toml. "
    "If not found -> raises an error.",
)
def sessions(tags: str = None, include: str = "all", config_path: str = None):
    """
    Shows the sessions created by Blazetest CLI.
    """
    config = ProjectConfiguration.from_toml_file(config_path)
    table = [SESSIONS_TABLE_COLUMNS]

    s3_manager = S3Manager(aws_config=config.cloud.aws)
    _ = s3_manager.find_s3_bucket()

    manager = TestSessionResultManager(
        config=config,
        s3_manager=s3_manager,
    )

    results = manager.get_test_session_results(tags=tags, include=include)

    for result in results:
        table.append(result.get_tabular_data())

    print_table(table)
