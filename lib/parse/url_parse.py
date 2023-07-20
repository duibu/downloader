from urllib.parse import urlparse, parse_qs
import re

def urlresolution(url):
    parsed_url = urlparse(url)
    return parsed_url

def url_path(url):
    parsed_url = urlresolution(url)
    return parsed_url.path

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

def is_url(url):
    url_regex = re.compile(
        r'^(?:http|ftp)s?://'  # 协议
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # 域名
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP地址
        r'(?::\d+)?'  # 端口号
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)  # 路径和查询参数

    return url_regex.match(url)