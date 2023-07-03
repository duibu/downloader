import requests
import urllib.request
import browser_cookie3
from lib.parse.urlParse import urlresolution

def request(url, stream = False, headers = None):
    if url is not None and url != '':
        return requests.get(url, stream=stream, headers = headers)

def request_cookie(url, set_cookie = False, browser = 'chrome'):
    if url is not None and url != '':
        parsed_url = urlresolution(url)
        if set_cookie:
            switch = {
                'chrome': browser_cookie3.chrome,
                'firefox': browser_cookie3.firefox,
                'edge': browser_cookie3.edge
            }
            co = switch.get(browser)
            req_cookie = co() if co else None
            if req_cookie is not None:
                return requests.get(url, cookies = req_cookie)
        return requests.get(url)

def head(url):
    return requests.head(url)

def is_enable_proxy():
    proxies = urllib.request.getproxies()
    if len(proxies) > 0:
        return True
    else:
        return False
