import re
import json

from lib.core.files import writeTextFile

def getM3u8KeyUri(m3u8_content):
    pattern = r'#EXT-X-KEY:(METHOD=[^,]+),URI="([^"]+)"(?:,IV=([0-9A-Fa-f]+))?'
    match = re.search(pattern, m3u8_content)
    if match:
        key_uri = match.group(2)
        return key_uri


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
        iv = match.group(3)
        return iv

def m3u8ToJson(m3u8_content, key):
    iv = getM3u8Iv(m3u8_content)
    method = getM3u8Method(m3u8_content)
    lines = m3u8_content.split("\n")
    data = {"segments": []}
    
    index = 0

    for line in lines:
        line = line.strip()
        pattern = r'#EXTINF:(\d+\.\d+),'
        seg = {"index": index, "method": method, "iv": iv}
        if re.match(pattern, line):

        data["segments"].append(line)
        index++

    json_data = json.dumps(data)
    print(json_data)

def saveM3u8Meta(metajson, filePath, filename):
    writeTextFile(filename, filePath, metajson)

