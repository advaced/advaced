from logging import (StreamHandler, Formatter, LogRecord, basicConfig, info as log_info, warning as log_warning,
                     error as log_error, debug as log_debug, critical as log_critical)

# Add to path
from sys import path
from os.path import dirname, abspath, join

path.insert(0, join(dirname(abspath(__file__)), '..', '..'))

from __init__ import LOG_FILE, LOG_LEVEL, FORMATS


class CustomFormatter(Formatter):
    def format(self, record: LogRecord) -> str:
        log_format = FORMATS[record.levelno]
        formatter = Formatter(log_format, style='{')

        return formatter.format(record)


def init_logger():
    handler = StreamHandler()
    handler.setFormatter(CustomFormatter())

    basicConfig(level=LOG_LEVEL, handlers=[handler])

    return handler
