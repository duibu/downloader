import re


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

def saveM3u8Meta(m3u8_content, filePath):

