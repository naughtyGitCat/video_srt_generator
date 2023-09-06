# 20230906
# todo implement
import logging
import sqlite3
import datetime
import dataclasses


@dataclasses.dataclass
class DictateHistory:
    file_path: str  # full path
    file_hash: str  # skip if already have dictate success history
    status: str  # ready, doing, success, failed
    start_time: datetime.datetime
    end_time: datetime.datetime
    lines: int
    current_time: datetime.timedelta  # current dictating audio time
    whole_time: datetime.datetime     # audio file whole time
    current_progress: float  # 0 - 1  # calc by current_time/whole_time
    model: str  # dictate language model
    device: str  # dictate compute device


class RecordManager:
    conn: sqlite3.Connection
    logger: logging.Logger

    def __init__(self):
        pass

    def insert_record(self, dictate_history: DictateHistory) -> None:
        pass

    def update_progress(self, file_path: str, file_hash: str, current_time: datetime.timedelta, current_progress: float):
        pass

    def update_status(self, file_path:str, file_hash: str, status: str) -> None:
        pass
