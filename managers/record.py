# 20230906
# todo implement
import logging
import sqlite3
import datetime
import dataclasses
from utils.logger import get_logger
from utils.file import (get_file_name, get_path_parent)


@dataclasses.dataclass
class DictateHistory:
    file_path: str  # full path
    file_hash: str  # skip if already have dictate success history
    status: str  # start, doing(ffmpeg, transcribe), success/failed
    start_time: datetime.datetime
    end_time: datetime.datetime
    lines: int
    current_time: datetime.timedelta  # current dictating audio time
    whole_time: datetime.datetime  # audio file whole time
    current_progress: float  # 0 - 1  # calc by current_time/whole_time
    model: str  # dictate language model
    device: str  # dictate compute device


class RecordManager:
    conn: sqlite3.Connection
    logger: logging.Logger

    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.logger = get_logger("record")

    def _create_table(self) -> None:
        sql = f"""
            CREATE TABLE IF NOT EXISTS history (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              path TEXT NOT NULL,
              name TEXT NOT NULL,
              status TEXT NOT NULL,
              progress REAL NOT NULL,
              create_time DATETIME NOT NULL,
              update_time DATETIME NOT NULL,
              remark TEXT NOT NULL,
              UNIQUE (path, name)
            );
            """
        self.conn.execute(sql)

    def _table_exists(self) -> bool:
        pass

    def insert_record(self, path_name: str) -> None:
        path = get_path_parent(path_name)
        name = get_file_name(path_name)
        sql = f"""
                INSERT OR REPLACE INTO history (path, name, status, progress, create_time, update_time, remark)
                VALUES ('{path}', '{name}', 'start', 0, '{datetime.datetime.now()}', '{datetime.datetime.now()}', '');
                """
        self.conn.execute(sql)

    def update_progress(self, path_name: str, progress: float):
        path = get_path_parent(path_name)
        name = get_file_name(path_name)
        sql = f"""
            UPDATE history
            SET progress = {progress}
            WHERE path='{path}' AND name = '{name}'
            """
        self.conn.execute(sql)

    def update_status(self, path_name: str, status: str, remark: str = '') -> None:
        path = get_path_parent(path_name)
        name = get_file_name(path_name)
        sql = f"""
            UPDATE history
            SET status = '{status}', remark='{remark}'
            WHERE path='{path}' AND name = '{name}'
            """
        self.conn.execute(sql)
