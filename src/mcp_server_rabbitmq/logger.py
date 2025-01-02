import datetime
from enum import IntEnum

class LOG_LEVEL(IntEnum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3

# TODO: see if there are better libraries available
class Logger:
    def __init__(self, log_file_path: str, log_level: LOG_LEVEL = LOG_LEVEL.WARNING):
        self.log_file_path = log_file_path
        self.log_level = log_level
    
    def debug(self, msg):
        if not self.__should_skip_logging(LOG_LEVEL.DEBUG):
            self.__write_log(self.__post_process_log_entry(msg, LOG_LEVEL.DEBUG))

    def info(self, msg):
        if not self.__should_skip_logging(LOG_LEVEL.INFO):
            self.__write_log(self.__post_process_log_entry(msg, LOG_LEVEL.INFO))

    def warning(self, msg):
        if not self.__should_skip_logging(LOG_LEVEL.WARNING):
            self.__write_log(self.__post_process_log_entry(msg, LOG_LEVEL.WARNING))

    def error(self, msg):
        if not self.__should_skip_logging(LOG_LEVEL.ERROR):
            self.__write_log(self.__post_process_log_entry(msg, LOG_LEVEL.ERROR))

    def __post_process_log_entry(self, msg: str, log_level: LOG_LEVEL) -> str:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{log_level.name}] {timestamp} - {msg}\n"

    def __write_log(self, msg):
        with open(self.log_file_path, "a") as f:
            f.write(msg)
            # TODO: look for optimization opportunity here
            f.flush()
    
    def __should_skip_logging(self, log_level: LOG_LEVEL) -> bool:
        return int(log_level) < int(self.log_level)