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
from lib.core.useparameter import getTmpPath
from lib.core.useparameter import numlen
from lib.core.useparameter import numformat
from lib.core.threads import thread
from lib.core.files import del_dir_not_empty
from lib.request.httprequest import request
from bs4 import BeautifulSoup
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
    resp = request(url)
    # print(resp.text)
    html = resp.text.replace("\n", "")

    soup = BeautifulSoup(html, 'html.parser')

    # 找到所有的<script>标签
    script_tags = soup.find_all('script')

    html = ''

    # 遍历每个<script>标签并打印脚本内容
    for script_tag in script_tags:
        script_content = script_tag.get_text()

        if script_content.startswith('window.__playinfo__'):
            html = script_content.replace('window.__playinfo__=','')
            break
    
    logger.debug(json.loads(html))
    questions = [
        inquirer.Text('name', message='请输入你的名字')
    ]
    
    answers = inquirer.prompt(questions)
    logger.debug(answers['name'])