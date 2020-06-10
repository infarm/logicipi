import pytest
from structlog import configure
from structlog._config import _Configuration


@pytest.fixture
def reset_structlog_conf():
    """
    Reset structlog configuration to default processors.
    """
    yield configure(processors=_Configuration.default_processors)
