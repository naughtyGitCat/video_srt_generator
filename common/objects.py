# 20240204

from managers.database import DatabaseManager


class ShareObjects:
    dbm: DatabaseManager
    current_status: str
    current_srt: str
    current_audio: str
