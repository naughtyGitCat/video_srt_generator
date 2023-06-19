# 20230618
import dataclasses


class Config:
    ffmpeg = r"C:\Program Files\FFmpeg\bin\ffmpeg.exe"
    audio_tmp_path = r"F:\audio_tmp"

    model = r"E:\wisper\models\medium.pt"

    # media_path = r"E:\Something\英雄时刻"
    media_path = r"\\B350m\e\电影\纪录片\国家地理.伟大工程巡礼系列National.Geographic.Megastructures.720p.HDTV"
    media_suffix = ["mp4", "mkv", "wmv", 'avi']
    media_smb_user = ""
    media_smb_password = ""
    search_recursive = True
    translate = True
    translate_to = "zh"

    overwrite = True
    verbose = True
