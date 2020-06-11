import pytest
from structlog import configure
from structlog._config import _Configuration

from logicipi.function import Logger


@pytest.fixture
def reset_structlog_conf():
    """
    Reset structlog configuration to default processors.
    """
    yield configure(processors=_Configuration.default_processors)


@pytest.fixture(scope="function", autouse=True)
def reset_singleton():
    """Reset the Logger singleton"""
    if hasattr(Logger, "_instance"):
        del Logger._instance
    yield
