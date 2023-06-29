# 20230619
# copy from whisper.utils, with some translate and smb modifies
import os
import sys
import time
from typing import TextIO

from utils import translator
from utils import CONFIG
from utils import get_logger

logger = get_logger("srt")

system_encoding = sys.getdefaultencoding()

if system_encoding != "utf-8":

    def make_safe(string):
        # replaces any character not representable using the system default encoding with an '?',
        # avoiding UnicodeEncodeError (https://github.com/openai/whisper/discussions/729).
        return string.encode(system_encoding, errors="replace").decode(system_encoding)

else:

    def make_safe(string):
        # utf-8 can encode any Unicode code point, so no need to do the round-trip encoding
        return string


def format_timestamp(
    seconds: float, always_include_hours: bool = False, decimal_marker: str = "."
):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
    return (
        f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"
    )


class ResultWriter:
    extension: str

    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def __call__(self, result: dict, video_name: str):
        video_basename = os.path.basename(video_name)
        video_basename = os.path.splitext(video_basename)[0]
        output_path = os.path.join(
            self.output_dir, video_basename + "." + self.extension
        )

        with open(output_path, "w", encoding="utf-8") as f:
            self.write_result(result, file=f)

    def write_result(self, result: dict, file: TextIO):
        raise NotImplementedError


class SubtitlesWriter(ResultWriter):
    always_include_hours: bool
    decimal_marker: str

    def iterate_result(self, result: dict):
        for segment in result["segments"]:
            segment_start = self.format_timestamp(segment["start"])
            segment_end = self.format_timestamp(segment["end"])
            segment_text = segment["text"].strip().replace("-->", "->")

            if word_timings := segment.get("words", None):
                all_words = [timing["word"] for timing in word_timings]
                all_words[0] = all_words[0].strip()  # remove the leading space, if any
                last = segment_start
                for i, this_word in enumerate(word_timings):
                    start = self.format_timestamp(this_word["start"])
                    end = self.format_timestamp(this_word["end"])
                    if last != start:
                        yield last, start, segment_text

                    yield start, end, "".join(
                        [
                            f"<u>{word}</u>" if j == i else word
                            for j, word in enumerate(all_words)
                        ]
                    )
                    last = end

                if last != segment_end:
                    yield last, segment_end, segment_text
            else:
                yield segment_start, segment_end, segment_text

    def format_timestamp(self, seconds: float):
        return format_timestamp(
            seconds=seconds,
            always_include_hours=self.always_include_hours,
            decimal_marker=self.decimal_marker,
        )


class WriteSRT(SubtitlesWriter):
    extension: str = "srt"
    always_include_hours: bool = True
    decimal_marker: str = ","

    def write_result(self, result: dict, file: TextIO):
        for i, (start, end, text) in enumerate(self.iterate_result(result), start=1):
            # if choose do translate
            if CONFIG.Translate.enable:
                translated_text = translator.translate(text)
                if CONFIG.Srt.bilingual:
                    # generate bilingual text
                    translated_text = f"{text}\n{translated_text}"
                text = translated_text
                time.sleep(0.5)  # Too Many Requests for url
            print(f"{i}\n{start} --> {end}\n{text}\n", file=file, flush=True)


def get_srt_writer(output_dir: str) -> any:
    return WriteSRT(output_dir)


class SRTWriter:
    _srt_path: str
    _srt_file: any
    always_include_hours: bool = True
    decimal_marker: str = ","
    line_number: int = 1

    def __init__(self, srt_fullpath: str):
        self._srt_path = srt_fullpath
        self._srt_file = open(self._srt_path, 'w', encoding='utf-8')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._srt_file.close()

    def format_timestamp(self, seconds: float):
        return format_timestamp(
            seconds=seconds,
            always_include_hours=self.always_include_hours,
            decimal_marker=self.decimal_marker,
        )

    def segment_to_srt(self, segment: dict):
        with open(self._srt_path, "w", encoding="utf-8") as f:
            segment_start = self.format_timestamp(segment["start"])
            segment_end = self.format_timestamp(segment["end"])
            segment_text = segment["text"].strip().replace("-->", "->")
            if CONFIG.Translate.enable:
                translated_text = translator.translate(segment_text)
                logger.debug(f"{segment_start} --> {segment_end} {translated_text}")
                if CONFIG.Srt.bilingual:
                    # generate bilingual text
                    translated_text = f"{segment_text}\n{translated_text}"
                segment_text = translated_text
                time.sleep(0.3)  # Too Many Requests for url
            print(f"{self.line_number}\n{segment_start} --> {segment_end}\n{segment_text}\n", file=f, flush=True)
        self.line_number += 1

    def segment_to_srt1(self, segment: dict):
        segment_start = self.format_timestamp(segment["start"])
        segment_end = self.format_timestamp(segment["end"])
        segment_text = segment["text"].strip().replace("-->", "->")
        if CONFIG.Translate.enable:
            translated_text = translator.translate(segment_text)
            logger.debug(f"{segment_start} --> {segment_end} {translated_text}")
            if CONFIG.Srt.bilingual:
                # generate bilingual text
                translated_text = f"{segment_text}\n{translated_text}"
            segment_text = translated_text
            time.sleep(0.3)  # Too Many Requests for url
        print(f"{self.line_number}\n{segment_start} --> {segment_end}\n{segment_text}\n", file=self._srt_file, flush=True)
        self.line_number += 1

