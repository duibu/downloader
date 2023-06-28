from lib.core.settings import IS_WIN
from lib.core.settings import IS_LINUX
from lib.core.settings import ABS_PATH

import subprocess
import os


def merge(files, tsfilepath, muxFormat, fastStart, OutPutPath, poster="", audioName="", title="",
          copyright="", comment="", encodingTool=""):
    UseAACFilter = False
    # dateString = REC_TIME if REC_TIME else datetime.datetime.now().isoformat()

    # Coexistence strategy for already existing files with the same name
    # if os.path.exists(f"{OutPutPath}.{muxFormat.lower()}"):
    #     base_name = os.path.basename(OutPutPath)
    #     dir_name = os.path.dirname(OutPutPath)
    #     OutPutPath = os.path.join(dir_name, f"{base_name}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")

    command = "-loglevel warning -i concat:"
    ddpAudio = ""
    addPoster = "-map 1 -c:v:1 copy -disposition:v:1 attached_pic"

    ddp_audio_file = f"{os.path.splitext(OutPutPath + '.mp4')[0]}.txt"
    if os.path.exists(ddp_audio_file):
        with open(ddp_audio_file, "r") as f:
            ddpAudio = f.read()
    if ddpAudio:
        UseAACFilter = False

    for t in files:
        command += t + "|"


    switcher = {
        "MP4": lambda: command + " " + (('-i \"' + poster + '\"') if poster else '') +
                       (" -i \"" + ddpAudio + "\"" if ddpAudio else '') +
                       " -map 0:v? " +
                       (" -map 0:a?" if not ddpAudio else (' -map ' + ('1' if not poster else '2') +
                                                              ':a -map 0:a?')) +
                       " -map 0:s? " + (' ' + addPoster if poster else '') +
                    #    (" -metadata date=\"2023-01-01\"" if False else '') +
                       " -metadata encoding_tool=\"" + encodingTool + "\"" +
                       " -metadata title=\"" + title + "\"" +
                       " -metadata copyright=\"" + copyright + "\"" +
                       " -metadata comment=\"" + comment + "\"" +
                       " -metadata:s:a:" + ('0' if not ddpAudio else '1') +
                       " handler_name=\"" + audioName + '\"' +
                       " -metadata:s:a:" + ('0' if not ddpAudio else '1') +
                       " handler=\"" + audioName + '\"' +
                       (" -metadata:s:a:0 handler_name=\"DD+\" -metadata:s:a:0 handler=\"DD+\"" if ddpAudio else '') +
                       (" -movflags +faststart" if fastStart else '') +
                       (" -c copy -y " + ('-bsf:a aac_adtstoasc' if UseAACFilter else '') +
                       " " + OutPutPath + ".mp4"),
        "MKV": lambda: command + " -map 0 -c copy -y " + ('-bsf:a aac_adtstoasc' if UseAACFilter else '') +
                       " " + OutPutPath + ".mkv",
        "FLV": lambda: command + " -map 0 -c copy -y " + ('-bsf:a aac_adtstoasc' if UseAACFilter else '') +
                       " " + OutPutPath + ".flv",
        "TS": lambda: command + " -map 0 -c copy -y -f mpegts -bsf:v h264_mp4toannexb" +
                       " " + OutPutPath + ".ts",
        "VTT": lambda: command + " -map 0 -y " + OutPutPath + ".srt",
        "EAC3": lambda: command + " -map 0:a -c copy -y " + OutPutPath + outputname + ".eac3",
        "AAC": lambda: command + " -map 0:a -c copy -y " + OutPutPath + outputname + ".m4a",
        "AC3": lambda: command + " -map 0:a -c copy -y " + OutPutPath + outputname + ".ac3",
    }

    ffmpeg_path = getFFmpegPath()
    command_builder = switcher.get(muxFormat.upper())
    if command_builder:
        command = command_builder()
        subprocess.call([ffmpeg_path] + command.split(), cwd=tsfilepath)


def getFFmpegPath():
    if IS_WIN:
        return ABS_PATH + '\\ffmpeg\\win\\ffmpeg'
    elif IS_LINUX:
        return ABS_PATH + '/ffmpeg/linux/ffmpeg'

