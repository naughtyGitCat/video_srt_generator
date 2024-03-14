# 20230618
import os
import typing
import pathlib
import smbclient
import platform
import subprocess

from utils.config import CONFIG, Target


def have_srt_file(video_file: str) -> bool:
    path_object = pathlib.Path(video_file)
    srt_name = path_object.name.split(path_object.suffix)[0] + ".srt"
    srt_file = path_object.parent.joinpath(srt_name)
    if video_file.startswith("\\"):
        return smbclient.path.exists(srt_file)
    else:
        return os.path.exists(srt_file)


def is_pre_translated(video_file_name: str) -> bool:
    if video_file_name.upper().find("-C.") > 0:
        return True


def subtitle_embedded(video_file: str) -> bool:
    """
    use mediainfo or ffmpeg check video file have subtitle stream
    ffmpeg -hide_banner -i test.mkv -c copy -map 0:s:0 -frames:s 1 -f null - -v 0;echo $?
    https://stackoverflow.com/questions/43005432/check-if-a-video-file-has-subtitles
    """
    cmd = f"{CONFIG.FFmpeg.binary_path} -hide_banner -i test.mkv -c copy -map 0:s:0 -frames:s 1 -f null - -v 0"
    status, data = subprocess.getstatusoutput(cmd)


def need_translation(video_file_name: str) -> bool:
    if is_pre_translated(video_file_name):
        return False
    if have_srt_file(video_file_name) and not CONFIG.Srt.overwrite:
        return False
    return True


def get_file_name(path: str) -> str:
    """optimized for smb/local file"""
    if platform.system() != 'Windows' and path.startswith("\\\\"):
        # windows \\ style
        return path.split('\\')[-1]
    else:
        return pathlib.Path(path).name


def get_path_parent(path: str) -> str:
    """optimized for smb/local file"""
    if platform.system() != 'Windows' and path.startswith("\\\\"):
        segments = path.split('\\')
        return "\\".join(segments[0:-2])
    else:
        return str(pathlib.Path(path).parent)


def join_path(seg1: str, seg2: str) -> str:
    """optimized for smb/local file"""
    if platform.system() != 'Windows' and seg1.startswith("\\\\"):
        return f"{seg1}\{seg2}"
    else:
        return os.path.join(seg1, seg2)


def smb_login(target: Target) -> None:
    if target.smb_user != "":
        smbclient.ClientConfig(username=target.smb_user, password=target.smb_password)


def get_files(target: Target) -> typing.Iterable[str]:
    if target.path.startswith('\\'):
        return get_smb_file(target)
    else:
        return get_local_file(target.path, target.search_recursive, target.suffixes)


def get_local_file(path: str, search_recursive: bool, suffixes: list[str]) -> typing.Iterable[str]:
    entrypoints = os.scandir(path)
    for entrypoint in entrypoints:
        if entrypoint.is_dir() and search_recursive:
            r_files = get_local_file(entrypoint.path, search_recursive, suffixes)
            for file in r_files:
                yield file
        if entrypoint.is_file():
            for suffix in suffixes:
                if entrypoint.name.endswith(suffix):
                    yield os.path.abspath(entrypoint.path)


def get_smb_file(target: Target) -> typing.Iterable[any]:
    if target.type == "smb":
        smb_login(target)
    for smb_entry in smbclient.scandir(target.path):
        if smb_entry.is_dir() and target.search_recursive:
            r_files = get_smb_file(target)
            for file in r_files:
                yield file
        if smb_entry.is_file():
            for suffix in target.suffixes:
                if smb_entry.name.endswith(suffix):
                    yield smb_entry.path


def remove_file(filepath: str):
    # if exist_file(filepath):
    if filepath.startswith('\\'):
        smbclient.remove(filepath)
    else:
        os.remove(filepath)


def exist_file(filepath: str):
    if filepath.startswith("\\"):
        return smbclient.path.exists(filepath)
    else:
        return os.path.exists(filepath)


def create_file(filepath: str):
    pass


if __name__ == "__main__":
    files = get_local_file(Target(path=r"E:\Something\x", suffixes=["mp4"], type="local", search_recursive=True))
    for f in files:
        print(f)
