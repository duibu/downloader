
from lib.core.log import logger
from lib.request.http_request import request

from lib.core.files import newdir
from lib.core.progressbar import get_progress_bar

def downloadM4s(url, start, end, name, filepath, progress_bar):
    newdir(filepath)
    headers = {"Range": f"bytes={start}-{end}"}
    response = request(url, stream = True, headers = headers)
    with open(filepath + str(name) + '.m4s', 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)
            progress_bar.update(len(chunk))

def single_download(download_url, download_video_path, enable_progress_bar=True, block_size=1024):
    response = request(download_url, stream=True)
    file_size = int(response.headers.get("Content-Length", 0))
    if enable_progress_bar:
        progress_bar = get_progress_bar(file_size)
    with open(download_video_path, "wb") as file:
        for data in response.iter_content(block_size):
            if enable_progress_bar:
                progress_bar.update(len(data))
            file.write(data)
            
    if enable_progress_bar:
        progress_bar.close()
