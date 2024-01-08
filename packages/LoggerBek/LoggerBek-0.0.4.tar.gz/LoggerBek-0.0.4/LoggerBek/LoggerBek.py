from functools import wraps
import time
import logging
import psutil


class LoggerBek:
    def __init__(self, filename='logfile.txt'):
        logging.basicConfig(filename=filename,
                            encoding='utf-8',
                            filemode='a',
                            format='[%(asctime)s]|%(levelname)s:%(message)s',
                            datefmt="%Y-%m-%d|%H:%M:%S %p",
                            level=logging.INFO)

    def debug(self, debug):
        logging.debug(debug)

    def info(self, info):
        logging.info(info)

    def warning(self, warning):
        logging.warning(warning)

    def error(self, error):
        logging.error(error)

    def critical(self, critical):
        logging.critical(critical)

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cur_proc = psutil.Process()
            mem_info_before = cur_proc.memory_info()
            st = time.time()
            result = f(*args, **kwargs)
            ft = time.time()
            mem_info_after = cur_proc.memory_info()
            rss_diff = mem_info_after.rss - mem_info_before.rss
            vms_diff = mem_info_after.vms - mem_info_before.vms
            self.info(f'[Function:{f.__name__}][Handling time:{ft - st}][Result:{result}][RSS/VMS:{rss_diff}/{vms_diff} byte]')
            return result
        return wrapper
