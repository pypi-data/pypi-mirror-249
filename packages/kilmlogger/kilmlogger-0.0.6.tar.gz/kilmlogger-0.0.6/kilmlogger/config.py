import logging

import structlog

from structlog.dev import (
    Column,
    KeyValueColumnFormatter,
    BRIGHT,
    DIM,
    CYAN,
    RESET_ALL,
    RED,
    YELLOW,
    GREEN,
    RED_BACK,
)

from kilmlogger.constants import (
    TIME_FORMAT,
    DEFAULT_FILE_LOG,
    REPLACE_KEY_FOR_TIMESTAMP,
    REPLACE_KEY_FOR_EVENT,
    TIME_FIELD_NAME,
    MESSAGE_FIELD_NAME,
    LEVEL_FIELD_NAME,
    CORRELATION_FIELD_NAME,
)
from kilmlogger.utils import add_correlation
from kilmlogger.styles import LogLevelColumnFormatter


LOG_LEVEL_COLORS = {
    "critical": RED,
    "exception": RED,
    "error": RED,
    "warn": YELLOW,
    "warning": YELLOW,
    "info": GREEN,
    "debug": GREEN,
    "notset": RED_BACK,
}


def load_default_configuration(logging_filename: str = DEFAULT_FILE_LOG) -> None:
    # Configure logging
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "colored": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processors": [
                        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                        structlog.dev.ConsoleRenderer(
                            colors=True,
                            columns=[
                                Column(
                                    "",
                                    KeyValueColumnFormatter(
                                        key_style=None,
                                        value_style=DIM,
                                        reset_style=RESET_ALL,
                                        value_repr=str,
                                    ),
                                ),
                                Column(
                                    TIME_FIELD_NAME,
                                    KeyValueColumnFormatter(
                                        key_style=None,
                                        value_style=RESET_ALL,
                                        reset_style=RESET_ALL,
                                        value_repr=str,
                                    ),
                                ),
                                Column(
                                    LEVEL_FIELD_NAME,
                                    LogLevelColumnFormatter(
                                        LOG_LEVEL_COLORS, reset_style=RESET_ALL
                                    ),
                                ),
                                Column(
                                    CORRELATION_FIELD_NAME,
                                    KeyValueColumnFormatter(
                                        key_style=None,
                                        value_style=CYAN,
                                        reset_style=RESET_ALL,
                                        value_repr=str,
                                        width=30,
                                    ),
                                ),
                                Column(
                                    MESSAGE_FIELD_NAME,
                                    KeyValueColumnFormatter(
                                        key_style=None,
                                        value_style=BRIGHT,
                                        reset_style=RESET_ALL,
                                        value_repr=str,
                                        width=30,
                                    ),
                                ),
                            ],
                        ),
                    ],
                },
            },
            "handlers": {
                "default": {
                    "level": "INFO",
                    "class": "logging.StreamHandler",
                    "formatter": "colored",
                },
                "file": {
                    "level": "INFO",
                    "class": "logging.handlers.WatchedFileHandler",
                    "filename": logging_filename,
                },
                "scribe": {
                    "level": "INFO",
                    "class": "kilmlogger.handler.GRPCEventStreamingHandler",
                },
            },
            "loggers": {
                "": {
                    "handlers": ["default", "file", "scribe"],
                    "level": "INFO",
                    "propagate": True,
                },
            },
        }
    )

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            add_correlation,
            structlog.processors.TimeStamper(
                fmt=TIME_FORMAT, key=REPLACE_KEY_FOR_TIMESTAMP
            ),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.EventRenamer(to=REPLACE_KEY_FOR_EVENT),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
