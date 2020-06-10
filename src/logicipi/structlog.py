import logging
import logging.config
import sys
from typing import Any, Mapping

import structlog

log = structlog.get_logger()


def exception_hook(exc_type, exc_value, exc_traceback) -> None:
    """Execption hook to jsonify traceback"""
    log.error(
        "exception",
        exception_type=exc_type.__name__,
        exc_info=(exc_type, exc_value, exc_traceback),
    )


def from_level_to_severity(logger, log_method, event_dict) -> Mapping[str, Any]:
    """A custom processor for structlog, converts `level` to `severity`"""
    event_dict['severity'] = event_dict.pop('level')
    return event_dict


def configure_structlog(logging_level: str = "INFO", development: bool = False) -> None:
    """Configure structlog with some useful pre chains and json as processor.

    You can define the logging level by using logging_level.

    For local development you might consider setting `development=True` to have
    nice console rendered logs."""
    pre_chain = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    structlog.configure(
        processors=pre_chain
        + [
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            from_level_to_severity,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    processor = structlog.processors.JSONRenderer()

    if development:
        processor = structlog.dev.ConsoleRenderer()

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "plain": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": processor,
                "foreign_pre_chain": pre_chain,
            }
        },
        "handlers": {
            "default": {
                "level": logging_level,
                "class": "logging.StreamHandler",
                "formatter": "plain",
            }
        },
        "loggers": {
            "": {"level": logging_level, "handlers": ["default"], "propagate": False},
        },
    }

    sys.excepthook = exception_hook

    logging.config.dictConfig(LOGGING)
