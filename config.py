# 20230618
import dataclasses


class Config:

    # media_path = r"\\B350m\e\电影\纪录片\国家地理.伟大工程巡礼系列National.Geographic.Megastructures.720p.HDTV"
    media_path = r"\\Gen8\d\RAW\STARS-250"
    media_suffix = ["mp4", "mkv", "wmv", 'avi']  # add common video .extension here
    media_smb_user = ""
    media_smb_password = ""
    media_search_recursive = True

    ffmpeg = r"C:\Program Files\FFmpeg\bin\ffmpeg.exe"
    audio_tmp_path = r"F:\audio_tmp"

    # for more detail, please read github.com/openai/whisper/__init__.py,transcribe.py
    whisper_model_path = r"E:\wisper\models"  # where to find the models, where to place the models when download
    whisper_model_name = "medium"  # tiny[.en], small[.en], medium[.en], large_v2. for detail, please read README.md
    whisper_model_device = None  # cuda,cpu,None(without quotes). use None to let whisper auto choose cuda or cpu

    translate = True
    translate_to = "zh"
    translate_api = ["google", "bing", "Sogou", "Baidu", "Iflytek"]  # https://github.com/UlionTse/translators
    translate_fail_action = ""  # use '' or 'translation failed'

    srt_overwrite = True  # overwrite the existence srt
    srt_bilingual = True  # translated words in first line, while the origin lying on second line

    verbose = True
