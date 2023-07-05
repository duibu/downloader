import sys

from argparse import ArgumentParser
from argparse import ArgumentError
from argparse import SUPPRESS

from lib.core.settings import IS_WIN

def parse_key_value_pair(pair):
    key = pair.split(":")[0]
    value = pair
    return {key,value}

def cmdLineParser(argv=None):
    """
    This function parses the command line parameters and arguments
    """

    if not argv:
        argv = sys.argv

    # Reference: https://stackoverflow.com/a/4012683 (Note: previously used "...sys.getfilesystemencoding() or UNICODE_ENCODING")
    # _ = getUnicode(os.path.basename(argv[0]), encoding=sys.stdin.encoding)

    usage = "python downloader.py -u http://xxx.com/123.m3u8 [options]"
    parser = ArgumentParser(usage=usage)

    try:
        parser.add_argument("-u", "--url", dest="url",
            help="Target URL (e.g. \"http://xxx.com/123.m3u8?sign=xxxx\")")

        parser.add_argument("-t", "--thread", dest="thread", type = int, default = 1,
            help="Thread number  (e.g. \"5\")")

        parser.add_argument("-name", "--video-name", dest="name",
            help="Video name (e.g. \"001.mp4\")")

        parser.add_argument("-site", "--site-type", dest="site_type",
            help="web size type (e.g. \"bili\" \"youtube\" )")

        parser.add_argument("-path", "--save-path", dest="path", default = './',
            help="The path where the video is saved (e.g. \"win: C:/user/video linux or mac: /user/download/video\")")

        parser.add_argument("--batch-file", dest="batch_file_path",
            help="The url file (e.g. \"win: C:/user/video/down.txt linux or mac: /user/download/video/down.csv\")")

        # parser.add_argument("--cookie", dest="http_cookie",
        #     help="http request cookie header. (e.g. \"xxx:xxx;xxx:xxx\")")

        parser.add_argument("--proxy", nargs='*', dest="proxy", type=parse_key_value_pair,
            help="Network Agent configuration. (e.g. \"http://127.0.0.1:8080\")")

        args = parser.parse_args()
        # if args.proxy is not None:
        #     for a in args.proxy:
        #         proxy[a[:a[':']]] = a
        #     args.proxy = proxy
        return args
    except Exception as e:
        print(e)