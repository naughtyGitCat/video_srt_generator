# 20230618
import os
import typing
from utils import config
import smbclient
import platform


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
        return pathlib.Path(path).parent

def join_path(seg1: str, seg2: str) -> str: 
    """optimized for smb/local file"""
    if platform.system() != 'Windows' and seg1.startswith("\\\\"):
        return f"{seg1}\{seg2}"
    else:
        return os.path.join(seg1, seg2)

def smb_login() -> None:
    if config.Config.media_smb_user != "":
        smbclient.ClientConfig(username=config.Config.media_smb_user, password=config.Config.media_smb_password)


def get_files(filepath: str, recursive: bool) -> typing.Iterable[str]:
    if filepath.startswith('\\'):
        return get_smb_file(filepath, recursive)
    else:
        return get_local_file(filepath, recursive)


def get_local_file(filepath: str, recursive: bool) -> typing.Iterable[str]:
    entrypoints = os.scandir(filepath)
    for entrypoint in entrypoints:
        if entrypoint.is_dir() and recursive:
            r_files = get_local_file(entrypoint.path, recursive)
            for file in r_files:
                yield file
        if entrypoint.is_file():
            for suffix in config.Config.media_suffix:
                if entrypoint.name.endswith(suffix):
                    yield entrypoint.path


def get_smb_file(filepath: str, recursive: bool) -> typing.Iterable[any]:
    smb_login()
    for smb_entry in smbclient.scandir(filepath):
        if smb_entry.is_dir() and recursive:
            r_files = get_local_file(smb_entry.path, recursive)
            for file in r_files:
                yield file
        if smb_entry.is_file():
            for suffix in config.Config.media_suffix:
                if smb_entry.name.endswith(suffix):
                    yield smb_entry.path


def remove_file(filepath: str):
    smb_login()
    if filepath.startswith('\\'):
        smbclient.remove(filepath)
    else:
        os.remove(filepath)


def create_file(filepath: str):
    pass


if __name__ == "__main__":
    files = get_local_file(r"E:\Something\英雄时刻\516160507", False)
    for f in files:
        print(f)
