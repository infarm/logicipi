from contextlib import contextmanager

from structlog import DropEvent, configure, get_config


class LogCapture:
    """
    Class for capturing log messages in its entries list.
    but you can use this class if you want to capture logs with other patterns.
    """

    def __init__(self):
        self.entries = []

    def __call__(self, _, method_name, event_dict):
        if "event" in event_dict:
            self.entries.append(event_dict)
        else:
            # event_dict is a tuple with multiple elements
            # (({log dict},),{dict with extra info})
            self.entries.append(event_dict[0][0])
        raise DropEvent


@contextmanager
def capture_logs():
    """
    Context manager that appends all logging statements to its yielded list
    while it is active.

    It appends a LogCapture to the existing processors.
    """
    cap = LogCapture()
    old_processors = get_config()["processors"]
    try:
        configure(processors=[*old_processors, cap])
        yield cap.entries
    finally:
        configure(processors=old_processors)
