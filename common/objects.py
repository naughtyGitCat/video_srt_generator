# 20240204

from managers.database import DatabaseManager
from managers.record import  HistoryRecordManager, TranslationRecordManager


class ShareObjects:
    dbm: DatabaseManager
    history_record_manager: HistoryRecordManager
    translation_record_manager: TranslationRecordManager
    current_status: str
    current_srt: str
    current_audio: str
