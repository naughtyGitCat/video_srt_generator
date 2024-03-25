# 20240204
from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from managers.database import DatabaseManager
    from managers.record import HistoryRecordManager, TranslationRecordManager


class ShareObjects:
    dbm: DatabaseManager
    history_record_manager: HistoryRecordManager
    translation_record_manager: TranslationRecordManager
    current_status: str
    current_srt: str
    current_audio: str

    @classmethod
    def reset_current(cls):
        cls.current_status = ""
        cls.current_srt = ""
        cls.current_audio = ""


