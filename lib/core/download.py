from lib.core.m3u8_download import downloadm3u8
from lib.core.m3u8_download import getm3u8key
from lib.core.m3u8_download import downloadM3u8Ts
from lib.parse.m3u8_parse import m3u8ToJson
from lib.parse.m3u8_parse import getM3u8KeyUri
from lib.parse.url_parse import getm3u8BaseUrl
from lib.parse.url_parse import url_path
from lib.core.log import logger
from lib.core.convert import tsToMp4forffmpeg
from lib.core.convert import m4s_merge_for_ffmpeg
from lib.core.convert import m4s_audio_video_merge
from lib.core.use_parameter import getTmpPath
from lib.core.use_parameter import numlen
from lib.core.use_parameter import numformat
from lib.core.threads import ThreadPool
from lib.core.files import del_dir_not_empty
from lib.core.files import delete_file
from lib.request.http_request import request
from lib.parse.html_parse import get_html_tag_content
from lib.core.cmd_output import outputTable
from lib.core.cmd_output import get_link_text
from lib.request.http_request import request_cookie
from lib.validate.inquirer_validate import validate_number
from lib.validate.inquirer_validate import validate_input
from lib.core.progressbar import get_progress_bar
from lib.request.http_request import getContentLength
from lib.core.m4s_download import downloadM4s
from lib.core.m4s_download import single_download
from lib.core.constant import AUDIO_BIT
from lib.core.command_in import confirm_input
from lib.core.command_in import text_input
from lib.core import shared_variable
import multiprocessing
import json
import re


def download_m3u8_video(url, video_save_path, video_name, thread_num):
    
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
        logger.info(f'文件保存路径 -> {get_link_text(video_save_path + video_name + ".mp4")}')
        del_dir_not_empty(filepath)

    def pbarUp():
        pbar.update(1)
        increment_count()
        if count.value == json_data['count']:
            merge()

    countlen = numlen(json_data['count'])

    if thread_num is not None and thread_num > 1:
        # thread_down = thread(num_threads = thread_num)
        thread_pool = ThreadPool(thread_num, pbarUp)
        for s in seg:
            thread_pool.add_task(downloadM3u8Ts, (s['url'], s['key'], s['iv'], numformat(s['index'], countlen), s['method'], filepath))
        thread_pool.start()
    else:
        for s in seg:
            downloadM3u8Ts(s['url'], s['key'], s['iv'], numformat(s['index'], countlen), s['method'], filepath)
            pbar.update(1)
        merge()


def download_bili(url, video_save_path, video_name, thread_num):
    logger.info(f'开始解析 url -> [{url}]')
    shared_variable.headers['Referer'] = url
    read_cookie = confirm_input('read_cookie', message='是否允许读取本机浏览器Cookie?', default=False)

    browser_type = 'chrome'
    if read_cookie:
        browser_type = text_input('browser_type',message='请输入cookie所属浏览器名称(chrome/firefox/edge)', validate=validate_input)
        browser_type = browser_type.lower()

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
    audio_table_map = {}
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
    user_video_code = text_input('user_code_id', message='请输入下载视频清晰度对应的编号值 (eg:1)', default=1, validate=validate_number(lt=0, gt=len(accept_quality_set)))
    video_down_id = accept_quality_set[int(user_video_code) - 1]
    for v in video_info:
        if v['id'] == video_down_id and v['codecid'] == 12:
            download_url  = v['baseUrl']
    outputTable(audio_table)
    user_audio_code = text_input('audio_code_id', message = '请输入下载视频音频码率对应的编号值, 默认128kbps (eg:1)', default=2, validate=validate_number(gt=len(audio_table_map)))
    for a in audio_info:
        if a['id'] == audio_table_map[int(user_audio_code)]:
            audio_url = a['baseUrl']

    if video_name is None or video_name == '':
        video_name = url_path(url).replace('/','')

    filepath = getTmpPath(video_save_path, video_name)    
    
    download_video_path = video_save_path + video_name + '_v.m4s'
    download_audio_path = video_save_path + video_name + '_a.m4s'

    if thread_num is not None and thread_num > 1:
        logger.info('Start downloading the video file...')
        file_size = getContentLength(download_url, stream=True)
        progress_bar = get_progress_bar(file_size)
        block_size = 100000
        block_size = file_size // thread_num
        thread_pool = ThreadPool(thread_num)
        for i in range(thread_num):
            start = i * block_size
            if i == thread_num - 1:
                end = file_size
            else:
                end = start + block_size - 1
            thread_pool.add_task(downloadM4s, (download_url, start, end, numformat(i, thread_num), filepath, progress_bar))
        
        thread_pool.start()
        progress_bar.close()
        m4s_merge_for_ffmpeg(filepath, video_save_path, video_name)
        del_dir_not_empty(filepath)
        logger.info('Start downloading the audio file...')
        single_download(audio_url, download_audio_path)
        logger.info('Start compositing...')
        m4s_audio_video_merge(video_save_path, video_save_path, video_name)
        logger.info('The download is complete.')
        logger.info(f'文件保存路径 -> {get_link_text(video_save_path + video_name + ".mp4")}')
        delete_file(download_audio_path)
        delete_file(video_save_path + video_name + '_v.mp4')
    else:
        block_size = 1024  # 每次下载的数据块大小
        logger.info('Start downloading the video file...')
        single_download(download_url, download_video_path)
        logger.info('Start downloading the audio file...')
        single_download(audio_url, download_audio_path)
        logger.info('Start compositing...')
        m4s_audio_video_merge(video_save_path, video_save_path, video_name)
        logger.info('The download is complete.')
        logger.info(f'文件保存路径 -> {get_link_text(video_save_path + video_name + ".mp4")}')
        delete_file(download_video_path)
        delete_file(download_audio_path)
