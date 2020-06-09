from logicipi.functions import LogSeverity, stackdriver_logger_patcher


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
