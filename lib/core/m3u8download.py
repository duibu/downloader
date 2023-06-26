import requests
import base64

from lib.parse.m3u8Parse import getM3u8KeyUri

def downloadm3u8(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        m3u8_content = resp.text
    # print(m3u8_content)
        return m3u8_content


def getm3u8key(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        key = base64.b64encode(resp.content).decode('utf-8')
        print("m2u8 key is ", key)
        return key