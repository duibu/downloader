from lib.core.common import banner
from lib.parse.command import cmdLineParser
from lib.parse.typeParse import parseType
from lib.core.m3u8download import downloadm3u8


if __name__ == '__main__':
    banner()
    args = cmdLineParser()
    video_type = parseType(args.url)
    if video_type == 'm3u8':
        downloadm3u8(args.url, '123')
    print('url is ' + args.url)