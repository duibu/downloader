from lib.core.common import banner
from lib.parse.command import cmdLineParser
from lib.parse.typeParse import parseType
from lib.core.m3u8download import downloadm3u8
from lib.core.m3u8download import getm3u8key
from lib.parse.m3u8Parse import m3u8ToJson
from lib.parse.m3u8Parse import getM3u8KeyUri


if __name__ == '__main__':
    banner()
    args = cmdLineParser()
    video_type = parseType(args.url)
    if video_type == 'm3u8':
        m3u8_ori_content = downloadm3u8(args.url)
        key_uri = getM3u8KeyUri(m3u8_ori_content)
        key = getm3u8key(key_uri)
        print(m3u8_ori_content)
        m3u8Json = m3u8ToJson(m3u8_ori_content, key)
        print(m3u8Json)
        print('key is ',key)


    print('url is ' + args.url)