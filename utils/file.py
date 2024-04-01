# 20230618
import os
import typing
import pathlib
import smbclient
import platform


from utils.config import Target


def have_src_file(video_file: str) -> bool:
    pass


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
        return get_local_file(target)


def get_local_file(target: Target) -> typing.Iterable[str]:
    entrypoints = os.scandir(target.path)
    for entrypoint in entrypoints:
        if entrypoint.is_dir() and target.search_recursive:
            r_files = get_local_file(target)
            for file in r_files:
                yield file
        if entrypoint.is_file():
            for suffix in target.suffixes:
                if entrypoint.name.endswith(suffix):
                    yield entrypoint.path


def get_smb_file(target: Target) -> typing.Iterable[any]:
    if target.type == "smb":
        smb_login(target)
    for smb_entry in smbclient.scandir(target.path):
        if smb_entry.is_dir() and target.search_recursive:
            r_files = get_local_file(target)
            for file in r_files:
                yield file
        if smb_entry.is_file():
            for suffix in target.suffixes:
                if smb_entry.name.endswith(suffix):
                    yield smb_entry.path


def remove_file(filepath: str):
    if filepath.startswith('\\'):
        smbclient.remove(filepath)
    else:
        os.remove(filepath)


def create_file(filepath: str):
    pass


if __name__ == "__main__":
    files = get_local_file(Target(path=r"E:\Something\英雄时刻", suffixes=["mp4"], type="local", search_recursive=True))
    for f in files:
        print(f)
