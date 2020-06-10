import os
from typing import Mapping, Union

from google.cloud import logging as google_logging
from google.cloud.logging.resource import Resource
from google.cloud.logging_v2.gapic.enums import LogSeverity
from structlog import BoundLogger, get_logger

from logicipi.structlog import configure_structlog


def stackdriver_logger_patcher(function_name: str, region: str, logger, severity):
    STACKDRIVER_RESOURCE = Resource(
        type="cloud_function",
        labels={"region": region, "function_name": function_name},
    )

    def parametrize_logger(event: Union[str, Mapping], **kwargs):
        if isinstance(event, str):
            log_dict = {'event': event, **kwargs}
        else:
            log_dict = {**event, **kwargs}

        return logger.log_struct(
            log_dict, severity=severity, resource=STACKDRIVER_RESOURCE
        )

    return parametrize_logger


def _logger(
    function_name: str, region: str
) -> Union[BoundLogger, google_logging.logger.Logger]:
    if 'DISABLE_GOOGLE_STACKDRIVER' in os.environ:
        configure_structlog()
        logger = get_logger()
        return logger

    log_name = 'cloudfunctions.googleapis.com%2Fcloud-functions'
    logger = google_logging.logger.Logger(log_name, google_logging.client.Client())
    logger.debug = stackdriver_logger_patcher(
        function_name, region, logger, LogSeverity.DEBUG
    )
    logger.info = stackdriver_logger_patcher(
        function_name, region, logger, LogSeverity.INFO
    )
    logger.warning = stackdriver_logger_patcher(
        function_name, region, logger, LogSeverity.WARNING
    )
    logger.error = stackdriver_logger_patcher(
        function_name, region, logger, LogSeverity.ERROR
    )

    return logger


class Logger:
    __slots__ = ("function_name", "region", "_logger")

    def __new__(cls, **kwargs) -> "Logger":
        if not hasattr(cls, '_instance') or not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *, function_name: str, region: str) -> None:
        self.function_name = function_name
        self.region = region
        self._logger = None

    def get_logger(self) -> Union[BoundLogger, google_logging.logger.Logger]:
        if not self._logger:
            self._logger = _logger(self.function_name, self.region)
        return self._logger
