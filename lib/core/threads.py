from concurrent.futures import ThreadPoolExecutor
from lib.core.m3u8download import downloadM3u8Ts

class thread:
    def __init__(self, num_threads=10,done_callback=None):
        self.num_threads = num_threads
        self.executor = ThreadPoolExecutor(max_workers=num_threads)

    def downloadts(self, url, key, iv, name, method, path, callback=None):
        future = self.executor.submit(downloadM3u8Ts(url, key, iv, name, method, path))
        if callback:
            future.add_done_callback(callback)

    def wait_completion(self):
        self.executor.shutdown(wait=True)