# 20230618
import tomllib
import dataclasses
import logging


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


@dataclasses.dataclass
class Log:
    level: int
    count: int
    size: int


@dataclasses.dataclass
class Target:
    path: str
    type: str
    suffixes: list[str]
    smb_user: str
    smb_password: str


@dataclasses.dataclass
class FFmpeg:
    binary_path: str
    tmp_path: str


@dataclasses.dataclass
class Whisper:
    model_path: str  # where to find the models, where to place the models when download
    model_name: str  # tiny[.en], small[.en], medium[.en], large_v2  for detail, please read README.md
    model_device: str  # cuda,cpu,""  use "" to let whisper auto choose cuda or cpu


@dataclasses.dataclass
class Translate:
    enable: bool  # true,false
    target_language: str
    api: list[str]  # https://github.com/UlionTse/translators
    fail_hint: str  # "","translation failed"


@dataclasses.dataclass
class Srt:
    overwrite: bool  # true,false overwrite the existence srt
    bilingual: bool


@dataclasses.dataclass
class Config1:
    # media_path = r"\\B350m\e\电影\纪录片\国家地理.伟大工程巡礼系列National.Geographic.Megastructures.720p.HDTV"
    Targets: list[Target]

    FFmpeg: FFmpeg

    Whisper: Whisper

    Translate: Translate

    Srt: Srt

    Log: Log


CONFIG: Config1


def init_config() -> Config1:
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    CONFIG.Log = Log(level=logging.DEBUG, count=0, size=0)
    CONFIG.Log.size = data['log']['size'] * 1024 * 1024  # bytes to MB
    CONFIG.Log.count = data['log']['count']
    if data['log']['level'] == "info":
        CONFIG.Log.level = logging.INFO
    if data['log']['level'] == "warn":
        CONFIG.Log.level = logging.WARN
    if data['log']['level'] == "error":
        CONFIG.Log.level = logging.ERROR

    CONFIG.Targets = list()
    for t in data['log']['targets']:
        CONFIG.Targets.append(Target(path=t['path'], type=t['type'], suffixes=t['suffixes'],
                                     smb_user=t['smb_user'], smb_password=t['smb_password']))

    CONFIG.FFmpeg = FFmpeg(binary_path=data['ffmpeg']['binary_path'], tmp_path=data['ffmpeg']['tmp_path'])

    CONFIG.Whisper = Whisper(model_path=data['whisper']['model_path'], model_name=data['whisper']['model_name'],
                             model_device=data['whisper']['model_device'])

    CONFIG.Translate = Translate(enable=data['translate']['enable'],
                                 target_language=data['translate']['target_language'],
                                 api=data['translate']['api'], fail_hint=data['translate']['fail_hint'])

    CONFIG.Srt = Srt(overwrite=data['srt']['overwrite'], bilingual=data['srt']['bilingual'])
