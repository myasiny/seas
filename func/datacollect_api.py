import psutil
from func import database_api

__author__ = "Ali Emre Oz"


def get_data(token, course, exam, userid, counter, dt):
    cur_mem_usage = round(float(psutil.virtual_memory().used) / 1024 / 1024, 2)
    net_sent = float(psutil.net_io_counters().bytes_sent) / 1024
    net_recv = float(psutil.net_io_counters().bytes_recv) / 1024

    exam_data = {"keystroke": [counter], "memory_usage": [cur_mem_usage], "network_download": [net_recv],
                 "network_upload": [net_sent], "key_stream": []}

    database_api.postExamData(token, course, exam, userid, **exam_data)
