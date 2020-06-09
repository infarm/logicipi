import pytest

from logicipi.structlog import from_level_to_severity


def test_from_level_to_severity():
    assert from_level_to_severity(None, None, {"level": "info"}) == {"severity": "info"}


def test_from_level_to_severity_with_empty_event_dict():
    with pytest.raises(KeyError):
        assert from_level_to_severity(None, None, {}) == {}
