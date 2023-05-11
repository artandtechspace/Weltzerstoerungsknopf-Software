import time
from loggingsystem.LogType import LogType


class LogMessage:
    def __init__(self, log_id: int, log_type: LogType, logger_name: str, func_name: str, message: str):
        self.log_id = log_id
        self.log_type = log_type
        self.message = message
        self.logger_name = logger_name
        self.func_name = func_name
        self.log_time = time.localtime()

    # Turn the log into a single string which can be saved to a file
    def to_single_line(self):
        return "{} - [{}] ({} / {}): {}".format(
            time.strftime('%Y-%m-%dT%H-%M-%S', time.localtime()),
            self.log_type.value,
            self.logger_name,
            self.func_name,
            self.message
        )

    # Returns the log as a json-serializable object
    def as_json(self):
        return {
            "type": self.log_type.value,
            "logger": self.logger_name,
            "func": self.func_name,
            "msg": self.message,
            "time": self.log_time
        }
