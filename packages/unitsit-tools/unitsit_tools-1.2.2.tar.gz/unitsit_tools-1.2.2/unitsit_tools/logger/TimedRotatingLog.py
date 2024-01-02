from __future__ import annotations

import os
from enum import IntEnum
from logging import Formatter, getLogger
from logging.handlers import TimedRotatingFileHandler


class Level(IntEnum):
    """
    Enumeration for various log levels.
    """

    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class TimedRotatingLog:
    """
    TimedRotatingLog creates a logger with a TimedRotatingFileHandler for rotating log files.

    :param name: The name of the logger.
    :param level: The log level, default is INFO.
    :param path: The path where the log file will be created. By default, this is the current working directory.
    :param timer: The interval for rotating log files in minutes, default is 1440 (24 hours).
    :param max_backups: Maximum number of backups before old files are overwritten. By default, this is 14.
    :param log_format: The format string for log messages, default is standard format.

    Attributes:
        name (str): The name of the logger.
        level (int): The log level.
        timer (int): The interval for rotating log files.
        max_backups (int): Maximum number of backups.
        path (str): The full path to the log file.

    Methods:
        info(message: str): Writes a log message with the INFO level.
        warn(message: str): Writes a log message with the WARNING level.
        error(message: str): Writes a log message with the ERROR level.
        debug(message: str): Writes a log message with the DEBUG level.
        critical(message: str): Writes a log message with the CRITICAL level.
    """

    def __init__(
        self,
        name: str,
        level: int | Level = Level.INFO,
        path: str = os.getcwd(),
        timer: int = 1440,
        max_backups: int = 14,
        log_format: str = "",
    ) -> None:
        """
        Initializes the TimedRotatingLog.

        :param name: The name of the logger.
        :param level: The log level, default is INFO.
        :param path: The path where the log file will be created. By default, this is the current working directory.
        :param timer: The interval for rotating log files in minutes, default is 1440 (24 hours).
        :param max_backups: Maximum number of backups before old files are overwritten. By default, this is 14.
        :param log_format: The format string for log messages, default is standard format.
        """
        self.name = name or "Log"
        self.level = level
        self.timer = timer
        self.max_backups = max_backups
        self.path = os.path.join(path, f"{name}.log")

        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        self.handler = TimedRotatingFileHandler(
            filename=self.path,
            when="M",
            interval=timer,
            backupCount=self.max_backups,
            encoding="utf-8",
            delay=False,
        )

        # Set log format if provided, otherwise use the default
        log_format = (
            log_format
            or "[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)d] %(message)s"
        )

        self.handler.setFormatter(Formatter(log_format, "%Y-%m-%d %H:%M:%S"))
        self.handler.suffix = "%Y-%m-%d_%H-%M.log"

        self._log = getLogger(self.name)
        self._log.setLevel(self.level)
        self._log.addHandler(self.handler)

    def info(self, message: str) -> None:
        """
        Writes a log message with the INFO level.

        :param message: The log message.
        """
        self._log.info(message)

    def warn(self, message: str) -> None:
        """
        Writes a log message with the WARNING level.

        :param message: The log message.
        """
        self._log.warning(message)

    def error(self, message: str) -> None:
        """
        Writes a log message with the ERROR level.

        :param message: The log message.
        """
        self._log.error(message)

    def debug(self, message: str) -> None:
        """
        Writes a log message with the DEBUG level.

        :param message: The log message.
        """
        self._log.debug(message)

    def critical(self, message: str) -> None:
        """
        Writes a log message with the CRITICAL level.

        :param message: The log message.
        """
        self._log.critical(message)
