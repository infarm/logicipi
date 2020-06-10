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


def test_Logger_with_stackdriver_disabled(mocker, monkeypatch):
    monkeypatch.setenv("DISABLE_GOOGLE_STACKDRIVER", "true")

    instance = Logger(function_name='my-function', region="my-region")

    log = instance.get_logger()

    assert isinstance(log, BoundLoggerLazyProxy)
