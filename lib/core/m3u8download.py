import requests

from lib.parse.m3u8Parse import getM3u8KeyUri

def downloadm3u8(url):
    resp = requests.get(url)
    m3u8_content = resp.text
    # print(m3u8_content)
    return m3u8_content


def getm3u8key(url):
    resp = requests.get(url)
    key = resp.content
    print("m2u8 key is ", key)
    return key