import pathlib
import time
from loggingsystem.LogMessage import LogMessage
from loggingsystem.LogType import LogType
import os
import asyncio

# Returns the name for a new logfile based on the current time
def get_current_logfile():
    # Gets the folder path
    folder = str(pathlib.Path(__file__).parent.absolute()) + "/../logs/"

    # Gets the filename
    fname = time.strftime('%Y-%m-%dT%H-%M-%S', time.localtime()) + ".log"

    return folder + fname


class LoggingManager:
    # Path to the current log-file
    __log_file_path = get_current_logfile()

    # Stores log-messages (Not all, just unsaved ones)
    __logs: [LogMessage] = []

    # Incrementing id counter to uniquely identify messages
    __log_counter: int = 0

    # Array-index inside the __logs array where the file last left of
    __file_ptr: int = 0

    @staticmethod
    def get_logs_as_json():
        return list(map(lambda x: x.as_json(), LoggingManager.__logs))

    # Used by the loggers to register messages
    @staticmethod
    def on_message_log(type: LogType, logger_name: str, func_name: str, message: str):

        # Creates the log
        log = LogMessage(
            LoggingManager.__log_counter,
            type,
            logger_name,
            func_name,
            message
        )

        # Appends the log
        LoggingManager.__logs.append(log)

        # Increments the log-counter
        LoggingManager.__log_counter += 1

        # Moves the "dirty" file pointer forwards
        LoggingManager.__file_ptr += 1

        from webserver.WebProgram import broadcast_log
        broadcast_log(log.as_json())
        pass

    # Starts the timer to write logs every x seconds
    @staticmethod
    def start_logging_thread(save_delay_time: int):
        async def start_async_writer():
            # Ensure the parent directory exists
            pathlib.Path(os.path.dirname(LoggingManager.__log_file_path)).mkdir(parents=True, exist_ok=True)

            # Continuously logs
            while True:
                LoggingManager.write_to_disk_and_flush()
                await asyncio.sleep(save_delay_time)
                LoggingManager.on_message_log(LogType.INFO, "LogManager", "start_async_writer", "test lul")

        # Runs the writer tasks
        asyncio.run(start_async_writer())

    '''
    Writes the log to disk and ensures that the logging-buffer is not longer than at most x messages
    '''

    @staticmethod
    def write_to_disk_and_flush():
        # Writes the logs
        with open(LoggingManager.__log_file_path, "a") as fp:
            # Range of logs that still must be written
            frm = len(LoggingManager.__logs) - LoggingManager.__file_ptr
            to = len(LoggingManager.__logs)

            # Iterates over all logs which haven't been written yet
            for log_id in range(frm, to):
                fp.write(LoggingManager.__logs[log_id].to_single_line() + "\n")

            # Flushes the data
            fp.flush()

        # Ensures no more than x logs are kept in memory
        if len(LoggingManager.__logs) > 50:
            # Flushes all logs that are over 50
            LoggingManager.__logs = LoggingManager.__logs[(len(LoggingManager.__logs) - 50):]

        # Resets the dirty-logs ptr
        LoggingManager.__file_ptr = 0
