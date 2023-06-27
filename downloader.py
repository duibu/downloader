from lib.core.common import banner
from lib.parse.command import cmdLineParser
from lib.parse.typeParse import parseType
from lib.core.m3u8download import downloadm3u8
from lib.core.m3u8download import getm3u8key
from lib.core.m3u8download import downloadM3u8Ts
from lib.parse.m3u8Parse import m3u8ToJson
from lib.parse.m3u8Parse import getM3u8KeyUri
from lib.parse.urlParse import getm3u8BaseUrl
from lib.core.log import logger
from lib.core.convert import tsToMp4
from lib.core.convert import tsToMp4forffmpeg
from lib.core.useparameter import getTmpPath
from lib.core.useparameter import numlen
from lib.core.useparameter import numformat
from lib.core.threads import thread
from tqdm import tqdm
import multiprocessing

import json


if __name__ == '__main__':
    count = multiprocessing.Value('i', 0)
    def increment_count():
        with count.get_lock():
            count.value += 1
    banner()
    args = cmdLineParser()
    url = args.url
    name = args.name
    path = args.path
    thread_num = int(args.thread)
    video_type = parseType(args.url)
    if video_type == 'm3u8':
        baseUrl = getm3u8BaseUrl(url)
        m3u8_ori_content = downloadm3u8(url)
        key_uri = getM3u8KeyUri(m3u8_ori_content)
        key = getm3u8key(key_uri)
        m3u8Json = m3u8ToJson(baseUrl, m3u8_ori_content, key)
        json_data = json.loads(m3u8Json)
        seg = json_data['segments']
        pbar = tqdm(total=len(seg))
        filepath = getTmpPath(path, name)

        def merge():
            pbar.close()
            # tsToMp4(tsfilepath = filepath, outputname = name, outputpath = path)
            tsToMp4forffmpeg(tsfilepath = filepath, outputname = name, outputpath = path)

        def pbarUp():
            pbar.update(1)
            increment_count()
            if count.value == json_data['count']:
                merge()

        countlen = numlen(json_data['count'])

        if thread_num is not None and thread_num > 1:
            thread_down = thread(num_threads = thread_num)
            for s in seg:
                thread_down.downloadts(s['url'], s['key'], s['iv'], numformat(s['index'], countlen), s['method'], filepath, pbarUp())
            thread_down.wait_completion()
        else:
            for s in seg:
                downloadM3u8Ts(s['url'], s['key'], s['iv'], numformat(s['index'], countlen), s['method'], filepath)
                pbar.update(1)
            merge()
    
        
