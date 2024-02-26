# video_srt_generator 视频字幕生成器
transcribe video srt and translate to custom language 
根据视频中的对话生成srt字幕,并且按需翻译成指定语言

## run 运行

### config 配置
please customize you setting in `config.toml`
请在`config.toml`中进行自定义设置

### linux
*tested on debian12 + python3.11 + (smb mounted as cifs) media*
```sh
apt install nvidia-cudnn
```
**please mount smb share by cifs as a local path, and add the mounted path as `local` in `config.toml`**

请将smb共享挂载到linux的目录上, 在配置文件中以local的类型设置

### windows
*tested on windows11 + python3.11 + local/smb media*

**please provide the smb share user/pass in `config.toml` if the user/pass is not stored in windows,**
**or  is running in remote pwsh connection， even if the share user/pass is set/stored in gui**

如果系统中没有保存文件的共享账户密码,请在配置文件中提供。如果时同pwsh远程连接执行的本脚本，虽然系统已经保存了共享账户密码，但仍需要在配置文件中提供

```bash
git clone https://github.com/naughtyGitCat/video_srt_generator
cd video_srt_generator
pip install -r requirements.txt 
# edit config.py
python main.py
```

## requirements 依赖

### python3
```
python --version >= 3.11
```

### ffmpeg
better to use `ffmpeg-full` than `ffmpeg`

推荐使用ffmpeg-full版本

you can download from https://www.ffmpeg.org/download.html
or use following command
```bat
# on Windows using Chocolatey (https://chocolatey.org/) or wget
choco install ffmpeg
wget install ffmpeg
```

```shell
apt install ffmpeg
dnf install ffmpeg
```

### openai-whisper
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
* https://stackoverflow.com/questions/66977227/could-not-load-dynamic-library-libcudnn-so-8-when-running-tensorflow-on-ubun
* https://github.com/guillaumekln/faster-whisper

### TODO

#### when file size change, overwrite srt generate 
- https://stackoverflow.com/questions/16874598/how-do-i-calculate-the-md5-checksum-of-a-file-in-python

### translate existed srt file
> merge all lines, translate by paragraph, split to lines
- https://pypi.org/project/srt/
- https://github.com/byroot/pysrt

### when use remote file system, write srt tmp file to local, move back final srt to remote
- https://stackoverflow.com/questions/25283882/determining-the-filesystem-type-from-a-path-in-python
