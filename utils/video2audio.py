# psyduck 20230618
import os.path
import pathlib
import subprocess

import config

FFMPEG = r"C:\Program Files\FFmpeg\bin\ffmpeg.exe"


def video2audio(video_file: str) -> str:
    """
     & 'ffmpeg.exe' -i "soa1.mp4" -f wav -vn -acodec pcm_s16le -ar 16000 -ac 1  -ss 00:00:00 -to 00:04:10  "soa1.1.wav"
    :param video_file:
    :return:
    """
    print(f'[DEBUG]now video2audio {video_file}')
    if config.Config.audio_tmp_path == "":
        _audio_tmp_path = pathlib.Path(video_file).parent
    else:
        _audio_tmp_path = config.Config.audio_tmp_path
    video_file_name = pathlib.Path(video_file).name
    print(f'[DEBUG]video_file_name {video_file_name}')
    audio_file = os.path.join(_audio_tmp_path, f"{video_file_name}.wisper.wav")
    print(f'[DEBUG]audio_file {audio_file}')
    p = subprocess.Popen([FFMPEG, "-i", video_file,
                          "-f", "wav", "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
                          "-ss", "00:00:00", "-to", "00:01:10",  # for test, only convert the header fragment audio
                          "-y", audio_file],
                         stdout=subprocess.PIPE, encoding="utf-8")
    while True:
        output = p.stdout.readline()
        if p.poll() is not None and output == '':
            if p.poll() != 0:
                if p.stderr:
                    for line in p.stderr.readlines():
                        print(line)
                raise RuntimeError
            else:
                print('[DEBUG]video to audio generated success')
                return audio_file
        if output:
            print(output.strip())
