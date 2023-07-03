import requests
from lib.core.log import logger
from lib.request.httprequest import request

from lib.parse.m3u8Parse import getM3u8KeyUri
from lib.core.files import newdir

def downloadM4s(url, start, end, name, filepath, progress_bar):
    newdir(filepath)
    headers = {"Range": f"bytes={start}-{end}"}
    response = request(url, stream = True, headers = headers)
    with open(filepath + str(name) + '.m4s', 'wb') as f:
        # f.seek(start)
        for chunk in response.iter_content(end - start):
            # print(chunk)
            f.write(chunk)
            progress_bar.update(len(chunk))