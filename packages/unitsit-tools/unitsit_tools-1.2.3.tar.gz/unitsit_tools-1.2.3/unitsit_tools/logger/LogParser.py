import re
from datetime import datetime
from typing import NamedTuple, List, Optional


class LogEntry(NamedTuple):
    """
    Represents a log entry with timestamp, log level, filename, line number, and log message.
    """

    timestamp: datetime
    level: str
    filename: str
    lineno: int
    message: str


class LogFileParser:
    """
    Parses log files with a specified format and extracts log entries.
    """

    def __init__(self, log_format: str = ""):
        """
        Initializes a LogFileParser with the specified log format.

        :param log_format: Regular expression pattern for parsing log lines.
        :type log_format: str
        """
        self.log_format = log_format or (
            r"\[(?P<timestamp>.*?)\] "
            r"(?P<level>\w+) "
            r"\[(?P<filename>.*?):(?P<lineno>\d+)\] "
            r"(?P<message>.*)"
        )

    def parse_log_line(self, log_line: str, force: bool = False) -> Optional[LogEntry]:
        """
        Parses a single log line and returns a LogEntry if successful.

        :param log_line: Log line to be parsed.
        :type log_line: str
        :param force: If True, creates a LogEntry even for unparsable lines.
        :type force: bool
        :return: Parsed LogEntry or None.
        :rtype: Optional[LogEntry]
        """
        match = re.match(self.log_format, log_line)
        if match:
            timestamp_str = match.group("timestamp")
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

            level = match.group("level")
            filename = match.group("filename")
            lineno = int(match.group("lineno"))
            message = match.group("message")

            return LogEntry(
                timestamp=timestamp,
                level=level,
                filename=filename,
                lineno=lineno,
                message=message,
            )
        elif force:
            return LogEntry(
                timestamp=datetime.now(),
                level="UNPARSED",
                filename="",
                lineno=0,
                message=log_line,
            )
        else:
            return None

    def parse_log_file(self, log_file_path: str, force: bool = False) -> List[LogEntry]:
        """
        Parses a log file and returns a list of LogEntry objects.

        :param log_file_path: Path to the log file.
        :type log_file_path: str
        :param force: If True, includes entries for unparsable lines.
        :type force: bool
        :return: List of LogEntry objects.
        :rtype: List[LogEntry]
        """
        with open(log_file_path, "r", encoding="utf-8") as file:
            log_entries = []
            unparsable_entries = []

            for line in file:
                log_entry = self.parse_log_line(line, force)
                if log_entry:
                    log_entries.append(log_entry)
                else:
                    unparsable_entries.append(line.strip())

        if force and unparsable_entries:
            timestamp = datetime.now()
            level = "UNPARSED"
            filename = ""
            lineno = 0
            message = "\n".join(unparsable_entries)
            log_entries.append(
                LogEntry(
                    timestamp=timestamp,
                    level=level,
                    filename=filename,
                    lineno=lineno,
                    message=message,
                )
            )

        return log_entries
