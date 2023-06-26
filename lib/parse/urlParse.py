from urllib.parse import urlparse, parse_qs

def urlresolution(url):
    parsed_url = urlparse(url)
    return parsed_url


def queryParamsParse(url):
    parsed_url = urlresolution(url)
    query_params = parse_qs(parsed_url.query)
    return query_params
