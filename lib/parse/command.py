import sys

from argparse import ArgumentParser
from argparse import ArgumentError
import argparse
from lib.parse.url_parse import is_url
from lib.core.log import logger
from lib.core.settings import DEFAULT_DOWNLOAD_PATH
from lib.core import shared_variable

from lib.core.settings import IS_WIN

def cmdLineParser(argv=None):
    """
    This function parses the command line parameters and arguments
    """

    if not argv:
        argv = sys.argv

    parser = ArgumentParser()

    try:
        parser.add_argument("-u", "--url", dest="url", default="",
            help="Target URL (e.g. \"http://xxx.com/123.m3u8?sign=xxxx\")")

        parser.add_argument("--name", "--video-name", dest="name",
            help="Video name (e.g. \"001.mp4\")")

        parser.add_argument("--path", "--save-path", dest="path", default = DEFAULT_DOWNLOAD_PATH, type=str,
            help="The path where the video is saved (e.g. \"win: C:/user/video linux or mac: /user/download/video\")")

        parser.add_argument("--site-type", dest="site_type",choices=['bili', 'youtube'],
            help="web size type (e.g. \"bili\" \"youtube\" )")

        parser.add_argument("--batch-file", dest="batch_file_path",
            help="The url file (e.g. \"win: C:/user/video/down.txt linux or mac: /user/download/video/down.csv\")")

        parser.add_argument("--thread", dest="thread", type = int, default = 1,
            help="Thread number  (e.g. \"5\")")

        parser.add_argument("--proxy", nargs='*', dest="proxy",
            help="Network Agent configuration. (e.g. \"http='http://127.0.0.1:8080' https='https://127.0.0.1:8080'\")")

        args = parser.parse_args()
        
        if (args.url is None or args.url == '') and (args.batch_file_path is None or args.batch_file_path == ''):
            parser.print_usage()
            sys.exit()

        if args.url != '' and not is_url(args.url):
            logger.error(f'无效的URL -> [{args.url}]')
            sys.exit()

        params = {}
        if args.proxy is not None and args.proxy != '':
            try:
                for param in args.proxy:
                    key, value = param.split('=')
                    params[key] = value
                    shared_variable.proxy = params
            except Exception as e:
                logger.error('代理参数配置有误，请确认后重新配置!')
                parser.print_help()
                sys.exit()


        return args
    except Exception as e:
        print(e)