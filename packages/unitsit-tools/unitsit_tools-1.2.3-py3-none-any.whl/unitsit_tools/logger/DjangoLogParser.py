from __future__ import annotations

import re
from datetime import datetime
from re import Pattern
from typing import List, Any
from typing import NamedTuple


class DjangoLogEntry(NamedTuple):
    """
    Represents a log entry with detailed information about a Django web application.

    Attributes:
    - timestamp (datetime): The timestamp when the log entry occurred.
    - ip (str): The IP address associated with the log entry.
    - level (str): The log level indicating the severity of the log entry.
    - view (str): The name of the Django view associated with the log entry.
    - lineno (int): The line number where the log entry originated.
    - method (str): The HTTP method (e.g., GET, POST) associated with the log entry.
    - route (str): The route or URL pattern associated with the log entry.
    - status_code (str): The HTTP status code associated with the log entry.
    - response_size (str): The size of the response associated with the log entry.

    Methods:
    - to_json(): Converts the log entry to a JSON-formatted string.

    Usage:
    log_entry = DjangoLogEntry(
        timestamp=datetime.now(),
        ip="127.0.0.1",
        level="INFO",
        view="example_view",
        lineno=42,
        method="GET",
        route="/example/",
        status_code="200 OK",
        response_size="1024 bytes"
    )

    json_representation = log_entry.to_json()
    """

    timestamp: datetime
    ip: str
    level: str
    view: str
    lineno: int
    method: str
    route: str
    status_code: str
    response_size: str

    def to_json(self):
        """
        Convert the log entry to a JSON-formatted string.

        Returns:
        str: JSON-formatted string representing the log entry.
        """

        import json

        return json.dumps(
            {
                "timestamp": self.timestamp.isoformat(),
                "ip": self.ip,
                "level": self.level,
                "view": self.view,
                "lineno": self.lineno,
                "method": self.method,
                "route": self.route,
                "status_code": self.status_code,
                "response_size": self.response_size,
            }
        )


class DjangoLogParser:
    """
    Parses Django log entries with a specified format and extracts log information.
    """

    log_format: Pattern[str] | Any

    def __init__(self, log_format=None):
        """
        Initialize the DjangoLogParser.

        :param log_format: Regular expression pattern for parsing log entries.
        :type log_format: str, optional
        """
        self.log_format = log_format or re.compile(
            r"\[(?P<timestamp>.*?)] "
            r"(?P<ip>[\w:.]+) "
            r"(?P<level>\w+) "
            r"\[(?P<view>.*?):(?P<lineno>\d+)] "
            r'"(?P<method>[A-Z]+) (?P<route>.*?) HTTP/[\d.]+" '
            r"(?P<status_code>\d+) "
            r"(?P<response_size>-|\d+)"
        )

    def set_log_format(self, log_format):
        """
        Set the log format pattern.

        :param log_format: Regular expression pattern for parsing log entries.
        :type log_format: str
        """
        self.log_format = re.compile(log_format)

    def get_log_format(self):
        """
        Get the current log format pattern.

        :return: Current log format pattern.
        :rtype: str
        """
        return self.log_format.pattern

    @staticmethod
    def filter_entries(entries, **kwargs):
        """
        Filter log entries based on specified criteria.

        :param entries: List of log entries.
        :type entries: List[DjangoLogEntry]
        :param kwargs: Filtering criteria as key-value pairs.
                       Example: filter_entries(log_entries, level='ERROR', view='app.views.home')
        :type kwargs: dict|Keyword Arguments
        :return: Filtered list of log entries.
        :rtype: List[DjangoLogEntry]
        """
        filtered_entries = entries

        if kwargs:
            for key, value in kwargs.items():
                filtered_entries = [
                    entry
                    for entry in filtered_entries
                    if getattr(entry, key, None) == value
                ]

        return filtered_entries

    @staticmethod
    def export_to_csv(entries, csv_file_path):
        """
        Export log entries to a CSV file.

        :param entries: List of log entries.
        :type entries: List[DjangoLogEntry]
        :param csv_file_path: Path to the CSV file.
        :type csv_file_path: str
        """
        import csv

        with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
            fieldnames = [
                "timestamp",
                "ip",
                "level",
                "view",
                "lineno",
                "method",
                "route",
                "status_code",
                "response_size",
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for entry in entries:
                writer.writerow(entry._asdict())

    def parse_log_line(self, log_line: str) -> DjangoLogEntry:
        """
        Parse a single log line and return a DjangoLogEntry if successful.

        :param log_line: Log line to be parsed.
        :type log_line: str
        :return: Parsed DjangoLogEntry or UNPARSED entry.
        :rtype: DjangoLogEntry
        """

        if match := self.log_format.match(log_line.strip()):
            groups = match.groupdict()
            timestamp_str = groups["timestamp"]
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

            return DjangoLogEntry(
                timestamp=timestamp,
                ip=groups["ip"],
                level=groups["level"],
                view=groups["view"],
                lineno=int(groups["lineno"]),
                method=groups["method"],
                route=groups["route"],
                status_code=groups["status_code"],
                response_size=groups["response_size"],
            )
        else:
            return DjangoLogEntry(
                timestamp=datetime.now(),
                ip="",
                level="UNPARSED",
                view="",
                lineno=0,
                method="",
                route=log_line,
                status_code="",
                response_size="",
            )

    def parse_log_file(self, log_file_path: str) -> List[DjangoLogEntry]:
        """
        Parse a log file and return a list of DjangoLogEntry objects.

        :param log_file_path: Path to the log file.
        :type log_file_path: str
        :return: List of DjangoLogEntry objects.
        :rtype: List[DjangoLogEntry]
        """
        with open(log_file_path, "r", encoding="utf-8") as file:
            return list(map(self.parse_log_line, file.readlines()))

    def __dict__(self) -> dict[str, str]:  # type: ignore
        """
        Return a dictionary representation of the DjangoLogParser instance.

        :return: Dictionary representation of the instance.
        :rtype: dict
        """

        return {"log_format": self.get_log_format()}
