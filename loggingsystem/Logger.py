from loggingsystem.LogType import LogType


class Logger:
    def __init__(self, name: str):
        self.name = name

    def debug(self, method: str, message: str):
        from loggingsystem.LoggingManager import LoggingManager
        LoggingManager.on_message_log(
            LogType.DEBUG,
            self.name,
            method,
            message
        )

    def error_with_exception(self, method: str, message: str, exc: Exception):
        from loggingsystem.LoggingManager import LoggingManager
        LoggingManager.on_message_log(
            LogType.ERROR,
            self.name,
            method,
            message + " (" + str(exc) + ")"
        )

    def error(self, method: str, message: str):
        from loggingsystem.LoggingManager import LoggingManager
        LoggingManager.on_message_log(
            LogType.ERROR,
            self.name,
            method,
            message
        )

    def warn(self, method: str, message: str):
        from loggingsystem.LoggingManager import LoggingManager
        LoggingManager.on_message_log(
            LogType.WARNING,
            self.name,
            method,
            message
        )

    def warn_exception(self, method: str, message: str, exc: Exception):
        from loggingsystem.LoggingManager import LoggingManager
        LoggingManager.on_message_log(
            LogType.WARNING,
            self.name,
            method,
            message + " (" + str(exc) + ")"
        )

    def state_switch(self, method: str, message: str):
        from loggingsystem.LoggingManager import LoggingManager
        LoggingManager.on_message_log(
            LogType.STATE_SWITCH,
            self.name,
            method,
            message
        )

    def info(self, method: str, message: str):
        from loggingsystem.LoggingManager import LoggingManager
        LoggingManager.on_message_log(
            LogType.INFO,
            self.name,
            method,
            message
        )
