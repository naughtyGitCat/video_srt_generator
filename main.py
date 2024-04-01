import datetime
import logging
import pathlib

import whisper
from utils.file import get_files
from utils import srt_writer, video2audio, transcriber
from utils.config import CONFIG, init_config
from utils.logger import get_logger

logger = get_logger("main")


def get_srt_filepath(video_file_fullpath: str) -> str:
    vf = pathlib.Path(video_file_fullpath)
    return str(vf.parent.joinpath(f"{vf.stem}.srt"))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    init_config()
    logger.info('get files')
    for target in CONFIG.Targets:
        files = get_files(target.path, target.search_recursive)
        model: whisper.Whisper
        model_loaded: bool = False
        for video_file in files:
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
                                                          verbose=CONFIG.Log.level == logging.DEBUG)
            for segment in segments:
                writer.segment_to_srt1(segment)

            logger.info(f'srt file path: {srt_path}')
            logger.info(f'srt file for {video_file} generated')
            te = datetime.datetime.now()
            logger.debug(f"[DEBUG] transcribe and translate to srt cost: {(te-ts).total_seconds()} seconds")
