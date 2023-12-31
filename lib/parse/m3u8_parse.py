import re
import json
import base64
import sys

from lib.core.files import writeTextFile
from lib.core.log import logger
from lib.parse.url_parse import is_url

def getM3u8KeyUri(m3u8_content):
    pattern = r'#EXT-X-KEY:(METHOD=[^,]+),URI="([^"]+)"(?:,IV=([0-9A-Fa-f]+))?'
    try:
        match = re.search(pattern, m3u8_content)
        if match:
            key_uri = match.group(2)
            return key_uri
    except TypeError as te:
        logger.error('请检查链接是否正确')
        sys.exit(0)


def getM3u8Method(m3u8_content):
    pattern = r'#EXT-X-KEY:(METHOD=[^,]+),URI="([^"]+)"(?:,IV=([0-9A-Fa-f]+))?'
    match = re.search(pattern, m3u8_content)
    if match:
        # 获取密钥相关信息
        method = match.group(1).split('=')[1]
        return method


def getM3u8Iv(m3u8_content):
    pattern = r'#EXT-X-KEY:(METHOD=[^,]+),URI="([^"]+)"(?:,IV=([0-9A-Fa-f]+))?'
    match = re.search(pattern, m3u8_content)
    if match:
        result = ''
        iv = match.group(3)
        if iv is not None and iv != '0':
            iv = bytes.fromhex(iv)
        else:
            iv = b'\x00'*16

        return base64.b64encode(iv).decode('utf-8')

def m3u8ToJson(baseUrl, m3u8_content, key = ''):
    iv = getM3u8Iv(m3u8_content)
    method = getM3u8Method(m3u8_content)
    lines = m3u8_content.split("\n")
    data = {"segments": []}
    
    index = 0
    flag = False
    video_length = 0.0
    
    for line in lines:
        seg = {"method": method, "iv": iv, "key": key}
        seg["index"] = index
        line = line.strip()
        pattern = r'#EXTINF:(\d+\.\d+),'
        if re.match(pattern, line):
            duration = float(re.findall(pattern, line)[0])
            seg["duration"] = duration
            video_length += duration
            flag = True
            continue
        elif line.startswith("#"):
            continue
        
        if flag:
            if is_url(line):
                seg["url"] = line
            else:
                seg["url"] = baseUrl + line
            data["segments"].append(seg)
            index += 1
            flag = False
    data["durationCount"] = video_length
    data["count"] = index
    json_data = json.dumps(data, indent=4)
    return json_data

def saveM3u8Meta(metajson, filePath, filename):
    writeTextFile(filename, filePath, metajson)

