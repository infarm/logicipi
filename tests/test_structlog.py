import pytest
import structlog
from utils import capture_logs

from logicipi.structlog import configure_structlog, from_level_to_severity


def test_from_level_to_severity():
    assert from_level_to_severity(None, None, {"level": "info"}) == {"severity": "info"}


def test_from_level_to_severity_with_empty_event_dict():
    with pytest.raises(KeyError):
        assert from_level_to_severity(None, None, {}) == {}


def test_no_configured_structlog(reset_structlog_conf):
    log = structlog.get_logger()

    with capture_logs() as cap_logs:
        log.info('Hello There')

        assert 'severity' not in cap_logs[0]


def test_configured_structlog(reset_structlog_conf):
    log = structlog.get_logger()

    configure_structlog()

    with capture_logs() as cap_logs:
        log.info('Hello There')

        assert 'severity' in cap_logs[0]
