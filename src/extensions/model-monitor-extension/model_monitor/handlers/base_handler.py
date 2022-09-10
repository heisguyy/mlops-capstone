# pylint: disable=too-few-public-methods,no-else-raise
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List


@dataclass(frozen=True)
class LogRecord:
    """
    Definition of what a log record looks like.
    """

    log_time: datetime
    request_id: str
    inputs: List
    results: List

    @staticmethod
    def parse(record: Dict[str, str]) -> "LogRecord":
        """Resolves data into a particular format to be stored.

        Args:
            record (Dict[str, str]): request_id, inputs and outputs in dictionary format.

        Returns:
            LogRecord: Another instance of LogRecord with the values defined in the inputs
        """
        return LogRecord(
            log_time=datetime.now(),
            request_id=record["request_id"],
            inputs=record["inputs"] if "inputs" in record.keys() else None,
            results=record["results"] if "results" in record.keys() else None,
        )

    @staticmethod
    def merge(first: "LogRecord", other: "LogRecord") -> "LogRecord":
        """Method to merge multiple records into a single record.

        Args:
            first (LogRecord): Earlier log record.
            other (LogRecord): New log record.

        Raises:
            KeyError: Raised when requests ID are not the same or
                     when they log records are entirely the same.

        Returns:
            LogRecord: New record formed from merging the two log records.
        """
        if first.request_id != other.request_id:
            raise KeyError("Request IDs do not match")
        elif first.__eq__(other):  # pylint: disable=unnecessary-dunder-call
            raise KeyError("Log records are the same, nothing to merge")

        return LogRecord(
            log_time=first.log_time,
            request_id=first.request_id,
            inputs=first.inputs or other.inputs,
            results=first.results or other.results,
        )


class LogsHandler(ABC):
    @abstractmethod
    def handle_logs(self, records: List[LogRecord]):
        """Unimplemeted class to log requests to s3.

        Args:
            records (List[LogRecord]): List of records accumulated.

        Raises:
            NotImplementedError: Implemented in the S3Handler Class.
        """
        raise NotImplementedError()
