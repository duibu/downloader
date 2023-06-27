from urllib.parse import urlparse, parse_qs

def urlresolution(url):
    parsed_url = urlparse(url)
    return parsed_url


def queryParamsParse(url):
    parsed_url = urlresolution(url)
    query_params = parse_qs(parsed_url.query)
    return query_params

def getBaseUrl(url):
    parsed_url = urlresolution(url)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
    return base_url

def getm3u8BaseUrl(url):
    parsed_url = urlresolution(url)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
    index = base_url.rfind('/')
    result = ""
    if index != -1:
        result = base_url[:index+1]
    return result