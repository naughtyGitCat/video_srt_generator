# 20240204
import sqlite3
import typing
import logging
from utils import get_logger


class DatabaseManager:

    _conn: sqlite3.Connection
    _logger: logging.Logger

    def __init__(self):
        self._conn = sqlite3.connect("data.db", check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._logger = get_logger("database")

    def execute(self, sql: str) -> None:
        self._logger.debug(sql)
        self._conn.execute(sql)
        self._conn.commit()

    def fetch(self, sql: str) -> typing.Iterable[dict]:
        self._logger.debug(sql)
        for row in self._conn.execute(sql):
            yield dict([(k, row[k]) for k in row.keys()])

    def single(self, sql: str) -> dict:
        self._logger.debug(sql)
        for row in self._conn.execute(sql):
            return dict([(k, row[k]) for k in row.keys()])
