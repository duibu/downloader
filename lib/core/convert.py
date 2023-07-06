from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
from lib.core.ffmpeg import merge
from lib.core.ffmpeg import audio_video_merge
from lib.core.log import logger
from lib.core.files import file_exists


def tsToMp4(tsfilepath, outputname, outputpath):
    # 找到所有的 TS 文件，并转换为 VideoFileClip 对象
    ts_files = sorted([f for f in os.listdir(tsfilepath) if f.endswith('.ts')])
    clips = [VideoFileClip(os.path.join(tsfilepath, f)) for f in ts_files]

    # 将所有的 VideoFileClip 对象连接成一个片段，并写入 MP4 文件
    try:
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(outputpath + outputname)
    except Exception as e:
        print(e)
    finally:
        final_clip.close()

def tsToMp4forffmpeg(tsfilepath, outputpath, outputname):
    ts_files = sorted([f for f in os.listdir(tsfilepath) if f.endswith('.ts')])
    logger.info('The FFMPEG conversion begins ......')
    merge(ts_files, tsfilepath, "MP4", True, outputpath + outputname)

def m4s_merge_for_ffmpeg(tsfilepath, outputpath, outputname):
    ts_files = sorted([f for f in os.listdir(tsfilepath) if f.endswith('.m4s')])
    logger.info('The FFMPEG conversion begins ......')
    merge(ts_files, tsfilepath, "MP4", True, outputpath + outputname + '_v')

def m4s_audio_video_merge(tsfilepath, outputpath, outputname):
    logger.info('The FFMPEG conversion begins ......')
    audio_video_merge(f'{outputname}_v.m4s' if file_exists(outputpath + outputname + '_v.m4s') else f'{outputname}_v.mp4', f'{outputname}_a.m4s', tsfilepath, "MP4", True, outputpath + outputname)

def getUnicode(value, encoding=None, noneToNull=False):
    """
    Returns the unicode representation of the supplied value

    >>> getUnicode('test') == u'test'
    True
    >>> getUnicode(1) == u'1'
    True
    >>> getUnicode(None) == 'None'
    True
    """

    if noneToNull and value is None:
        return NULL

    if isinstance(value, six.text_type):
        return value
    elif isinstance(value, six.binary_type):
        # Heuristics (if encoding not explicitly specified)
        candidates = filterNone((encoding, kb.get("pageEncoding") if kb.get("originalPage") else None, conf.get("encoding"), UNICODE_ENCODING, sys.getfilesystemencoding()))
        if all(_ in value for _ in (b'<', b'>')):
            pass
        elif any(_ in value for _ in (b":\\", b'/', b'.')) and b'\n' not in value:
            candidates = filterNone((encoding, sys.getfilesystemencoding(), kb.get("pageEncoding") if kb.get("originalPage") else None, UNICODE_ENCODING, conf.get("encoding")))
        elif conf.get("encoding") and b'\n' not in value:
            candidates = filterNone((encoding, conf.get("encoding"), kb.get("pageEncoding") if kb.get("originalPage") else None, sys.getfilesystemencoding(), UNICODE_ENCODING))

        for candidate in candidates:
            try:
                return six.text_type(value, candidate)
            except (UnicodeDecodeError, LookupError):
                pass

        try:
            return six.text_type(value, encoding or (kb.get("pageEncoding") if kb.get("originalPage") else None) or UNICODE_ENCODING)
        except UnicodeDecodeError:
            return six.text_type(value, UNICODE_ENCODING, errors="reversible")
    elif isListLike(value):
        value = list(getUnicode(_, encoding, noneToNull) for _ in value)
        return value
    else:
        try:
            return six.text_type(value)
        except UnicodeDecodeError:
            return six.text_type(str(value), errors="ignore")