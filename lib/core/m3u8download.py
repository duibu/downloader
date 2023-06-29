import requests
import base64
from Crypto.Cipher import AES
from Crypto.Util import Padding
from lib.core.log import logger
from lib.request.httprequest import request

from lib.parse.m3u8Parse import getM3u8KeyUri
from lib.core.files import newdir

def downloadm3u8(url):
    logger.info('获取m3u8流信息')
    resp = request(url)
    if resp.status_code == 200:
        m3u8_content = resp.text
    # print(m3u8_content)
        return m3u8_content
    # else:
    #     return resp


def getm3u8key(url):
    logger.info('获取Key')
    resp = request(url)
    if resp.status_code == 200:
        key = base64.b64encode(resp.content).decode('utf-8')
        return key


def downloadM3u8Ts(url, key, iv, name, method, filepath):
    newdir(filepath)
    response = request(url)
    # decrypt ts stream
    if key is not None and key != '':
        cipher = AES.new(base64.b64decode(key), AES.MODE_CBC, IV=bytes.fromhex(base64.b64decode(iv).hex()[:32]))
        decrypted_content = cipher.decrypt(response.content)
    else:
        decrypted_content = response.content
    # unpadded_plaintext = Padding.unpad(decrypted_content, AES.block_size, style='pkcs7')
    with open(filepath + str(name) + '.ts', 'wb') as f:
        f.write(decrypted_content)