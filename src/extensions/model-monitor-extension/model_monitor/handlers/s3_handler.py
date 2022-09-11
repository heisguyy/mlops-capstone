import random
from typing import List
import boto3

from model_monitor.configuration import Configuration
from model_monitor.handlers.base_handler import LogsHandler, LogRecord


class S3Handler(LogsHandler):
    def handle_logs(self, records: List[LogRecord]) -> bool:
        """Implemented method from parent class to log requests to s3 bucket.

        Args:
            records (List[LogRecord]): List of records to be sent to the s3 bucket.

        Returns:
            bool: True if there is a defined bucket and records to be logged.
        """
        # pylint: disable=invalid-name
        if not (Configuration.s3_bucket and records):
            return False
        key = S3Handler.get_key_name(records)
        data = S3Handler.format_records(records)
        if not Configuration.is_test:
            s3 = boto3.client("s3")
        else:
            s3 = boto3.client(
                "s3",
                endpoint_url="http://host.docker.internal:9000",
                aws_access_key_id="minioadmin",
                aws_secret_access_key="minioadmin",
            )
            print("Defined S3 resources.")
        s3.put_object(Body=data, Bucket=Configuration.s3_bucket, Key=key)
        print("Put in object already")
        return True

    @staticmethod
    def get_key_name(records: List[LogRecord]) -> str:
        """Generates the filename.

        Args:
            records (List[LogRecord]): List of records to be logged.

        Returns:
            str: name of file where logs will be stored.
        """
        start_time = min(r.log_time for r in records)
        log_directory = f"monitor-{start_time.year}-{start_time.month}-{start_time.day}-{start_time.hour}"  # pylint: disable=line-too-long
        return f"{log_directory}-{random.random()}"

    @staticmethod
    def format_records(records: List[LogRecord]) -> bytes:
        """Formats the record to a defined format.

        Args:
            records (List[LogRecord]): List of records to be logged.

        Returns:
            bytes: encoded records.
        """
        return "\n".join(map(S3Handler._format_record, records)).encode()

    @staticmethod
    def _format_record(r: LogRecord) -> str:  # pylint: disable=invalid-name
        """Returns format for records.

        Args:
            r (LogRecord): a records from the list of records

        Returns:
            str: format for a record to fit.
        """
        return f"{r.log_time.isoformat()} : {r.inputs} : {r.results}"
