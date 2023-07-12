import logging
import sys
from datetime import datetime

class Logger:

    _instance = None
    
    def __init__(self, name='downloader-log', level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')

        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        file_handler = logging.FileHandler(f'./log/{name}-{datetime.now().strftime("%Y%m%d%H%M%S")}.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def debug(self, msg):
        self.logger.debug(f"\033[36m{msg}\033[0m")

    def info(self, msg):
        self.logger.info(f"\033[32m{msg}\033[0m")

    def warning(self, msg):
        self.logger.warning(f"\033[01;33m{msg}\033[0m")

    def error(self, msg):
        self.logger.error(f"\033[01;91m{msg}\033[0m")

    def critical(self, msg):
        self.logger.critical(f"\033[31m\033[1m{msg}\033[0m")


logger = Logger()