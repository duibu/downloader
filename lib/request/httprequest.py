import requests
import urllib.request

def request(url):
    if url is not None and url != '':
        proxies = {
            "http": None,
            "https": None
        }
        return requests.get(url, proxies = proxies)


def is_enable_proxy():
    proxies = urllib.request.getproxies()
    if len(proxies) > 0:
        return True
    else:
        return False
