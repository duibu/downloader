from lib.core.common import banner
from lib.parse.command import cmdLineParser
from lib.core.log import logger
from lib.parse.typeParse import parseType
from lib.core.download import download_m3u8_video
from lib.core.download import download_bili
from lib.core.files import file_exists
from lib.core.files import file_is_txt
from lib.core.files import file_is_csv
from lib.core.files import read_csv
from lib.core.files import read_txt
from lib.core import shared_variable

import requests

def main():
    banner()
    args = cmdLineParser()
    url = args.url
    video_name = args.name
    video_save_path = args.path if args.path.endswith('/') else args.path + '/'
    thread_num = int(args.thread)
    batch_file_path = args.batch_file_path
    site_type = args.site_type
    print(args.proxy)
    shared_variable.proxy = args.proxy
    if site_type == 'bili':
        download_bili(url=url, video_save_path = video_save_path, video_name=video_name,thread_num=thread_num)
        return

    if (url is None or url == '') and (batch_file_path is None or batch_file_path == ''):
        logger.error("")
    if batch_file_path is not None and batch_file_path != '':
        batch_download(batch_file_path, video_save_path, thread_num)
    else:
        singleDownload(url,video_save_path,thread_num,video_name)

def singleDownload(url, video_save_path, thread_num, video_name = None):
    logger.info(f"开始解析 -> {url}")
    video_type = parseType(url)
    if video_type == 'm3u8':
        download_m3u8_video(url=url, video_save_path = video_save_path, video_name=video_name,thread_num=thread_num)
        return
    else: 
        logger.error('下载地址有误，请核对')

def batch_download(batch_file_path, video_save_path, thread_num):
    if file_exists(batch_file_path):
        logger.info(f"开始读取文件 -> {batch_file_path}")
        if file_is_txt(batch_file_path):
            url_list = read_txt(batch_file_path)
            for u in url_list:
                singleDownload(url=u, video_save_path=video_save_path, thread_num=thread_num)
        elif file_is_csv(batch_file_path):
            url_map = read_csv(batch_file_path)
            for u in url_map:
                singleDownload(url=u['url'], video_save_path=video_save_path, thread_num=thread_num, video_name = u['name'])

    else:
        logger.error(f"文件 [{batch_file_path}]不存在，请确认--batch-file参数是否正确或者文件是否存在！")
        



if __name__ == '__main__':
    try:
        main()
    except IndexError as ie:
        logger.error('用户输入内容序号有误，请核对后重新输入!')
    except requests.exceptions.ProxyError as pe:
        logger.error('网络异常，请确认网络正常连接并且关闭系统代理后进行操作！')
    except requests.exceptions.SSLError as e:
        logger.error('SSL/TLS 验证错误')
    except KeyboardInterrupt:
        pass
    except SystemExit:
        raise