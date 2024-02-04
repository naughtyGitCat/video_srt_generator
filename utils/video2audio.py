# psyduck 20230618
import os
import subprocess
from utils.config import CONFIG
from utils.logger import get_logger
from utils.file import (get_file_name, get_path_parent, join_path)

log = get_logger("audio")


def clean_audio() -> None:
    if CONFIG.FFmpeg.tmp_path != "":
        os.remove(CONFIG.FFmpeg.tmp_path)


def video2audio(video_file: str) -> str:
    """
     & 'ffmpeg.exe' -i "soa1.mp4" -f wav -vn -acodec pcm_s16le -ar 16000 -ac 1  -ss 00:00:00 -to 00:04:10  "soa1.1.wav"
    :param video_file:
    :return:
    """
    log.debug(f'now video2audio {video_file}')
    if CONFIG.FFmpeg.tmp_path == "":
        _audio_tmp_path = get_path_parent(video_file)
    else:
        _audio_tmp_path = CONFIG.FFmpeg.tmp_path
    video_file_name = get_file_name(video_file)
    log.debug(f'video_file_name {video_file_name}')
    audio_file = join_path(_audio_tmp_path, f"{video_file_name}.wisper.wav")
    log.debug(f'audio_file {audio_file}')
    p = subprocess.Popen([CONFIG.FFmpeg.binary_path, "-i", video_file,
                          "-f", "wav", "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
                          # "-ss", "00:00:00", "-to", "00:01:10",  # for test, only convert the header fragment audio
                          "-y", audio_file],
                         stdout=subprocess.PIPE, encoding="utf-8")
    log.debug(f'{subprocess.list2cmdline(p.args)}')
    while True:
        output = p.stdout.readline()
        if p.poll() is not None and output == '':
            if p.poll() != 0:
                if p.stderr:
                    for line in p.stderr.readlines():
                        log.warning(line)
                raise RuntimeError
            else:
                log.info('video to audio generated success')
                return audio_file
        if output:
            log.info(output.strip())
