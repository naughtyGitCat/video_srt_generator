# 20230906
# todo implement
import logging
import datetime
import dataclasses
import typing

from utils.logger import get_logger
from utils.file import (get_file_name, get_path_parent)
from common.objects import ShareObjects

if typing.TYPE_CHECKING:
    from managers.database import DatabaseManager


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


class TranslationRecordManager:
    _dbm: DatabaseManager
    _logger: logging.Logger

    def __init__(self):
        self._dbm = ShareObjects.dbm
        self._logger = get_logger("translation")
        self._create_table()

    def _create_table(self) -> None:
        sql = f"""
            CREATE TABLE IF NOT EXISTS translation_job (
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
        self._dbm.execute(sql)

    def insert(self, path_name: str) -> None:
        path = get_path_parent(path_name)
        name = get_file_name(path_name)
        sql = f"""
                INSERT OR REPLACE INTO translation_job (path, name, status, progress, create_time, update_time, remark)
                VALUES ('{path}', '{name}', 'ready', 0, '{datetime.datetime.now()}', '{datetime.datetime.now()}', '');
                """
        self._dbm.execute(sql)

    def update_status(self, path_name: str, status: str, remark: str = '') -> None:
        path = get_path_parent(path_name)
        name = get_file_name(path_name)
        sql = f"""
            UPDATE translation_job
            SET status = '{status}', remark='{remark}', update_time='{datetime.datetime.now()}'
            WHERE path='{path}' AND name = '{name}'
            """
        self._dbm.execute(sql)

    def update_progress(self, path_name: str, progress: float) -> None:
        path = get_path_parent(path_name)
        name = get_file_name(path_name)
        sql = f"""
            UPDATE translation_job
            SET progress = {progress}, update_time='{datetime.datetime.now()}'
            WHERE path='{path}' AND name = '{name}'
            """
        self._dbm.execute(sql)


class HistoryRecordManager:
    _dbm: DatabaseManager
    _logger: logging.Logger

    def __init__(self):
        self._dbm = ShareObjects.dbm
        self._logger = get_logger("record")
        self._create_table()

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
        self._dbm.execute(sql)

    def select_latest(self) -> dict:
        sql = "SELECT * FROM history ORDER BY ID DESC LIMIT 1"
        return self._dbm.single(sql)

    def select_history(self, page_size: int = 10, page_number: int = 1) -> typing.Iterable[dict]:
        sql = f"SELECT * FROM history ORDER BY ID DESC LIMIT {page_size} {(page_number-1)*page_size}"
        return self._dbm.fetch(sql)

    def insert(self, path_name: str) -> None:
        path = get_path_parent(path_name)
        name = get_file_name(path_name)
        sql = f"""
                INSERT OR REPLACE INTO history (path, name, status, progress, create_time, update_time, remark)
                VALUES ('{path}', '{name}', 'start', 0, '{datetime.datetime.now()}', '{datetime.datetime.now()}', '');
                """
        self._dbm.execute(sql)

    def update_progress(self, path_name: str, progress: float):
        path = get_path_parent(path_name)
        name = get_file_name(path_name)
        sql = f"""
            UPDATE history
            SET progress = {progress}, update_time='{datetime.datetime.now()}'
            WHERE path='{path}' AND name = '{name}'
            """
        self._dbm.execute(sql)

    def update_status(self, path_name: str, status: str, remark: str = '') -> None:
        path = get_path_parent(path_name)
        name = get_file_name(path_name)
        sql = f"""
            UPDATE history
            SET status = '{status}', remark='{remark}', update_time='{datetime.datetime.now()}'
            WHERE path='{path}' AND name = '{name}'
            """
        self._dbm.execute(sql)
