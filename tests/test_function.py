import pytest
from structlog._config import BoundLoggerLazyProxy

from logicipi.function import Logger, LogSeverity, stackdriver_logger_patcher


def test_stackdriver_call_with_event_and_kwargs(mocker):
    logger_mock = mocker.MagicMock()
    log = stackdriver_logger_patcher(
        "function-1", "region-1", logger_mock, LogSeverity.INFO
    )

    log("my_event", data=1)

    logger_mock.log_struct.assert_called_once()

    [call] = logger_mock.log_struct.call_args_list
    assert call[0] == ({'event': 'my_event', 'data': 1},)


def test_stackdriver_call_with_dict(mocker):
    logger_mock = mocker.MagicMock()
    log = stackdriver_logger_patcher(
        "function-1", "region-1", logger_mock, LogSeverity.INFO
    )

    log({"event": "my_event", "data": 1})

    logger_mock.log_struct.assert_called_once()

    [call] = logger_mock.log_struct.call_args_list
    assert call[0] == ({'event': 'my_event', 'data': 1},)


def test_Logger(mocker):
    function_name, region = 'my-function', 'my-region'
    instance_1 = Logger(function_name=function_name, region=region)
    instance_2 = Logger()

    assert instance_1.function_name == function_name
    assert instance_1.region == region

    assert instance_1 is instance_2

    mocker.patch("logicipi.function._logger")

    assert instance_1.get_logger() is instance_2.get_logger()


def test_you_can_set_Logger_only_once():
    function_name_1, region_1 = 'my-function', 'my-region'

    instance_1 = Logger(function_name=function_name_1, region=region_1)
    assert instance_1.function_name == function_name_1
    assert instance_1.region == region_1

    function_name_2, region_2 = 'my-function-2', 'my-region-2'
    instance_2 = Logger(function_name=function_name_2, region=region_2)

    assert instance_1.function_name == function_name_1
    assert instance_1.region == region_1

    assert instance_1 is instance_2


@pytest.mark.parametrize(
    "envs,err_message",
    [
        ({"name": "FUNCTION_NAME", "value": "my-function"}, "region"),
        ({"name": "FUNCTION_REGION", "value": "my-region"}, "function_name"),
    ],
)
def test_Logger_with_one_env_missing(monkeypatch, envs, err_message):
    monkeypatch.setenv(**envs)

    with pytest.raises(ValueError) as err:
        Logger()

    assert err_message in str(err)


def test_Logger_with_env_variables(monkeypatch):
    env_fn_name = {"name": "FUNCTION_NAME", "value": "my-function"}
    env_fn_region = {"name": "FUNCTION_REGION", "value": "my-region"}
    monkeypatch.setenv(**env_fn_name)

    # valid function_name and function_region
    monkeypatch.setenv(**env_fn_name)
    monkeypatch.setenv(**env_fn_region)

    instance = Logger()

    assert instance.function_name == env_fn_name['value']
    assert instance.region == env_fn_region['value']


def test_Logger_with_missing_envs():
    with pytest.raises(ValueError):
        Logger()


def test_Logger_with_stackdriver_disabled(monkeypatch):
    monkeypatch.setenv("DISABLE_GOOGLE_STACKDRIVER", "true")

    instance = Logger(function_name='my-function', region="my-region")

    log = instance.get_logger()

    assert isinstance(log, BoundLoggerLazyProxy)
