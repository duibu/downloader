# Downloaders
[![Python 2.6|2.7|3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-MIT-red.svg)](https://raw.githubusercontent.com/duibu/downloader/main/LICENSE)
## 环境说明

python:3.x

## 安装

使用git下载代码

```
git clone https://github.com/duibu/downloader.git
```

安装所需依赖

```
pip install -r requirements.txt
```

## 参数说明

```
-u/--url: 下载视频的url地址，只可以设置单个url
-name/--video-name: 下载到本地视频的文件名称
-path/--save-path: 视频保存路径
--batch-file: 批量地址文件的绝对路径，批量下载时使用，支持csv和txt
-t/--thread: 下载视频文件的线程数
```

## 使用示例

### 下载单个视频

直接下载

```
python downloader.py --url 'http://example.com/example.m3u8?xxx=xxx'
```

指定文件名称下载

```
python downloader.py --url 'http://example.com/example.m3u8?xxx=xxx' -name video
```

指定保存路径和文件名下载

```
python downloader.py --url 'http://example.com/example.m3u8?xxx=xxx' -name video -path /home/user/video
```

批量下载

```
python downloader.py --batch-file d:/video/url.txt -path /home/user/video
```
