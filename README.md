# video_srt_generator 视频字幕生成器
transcribe video srt and translate to custom language 
根据视频中的对话生成srt字幕,并且按需翻译成指定语言

## run 运行
*only test on windows11 + python3.11 + local/smb media*
```bash
git clone https://github.com/naughtyGitCat/video_srt_generator
cd video_srt_generator
pip install -r requirements.txt 
# edit config.py
python main.py
```

## requirements 依赖

### python3
```commandline
python --version >= 3.8
```

### ffmpeg
better to use `ffmpeg-full` than `ffmpeg`
推荐使用ffmpeg-full版本

you can download from https://www.ffmpeg.org/download.html
or use following command
```bat
# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg
```

### openai-whisper
```commandline
pip install -U openai-whisper
```
#### language model, GPU, speed 模型与GPU显存和速度

during cut a 1min10s video and transcribe to audio
* (smb means: 1000MB cable smb)
* (CPU: default FP32 only)
* (model: medium)

|round| i5-12400 | RTX 3090 | translate |
| --  |----------|----------|-----------|
|1| 75.4s    | 28.4s    | Y         |
|2| 73.4s    | 28.9s    | Y         |
|3| 74.9s    | 25.12s   | Y         |




### Thanks to 感谢
* https://github.com/openai/whisper
* https://www.spapas.net/2023/05/22/ai-auto-subtitling/
* https://github.com/ggerganov/whisper.cpp