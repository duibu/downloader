from moviepy.editor import VideoFileClip, concatenate_videoclips
import ffmpeg
import glob
import os


def tsToMp4(tsfilepath, outputname, outputpath):
    # 找到所有的 TS 文件，并转换为 VideoFileClip 对象
    ts_files = sorted([f for f in os.listdir(tsfilepath) if f.endswith('.ts')])
    clips = [VideoFileClip(os.path.join(tsfilepath, f)) for f in ts_files]

    # 将所有的 VideoFileClip 对象连接成一个片段，并写入 MP4 文件
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(outputpath + outputname)

def tsToMp4forffmpeg(tsfilepath, outputpath, outputname):
    # ts_files = sorted([f for f in os.listdir(tsfilepath) if f.endswith('.ts')])
    ts_files = sorted(glob.glob(tsfilepath+'*.ts')) 
    # input_args = ffmpeg.input(ts_files[0])
    # for ts_file in ts_files[1:]:
    #     input_args = input_args.input(ts_file)
    # # 创建输出命令
    # output_args = ffmpeg.output(input_args, outputname, vcodec='copy', acodec='copy')
    # # 执行命令
    # ffmpeg.run(output_args)
    try:
        input_args = ffmpeg.input(ts_files[0])
    except ValueError as e:
        print(f"无法设置输入流：{e}")
        return
    
    for ts_file in ts_files[1:]:
        try:
            input_args = input_args.concat(ffmpeg.input(ts_file), n=len(ts_files))
        except ValueError as e:
            print(f"无法添加输入文件 {ts_file}：{e}")
            continue
    
    # 设置 ffmpeg 输出流(.mp4 文件)
    output_args = ffmpeg.output(input_args, outputpath + outputname, c="copy", bsf="a")
    print(output_args.get_args()) # 调试信息
    output_args.run()

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