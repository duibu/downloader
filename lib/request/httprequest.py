import requests
import sys
import urllib.request
import browser_cookie3
from lib.parse.urlParse import urlresolution
from lib.core.log import logger
from lib.core import shared_variable

def request(url, stream = False, headers = None, proxy = None):
    if proxy is None and shared_variable.proxy is not None:
        proxy = shared_variable.proxy
    if headers is None:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    elif headers is not None and isinstance(type(headers), dict):
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    else:
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    if url is not None and url != '':
        return checkResponse(requests.get(url, stream=stream, headers = headers, proxies = proxy))
        

def request_cookie(url, set_cookie = False, browser = 'chrome', headers = None, proxy = None):
    if proxy is None and shared_variable.proxy is not None:
        proxy = shared_variable.proxy
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
                return checkResponse(requests.get(url, cookies = req_cookie, proxies=proxy))
        return checkResponse(requests.get(url, proxies=proxy))

def head(url):
    return checkResponse(requests.head(url))


def getContentLength(url, stream = False):
    head_resp = request(url, stream=stream)
    return int(head_resp.headers.get("Content-Length", 0))

def is_enable_proxy():
    proxies = urllib.request.getproxies()
    if len(proxies) > 0:
        return True
    else:
        return False

def checkResponse(resp):
    if resp.status_code in [200, 206]:
        return resp
    elif resp.status_code == 403:
        logger.error('没有相应的权限!')
        sys.exit()
    elif resp.status_code == 404:
        logger.error('url错误或资源不存在，请检查url是否正确!')
        sys.exit()
    elif resp.status_code == 500:
        logger.error('请求的服务器内部发生错误!')
        sys.exit()