import requests
import sys
import urllib.request
import browser_cookie3
from lib.parse.urlParse import urlresolution
from lib.core.log import logger

def request(url, stream = False, headers = None):
    if headers is None:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    elif headers is not None and isinstance(type(headers), dict):
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    if url is not None and url != '':
        return requests.get(url, stream=stream, headers = headers)

def request_cookie(url, set_cookie = False, browser = 'chrome', headers = None):
    if url is not None and url != '':
        parsed_url = urlresolution(url)
        if set_cookie:
            try:
                switch = {
                    'chrome': browser_cookie3.chrome,
                    'firefox': browser_cookie3.firefox,
                    'edge': browser_cookie3.edge
                }
                co = switch.get(browser)
                req_cookie = co() if co else None
            except PermissionError as pe:
                logger.error(f'cookie无法正确读取, 请关闭{browser}浏览器!')
                sys.exit()
            if req_cookie is not None:
                return requests.get(url, cookies = req_cookie)
        return requests.get(url)

def head(url):
    return requests.head(url)


def getContentLength(url, stream = False):
    head_resp = request(url, stream=stream)
    return int(head_resp.headers.get("Content-Length", 0))

def is_enable_proxy():
    proxies = urllib.request.getproxies()
    if len(proxies) > 0:
        return True
    else:
        return False
