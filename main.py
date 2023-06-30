import datetime
import logging
import pathlib

import whisper
from utils import CONFIG, get_files, get_logger, have_srt_file, remove_file
from utils import srt_writer, video2audio, transcriber

logger = get_logger("main")


def get_srt_filepath(video_file_fullpath: str) -> str:
    vf = pathlib.Path(video_file_fullpath)
    return str(vf.parent.joinpath(f"{vf.stem}.srt"))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logger.info('get files')
    for target in CONFIG.Targets:
        files = get_files(target)
        model: whisper.Whisper
        model_loaded: bool = False
        for video_file in files:
            # if not have srt file, or configured to overwrite
            if not have_srt_file(video_file) or CONFIG.Srt.overwrite:
                if not model_loaded:
                    logger.info('load model')
                    model = whisper.load_model(name=CONFIG.Whisper.model_name,
                                               device=CONFIG.Whisper.model_device,
                                               download_root=CONFIG.Whisper.model_path)
                    model_loaded = True
                logger.info(f'do file: {video_file}')
                audio_file = video2audio.video2audio(video_file)

                logger.info(f'now transcribe {audio_file}')
                srt_path = get_srt_filepath(video_file)

                writer = srt_writer.SRTWriter(srt_path)
                ts = datetime.datetime.now()
                segments = transcriber.transcribe_to_segments(model,
                                                              audio_file,
                                                              language=None,
                                                              verbose=CONFIG.Log.level == logging.DEBUG)
                for segment in segments:
                    writer.segment_to_srt1(segment)

                logger.info(f'srt file path: {srt_path}')
                logger.info(f'srt file for {video_file} generated')
                te = datetime.datetime.now()
                logger.debug(f"transcribe and translate to srt cost: {(te-ts).total_seconds()} seconds")
                logger.info(f"now delete tmp audio file {audio_file}")
                remove_file(audio_file)

