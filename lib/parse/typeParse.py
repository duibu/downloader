from lib.parse.urlParse import urlresolution
from lib.core.log import logger
from lib.request.httprequest import requests

def parseType(url):
    parsed_url = urlresolution(url)
    # 获取URL的主体（不包括查询参数）
    base_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path

    if base_url.endswith(".m3u8"):
        logger.info('视频类型为: m3u8')
        return 'm3u8'
    else:
        # Try to parse the video stream content
        res = requests.get(url)
        if len(res.content.split(b".m4s")) > 1:
            return ".m4s"
        else:
            return ''