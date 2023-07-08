
import queue, time, threading
import concurrent.futures

class ThreadPool():
    '''线城池模块'''
    def __init__(self, thread_num, call = None):
        self.max_thread = thread_num
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_thread)
        self.task_queue = queue.Queue()
        self.futures = {}
        self.call = call

    def add_task(self, func, target):
        new_task = (func, target)
        self.task_queue.put(new_task)

    def start(self):
        while self.task_queue.qsize() != 0:
            current_target, current_script = self.task_queue.get()
            future = self.thread_pool.submit(current_target, *current_script)
            self.futures[future] = (current_target, current_script)
        # while len(self.futures) > 0:
        for future in concurrent.futures.as_completed(self.futures):
            if(self.call is not None):
                self.call()

        self.thread_pool.shutdown(wait=True)
    
    def do_result(self, result):
        print(result)