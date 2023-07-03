from lib.core.m3u8download import downloadm3u8
from lib.core.m3u8download import getm3u8key
from lib.core.m3u8download import downloadM3u8Ts
from lib.parse.m3u8Parse import m3u8ToJson
from lib.parse.m3u8Parse import getM3u8KeyUri
from lib.parse.urlParse import getm3u8BaseUrl
from lib.parse.urlParse import url_path
from lib.core.log import logger
from lib.core.convert import tsToMp4
from lib.core.convert import tsToMp4forffmpeg
from lib.core.convert import m4sToMp4forffmpeg
from lib.core.useparameter import getTmpPath
from lib.core.useparameter import numlen
from lib.core.useparameter import numformat
from lib.core.threads import thread
from lib.core.files import del_dir_not_empty
from lib.request.httprequest import request
from lib.parse.htmlParse import get_html_tag_content
from lib.core.cmdOutput import outputTable
from lib.request.httprequest import request_cookie
from lib.request.httprequest import head
from tqdm import tqdm
import inquirer
import multiprocessing
import json
from datetime import datetime
import re


def download_m3u8_video(url, video_save_path, video_name,thread_num):
    
    count = multiprocessing.Value('i', 0)
    def increment_count():
        with count.get_lock():
            count.value += 1

    baseUrl = getm3u8BaseUrl(url)
    if video_name is None or video_name == '':
        video_name = url_path(url).replace('/','')
    
    logger.info(f"开始下载 -> {video_name}")
    m3u8_ori_content = downloadm3u8(url)
    key_uri = getM3u8KeyUri(m3u8_ori_content)
    if key_uri is not None and key_uri != '':
        key = getm3u8key(key_uri)
        m3u8Json = m3u8ToJson(baseUrl, m3u8_ori_content, key)
    else:
        m3u8Json = m3u8ToJson(baseUrl, m3u8_ori_content)
    json_data = json.loads(m3u8Json)
    seg = json_data['segments']
    pbar = tqdm(desc=datetime.now().strftime("[%Y-%m-%d %H:%M:%S,%f")[:-3] + ']',total=len(seg),bar_format='{desc} [{bar:85}]{percentage:3.0f}% ({n_fmt}/{total_fmt}) [{elapsed}<{remaining}, {rate_fmt}]', ascii=True)
    filepath = getTmpPath(video_save_path, video_name)

    def merge():
        pbar.close()
        tsToMp4forffmpeg(tsfilepath = filepath, outputname = video_name, outputpath = video_save_path)
        logger.info('The download is complete')
        del_dir_not_empty(filepath)

    def pbarUp():
        pbar.update(1)
        increment_count()
        if count.value == json_data['count']:
            merge()

    countlen = numlen(json_data['count'])

    if thread_num is not None and thread_num > 1:
        thread_down = thread(num_threads = thread_num)
        for s in seg:
            thread_down.downloadts(s['url'], s['key'], s['iv'], numformat(s['index'], countlen), s['method'], filepath, pbarUp())
        thread_down.wait_completion()
    else:
        for s in seg:
            downloadM3u8Ts(s['url'], s['key'], s['iv'], numformat(s['index'], countlen), s['method'], filepath)
            pbar.update(1)
        merge()


def download_bili(url, video_save_path, video_name,thread_num):
    resp = request_cookie(url,set_cookie=True)
    html_data = get_html_tag_content(resp.text, 'script', 'window.__playinfo__=')
    if html_data is None or html_data == '':
        logger.error('未获取到视频数据，请检查url是否正确！')
        return
    json_data = json.loads(html_data)
    accept_description = json_data['data']['accept_description']
    accept_quality = json_data['data']['accept_quality']
    video_info = json_data['data']['dash']['video']
    accept_quality_set = set()
    for v in video_info:
        accept_quality_set.add(v['id'])
    accept_quality_set = sorted(accept_quality_set, reverse=True)
    video_info_table = [['编号','清晰度']]

    for index, element in enumerate(accept_quality_set, start=1):
        row = [index, accept_description[accept_quality.index(element)]]
        video_info_table.append(row)

    outputTable(video_info_table)
    user_code_inq = [inquirer.Text('user_code_id', '请输入下载视频清晰度对应的编号值 (eg:1)')]
    user_code_answer = inquirer.prompt(user_code_inq)
    video_down_id = accept_quality_set[int(user_code_answer['user_code_id']) - 1]
    for v in video_info:
        if v['id'] == video_down_id and v['codecid'] == 12:
            download_url  = v['baseUrl']

    filepath = getTmpPath(video_save_path, video_name)
    head_resp = request(download_url, stream=True)
    headers = head_resp.headers
    file_size = int(head_resp.headers.get("Content-Length", 0))
    progress_bar = tqdm(desc=datetime.now().strftime("[%Y-%m-%d %H:%M:%S,%f")[:-3] + ']',total=file_size,bar_format='{desc} [{bar:85}]{percentage:3.0f}% ({n_fmt}/{total_fmt}) [{elapsed}<{remaining}, {rate_fmt}]', ascii=True)

    if thread_num is not None and thread_num > 1:
        block_size = 100000
        total_num = file_size // block_size
        thread_down = thread(num_threads = thread_num)
        for i in range(total_num):
            start = i * block_size
            if i == total_num - 1:
                end = file_size
            else:
                end = start + block_size - 1
            thread_down.download_m4s(download_url, start, end, numformat(i, thread_num), filepath, progress_bar)
        thread_down.wait_completion()
        progress_bar.close()
        m4sToMp4forffmpeg(filepath, video_save_path, video_name)

    else:
        response = request(download_url, stream=True)
        download_file_path = video_save_path + video_name + '.m4s'
        block_size = 1024  # 每次下载的数据块大小

        with open(download_file_path, "wb") as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

        progress_bar.close()
        m4sToMp4forffmpeg(video_save_path, video_save_path, video_name)

