import time
from functools import wraps
import requests
from socket import gethostname
try:
    import psutil
except ImportError:
    import pip
    pip.main(["install", "psutil"])
    import psutil

def redis_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        result = func(*args, **kwargs)

        # calc elapsed time
        elapsed_time = time.time() - start_time

        memory = psutil.virtual_memory()

        # build dict
        data = {'method': func.__name__,
                'etime': elapsed_time,
                'mtotal': memory.total,
                'mfree': memory.free,
                'mpercent': memory.percent,
                'host': gethostname()}

        result = requests.post('http://10.6.19.12:1000/log', json = data)

        return result
    return wrapper

def clear_redis():
    result = requests.post('http://10.6.19.12:1000/clear')

def start_logging():
    result = requests.post('http://10.6.19.12:1000/init')