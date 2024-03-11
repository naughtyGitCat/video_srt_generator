import datetime
import argparse
import signal
import pathlib
import traceback
import types
import typing

import faster_whisper

from common.objects import ShareObjects
from utils import CONFIG, get_files, get_logger, remove_file
from utils.file import need_translation
from utils import srt_writer, video2audio
from managers.database import DatabaseManager
from managers.web import WebManager
from managers.record import HistoryRecordManager, TranslationRecordManager

logger = get_logger("main")


def init():
    logger.debug(CONFIG)

    ShareObjects.dbm = DatabaseManager()
    ShareObjects.history_record_manager = HistoryRecordManager()
    ShareObjects.translation_record_manager = TranslationRecordManager()

    ShareObjects.current_status = "init"
    ShareObjects.current_srt = ""
    ShareObjects.current_audio = ""

    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)

    if CONFIG.Web.enable:
        WebManager().start()


def handle_exit(sig_num: int, frame: typing.Optional[types.FrameType]) -> None:
    logger.info(f"received signum: {sig_num}, frame: {frame}")
    if ShareObjects.current_status == "transcribe":
        if ShareObjects.current_srt != "":
            logger.info(f"now clean srt file {ShareObjects.current_srt}")
            remove_file(ShareObjects.current_srt)
        if ShareObjects.current_audio != "":
            logger.info(f"now clean audio file {ShareObjects.current_audio}")
            remove_file(ShareObjects.current_audio)
    if ShareObjects.current_status == "video2audio":
        if ShareObjects.current_audio != "":
            logger.info(f"now clean audio file {ShareObjects.current_audio}")
            remove_file(ShareObjects.current_audio)
    logger.info("graceful exit now...")
    exit(0)


def get_srt_filepath(video_file_fullpath: str) -> str:
    vf = pathlib.Path(video_file_fullpath)
    return str(vf.parent.joinpath(f"{vf.stem}.srt"))


def main():
    init()
    logger.info('loop setting targets')
    recorder = HistoryRecordManager()
    translation_record = TranslationRecordManager()
    try:
        logger.info("now looping targets")
        for target in CONFIG.Targets:
            logger.debug(f"now get files in target {target}")
            files = get_files(target)
            model: faster_whisper.WhisperModel
            model_loaded: bool = False
            for video_file in files:
                logger.info(f"loop file in target: {target.path}")
                # if not have srt file, or configured to overwrite
                if need_translation(video_file):
                    if not model_loaded:
                        ShareObjects.current_status = "loading"
                        logger.info(f'loading model: {CONFIG.Whisper.model_name}')
                        model = faster_whisper.WhisperModel(CONFIG.Whisper.model_name,
                                                            device=CONFIG.Whisper.model_device,
                                                            compute_type="int8",
                                                            download_root=CONFIG.Whisper.model_path)
                        model_loaded = True
                    logger.info(f'handle file: {video_file}')
                    recorder.insert(video_file)
                    try:
                        ShareObjects.current_status = "video2audio"
                        ShareObjects.current_audio = video_file
                        recorder.update_status(video_file, "video2audio", "ffmpeg")
                        audio_file = video2audio.video2audio(video_file)
                    except Exception as e:
                        logger.warning(e)
                        recorder.update_status(video_file, "failed", traceback.format_exc())
                        continue

                    try:
                        logger.info(f'now transcribe {audio_file}')

                        srt_path = get_srt_filepath(video_file)
                        ShareObjects.current_status = "transcribe"
                        ShareObjects.current_srt = srt_path
                        recorder.update_status(video_file, "transcribe")
                        writer = srt_writer.SRTWriter(srt_path)

                        ts = datetime.datetime.now()
                        segments, info = model.transcribe(audio_file, language=target.language,
                                                          condition_on_previous_text=True,
                                                          vad_filter=False, suppress_blank=False,
                                                          max_initial_timestamp=88888,
                                                          word_timestamps=True)
                        logger.info(f"Detected language {info.language} with probability {info.language_probability}")
                        recorder.update_status(
                            video_file,
                            "transcribe",
                            f"language: {info.language}, {info.language_probability * 100:.2f}%, duration: {info.duration}s")
                        if CONFIG.Translate.enable is True and CONFIG.Translate.sync is False:
                            translation_record.insert(srt_path)
                        for segment in segments:
                            logger.debug(f"{video_file} segment: {segment}")
                            writer.segment_to_srt1(segment)
                            recorder.update_progress(video_file, segment.start/info.duration)
                        logger.info(f'srt file path: {srt_path}')
                        logger.info(f'srt file for {video_file} generated')
                        te = datetime.datetime.now()
                        logger.debug(f"transcribe and translate to srt cost: {(te - ts).total_seconds()} seconds")
                        recorder.update_status(
                            video_file,
                            "success", f"elapse: {(te - ts).total_seconds()}s, total: {info.duration}s")
                        logger.info(f"now delete tmp audio file {audio_file}")
                        remove_file(audio_file)
                        ShareObjects.current_status = "next"
                        ShareObjects.current_srt = ""
                        ShareObjects.current_audio = ""
                    except Exception as e:
                        logger.warning(e)
                        recorder.update_status(video_file, "failed", traceback.format_exc())
        ShareObjects.current_status = "finish"
    except Exception as e:
        logger.warning(f"run failed {e}")
        logger.info(traceback.format_exc())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
