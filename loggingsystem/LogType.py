from enum import Enum


class LogType(Enum):
    ERROR = "error"
    DEBUG = "debug"
    WARNING = "warn"
    INFO = "info"
    STATE_SWITCH = "state"
