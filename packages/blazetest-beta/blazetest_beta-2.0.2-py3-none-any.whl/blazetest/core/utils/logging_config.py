import enum
import logging
import os
import uuid

import click
import logging_loki

from blazetest.core.config import LOKI_URL, CWD


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        level = record.levelname
        msg = record.msg
        if level == "DEBUG":
            msg = click.style(msg, fg="blue")
        elif level == "INFO":
            msg = click.style(msg, bold=True)
        elif level == "WARNING":
            msg = click.style(msg, fg="yellow")
        elif level == "ERROR":
            msg = click.style(msg, fg="red", bold=True)
        elif level == "CRITICAL":
            msg = click.style(msg, bg="red", fg="white")
        return f"* {msg}"


def setup_logging(
    debug: bool = False,
    stdout_enabled: bool = True,
    loki_api_key: str = None,
    session_uuid: str = uuid.uuid4(),
):
    """
    Sets up basic logging.
    If stdout_enabled, stdout is shown to the user. Otherwise, saved to the file.
    If loki_api_key is provided, logs are sent to Loki.
    """
    level = logging.DEBUG if debug else logging.INFO

    handlers = []
    # TODO: debug not working well with Loki (possible reason: too many requests)
    if loki_api_key:
        logging_loki.emitter.LokiEmitter.level_tag = "level"
        handler = logging_loki.LokiHandler(
            url=LOKI_URL.format(loki_api_key=loki_api_key),
            tags={"service": "blazetest", "session_id": session_uuid},
            version="1",
        )
        handlers.append(handler)

    if stdout_enabled:
        colored_handler = logging.StreamHandler()
        colored_handler.setFormatter(ColoredFormatter())
        handlers.append(colored_handler)
    else:
        handlers.append(
            logging.FileHandler(filename=os.path.join(CWD, "blazetest.log"))
        )

    logging.basicConfig(
        format="%(message)s",
        level=level,
        handlers=handlers,
    )


class ColoredOutput(enum.Enum):
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
