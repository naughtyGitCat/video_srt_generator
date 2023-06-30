# 20230618
import pathlib
import tomllib
import dataclasses
import logging
import typing

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
    smb_user: str = ""
    smb_password: str = ""
    search_recursive: bool = True


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


@dataclasses.dataclass(frozen=True)
class Config:
    _instance: typing.Optional[typing.Self] = dataclasses.field(init=False, repr=False)

    Targets: list[Target]

    FFmpeg: typing.Optional[FFmpeg]

    Whisper: typing.Optional[Whisper]

    Translate: typing.Optional[Translate]

    Srt: typing.Optional[Srt]

    Log: typing.Optional[Log]

    @classmethod
    def init_config(cls) -> typing.Self:
        if cls._instance is None:
            config = pathlib.Path().absolute().joinpath("config.toml")
            with open(config, "rb") as f:
                data = tomllib.load(f)
            log_config = Log(level=logging.DEBUG, count=0, size=0)
            log_config.size = data['log']['size'] * 1024 * 1024  # bytes to MB
            log_config.count = data['log']['count']
            if data['log']['level'] == "info":
                log_config.level = logging.INFO
            if data['log']['level'] == "warn":
                log_config.level = logging.WARN
            if data['log']['level'] == "error":
                log_config.level = logging.ERROR

            targets: list[Target] = list()
            for t in data['targets']:
                targets.append(Target(path=t['path'], type=t['type'], suffixes=t['suffixes'],
                                      smb_user=t['smb_user'], smb_password=t['smb_password'],
                                      search_recursive=t['search_recursive']))

            ffmpeg_config = FFmpeg(binary_path=data['ffmpeg']['binary_path'], tmp_path=data['ffmpeg']['tmp_path'])

            whisper_config = Whisper(model_path=data['whisper']['model_path'], model_name=data['whisper']['model_name'],
                                     model_device=data['whisper']['model_device'])

            translate_config = Translate(enable=data['translate']['enable'],
                                         target_language=data['translate']['target_language'],
                                         api=data['translate']['api'], fail_hint=data['translate']['fail_hint'])

            srt_config = Srt(overwrite=data['srt']['overwrite'], bilingual=data['srt']['bilingual'])

            cls._instance = Config(Targets=targets,
                                   FFmpeg=ffmpeg_config,
                                   Whisper=whisper_config,
                                   Translate=translate_config,
                                   Srt=srt_config,
                                   Log=log_config)
            return cls._instance


CONFIG: typing.Optional[Config] = Config.init_config()
