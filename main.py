import os
import pathlib

import whisper
import video2audio
import config
from file import get_files, remove_file
import pprint
from whisper.utils import get_writer

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('get files')
    files = get_files(config.Config.media_path, config.Config.search_recursive)

    model: whisper.Whisper
    model_loaded: bool = False
    for video_file in files:
        if not model_loaded:
            print('load model')
            model = whisper.load_model(config.Config.model)
            model_loaded = True
        print(f'do file: {video_file}')
        audio_file = video2audio.video2audio(video_file)

        print(f'now transcribe {audio_file}')
        result = model.transcribe(audio_file, language=None, verbose=config.Config.verbose)
        remove_file(audio_file)
        writer = get_writer('srt', str(pathlib.Path(video_file).parent))
        writer(result, video_file)
        print(pprint.pprint(result))
        break

# See PyCharm help at https://www.jetbrains.com/help/pycharm/