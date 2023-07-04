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
from lib.core.convert import m4s_audio_video_merge
from lib.core.useparameter import getTmpPath
from lib.core.useparameter import numlen
from lib.core.useparameter import numformat
from lib.core.threads import thread
from lib.core.files import del_dir_not_empty
from lib.core.files import delete_file
from lib.request.httprequest import request
from lib.parse.htmlParse import get_html_tag_content
from lib.core.cmdOutput import outputTable
from lib.request.httprequest import request_cookie
from lib.request.httprequest import head
from lib.validate.inquirervalidate import validate_number
from lib.core.progressbar import get_progress_bar
from lib.request.httprequest import getContentLength
from lib.core.m4sdownload import downloadM4s
from lib.core.m4sdownload import single_download
from lib.core.constant import AUDIO_BIT
import inquirer
import multiprocessing
import json
import re
import threading


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
    pbar = get_progress_bar(len(seg))
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
    logger.info(f'开始解析 url -> [{url}]')
    read_cookie_inquirer = [inquirer.Text('read_cookie', message='是否允许读取浏览器cookie(Y/N)')]
    browser_type_inquirer = [inquirer.Text('browser_type', message='请输入cookie所属浏览器名称(chrome/firefox/edge)')]
    read_cookie_answer = inquirer.prompt(read_cookie_inquirer)
    browser_type = 'chrome'
    if read_cookie_answer['read_cookie'].upper() == 'Y':
        read_cookie = True
        browser_type_inquirer = inquirer.prompt(browser_type_inquirer)
        if 'chrome' == browser_type_inquirer['browser_type'].lower():
            browser_type = 'chrome'
        elif 'firefox' == browser_type_inquirer['browser_type'].lower():
            browser_type = 'firefox'
        elif 'edge' == browser_type_inquirer['browser_type'].lower():
            browser_type = 'edge'         
    else:
        read_cookie = False
    resp = request_cookie(url, set_cookie=read_cookie, browser=browser_type)
    html_data = get_html_tag_content(resp.text, 'script', 'window.__playinfo__=')
    if html_data is None or html_data == '':
        logger.error('未获取到视频数据，请检查url是否正确！')
        return
    json_data = json.loads(html_data)
    accept_description = json_data['data']['accept_description']
    accept_quality = json_data['data']['accept_quality']
    video_info = json_data['data']['dash']['video']
    audio_info = json_data['data']['dash']['audio']
    if video_info is None or video_info == '':
        logger.error('未获取到视频数据，请检查url是否正确！')
        return
    if audio_info is None or audio_info == '':
        logger.error('未获取到音频数据，请检查url是否正确！')
        return
    accept_quality_set = set()
    audio_list = []
    for v in video_info:
        accept_quality_set.add(v['id'])
    for a in audio_info:
        audio_list.append(a['id'])
    accept_quality_set = sorted(accept_quality_set, reverse=True)
    video_info_table = [['编号','清晰度']]
    audio_table = [['编号','音频码率']]
    audio_table_map = {'1':30280,'2':30232,'3':30216}
    for i, e in enumerate(sorted(audio_list, reverse=True), start=1):
        if int(e) == 30280:
            audio_table.append([i, '320kbps'])
            audio_table_map[i] = AUDIO_BIT['320kbps']
        if int(e) == 30232:
            audio_table.append([i, '128kbps'])
            audio_table_map[i] = AUDIO_BIT['128kbps']
        if int(e) == 30216:
            audio_table.append([i, '64kbps'])
            audio_table_map[i] = AUDIO_BIT['64kbps']

    for index, element in enumerate(accept_quality_set, start=1):
        row = [index, accept_description[accept_quality.index(element)]]
        video_info_table.append(row)

    outputTable(video_info_table)
    user_code_inq = [inquirer.Text('user_code_id', message='请输入下载视频清晰度对应的编号值 (eg:1)', default=1, validate = [validate_number])]
    user_code_answer = inquirer.prompt(user_code_inq)
    outputTable(audio_table)
    user_audio_code_inq = [inquirer.Text('audio_code_id', message = '请输入下载视频音频码率对应的编号值, 默认128kbps (eg:1)', default=2, validate=[validate_number])]
    user_audio_code_answer = inquirer.prompt(user_audio_code_inq)
    video_down_id = accept_quality_set[int(user_code_answer['user_code_id']) - 1]
    for v in video_info:
        if v['id'] == video_down_id and v['codecid'] == 12:
            download_url  = v['baseUrl']

    for a in audio_info:
        if a['id'] == audio_table_map[user_audio_code_answer['audio_code_id']]:
            audio_url = a['baseUrl']

    filepath = getTmpPath(video_save_path, video_name)    
    
    if thread_num is not None and thread_num > 1:
        file_size = getContentLength(download_url, stream=True)
        block_size = 100000
        block_size = file_size // thread_num
        threads = []
        # thread_down = thread(num_threads = thread_num)
        for i in range(thread_num):
            start = i * block_size
            if i == thread_num - 1:
                end = file_size
            else:
                end = start + block_size - 1
            # argss.append((download_url, start, end, numformat(i, thread_num), filepath, progress_bar))
            thread = threading.Thread(target=downloadM4s, args=(download_url, start, end, numformat(i, thread_num), filepath, progress_bar))
            thread.start()
            threads.append(thread)
            # thread_down.download_m4s(download_url, start, end, numformat(i, thread_num), filepath, progress_bar)
        for thread in threads:
            thread.join()

        progress_bar.close()
        m4sToMp4forffmpeg(filepath, video_save_path, video_name)

    else:
        download_video_path = video_save_path + video_name + '_v.m4s'
        download_audio_path = video_save_path + video_name + '_a.m4s'
        block_size = 1024  # 每次下载的数据块大小
        logger.info('Start downloading the video file...')
        single_download(download_url, download_video_path)
        logger.info('Start downloading the audio file...')
        single_download(audio_url, download_audio_path)
        logger.info('Start compositing...')
        m4s_audio_video_merge(video_save_path, video_save_path, video_name)
        logger.info('The download is complete.')
        logger.info(f'文件保存路径 -> [{video_save_path}{video_name}.mp4]')
        delete_file(download_video_path)
        delete_file(download_audio_path)
