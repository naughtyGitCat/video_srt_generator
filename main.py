import datetime
import pathlib
import pprint

import whisper
import config
from utils.file import get_files, remove_file
from utils import srt_writer, video2audio, transcriber


def get_srt_filepath(video_file_fullpath: str) -> str:
    vf = pathlib.Path(video_file_fullpath)
    return str(vf.parent.joinpath(f"{vf.stem}.srt"))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('get files')
    files = get_files(config.Config.media_path, config.Config.media_search_recursive)

    model: whisper.Whisper
    model_loaded: bool = False
    for video_file in files:
        if not model_loaded:
            print('load model')
            model = whisper.load_model(name=config.Config.whisper_model_name,
                                       device=config.Config.whisper_model_device,
                                       download_root=config.Config.whisper_model_path)
            model_loaded = True
        print(f'do file: {video_file}')
        audio_file = video2audio.video2audio(video_file)

        print(f'now transcribe {audio_file}')
        srt_path = get_srt_filepath(video_file)
        # result = model.transcribe(audio_file, language=None, verbose=config.Config.verbose)
        # print(f'[DEBUG] {pprint.pprint(result)}')
        # remove_file(audio_file)
        # writer = srt_writer.get_srt_writer(str(pathlib.Path(video_file).parent))
        # writer(result, video_file)

        writer = srt_writer.SRTWriter(srt_path)
        ts = datetime.datetime.now()
        segments = transcriber.transcribe_to_segments(model,
                                                      audio_file,
                                                      language=None,
                                                      verbose=config.Config.verbose)
        for segment in segments:
            writer.segment_to_srt1(segment)

        print(f'srt file path: {srt_path}')
        print(f'srt file for {video_file} generated')
        te = datetime.datetime.now()
        print(f"[DEBUG] transcribe and translate to srt cost: {(te-ts).total_seconds()} seconds")
