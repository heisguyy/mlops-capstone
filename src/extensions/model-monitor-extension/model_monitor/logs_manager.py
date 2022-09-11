from datetime import datetime
from typing import Dict, List

# from model_monitor.configuration import Configuration
from model_monitor.handlers.base_handler import LogRecord, LogsHandler


class LogsManager:
    _singleton = None

    def __init__(self):
        self.last_time_sent: datetime = datetime.now()
        self.pending_logs: Dict[str, LogRecord] = {}
        self.pending_logs_size: int = 0

    # add_records
    def add_records(self, raw_records: List[dict]):
        """Add responses to previous response waiting to be  processed and sent.

        Args:
            raw_records (List[dict]): list of responses from the lambda function.
        """
        for record in raw_records:
            self.add_record(record)

    def add_record(self, raw_record: dict):
        """Add response to previous response waiting to be  processed and sent.

        Args:
            raw_record (dict): response from the lambda function.
        """
        new_record = LogRecord.parse(raw_record)

        if new_record.request_id in self.pending_logs:
            existing_record = self.pending_logs[new_record.request_id]
            self.pending_logs[new_record.request_id] = LogRecord.merge(
                existing_record, new_record
            )
        else:
            self.pending_logs[new_record.request_id] = new_record
            self.pending_logs_size += 1

    # # send the batch if the size or time window are exceeded
    # def send_batch_if_needed(self) -> bool:
    #     """Sends values if condition is met.

    #     Returns:
    #         bool: True if sends values False if it doesn't send.
    #     """
    #     over_batch_size = self.pending_logs_size >= Configuration.batch_size
    #     over_batch_window = (
    #         datetime.now() - self.last_time_sent
    #     ).total_seconds() >= Configuration.batch_window

    #     if over_batch_size or over_batch_window:
    #         self.send_batch()
    #         return True
    #     return False

    # send_batch
    def send_batch(self) -> bool:
        """Sends values.

        Returns:
            bool: always returns True.
        """
        self.last_time_sent = datetime.now()
        if not self.pending_logs:
            return False

        available_handlers = LogsHandler.__subclasses__()
        for handler in available_handlers:
            try:
                handler().handle_logs(self.pending_logs.values())
            except Exception as err:  # pylint: disable=broad-except
                print("Exception!! Could not handle sending logs")
                print(f"error: {err}")

        self.pending_logs.clear()
        self.pending_logs_size = 0

        return True

    @staticmethod
    def get_manager():
        """Initiliazes LogManager

        Returns:
            _type_: _description_
        """
        if not LogsManager._singleton:
            LogsManager._singleton = LogsManager()
        return LogsManager._singleton
