import psutil
from func import database_api

__author__ = "Ali Emre Oz"


def post_data(token, course, exam, userid, counter, self, dt):
    """
    collecting data
    :param token: user's token
    :param course: course's code
    :param exam: exam's name
    :param userid: user's id
    :param counter: keystroke count
    :param self: for accessing to student's answer
    :param dt: clock callback input
    :return:
    """

    cur_mem_usage = round(float(psutil.virtual_memory().used) / 1024 / 1024, 2)
    net_sent = float(psutil.net_io_counters().bytes_sent) / 1024
    net_recv = float(psutil.net_io_counters().bytes_recv) / 1024

    exam_data = {"keystroke": [counter], "memory_usage": [cur_mem_usage],
                 "network_download": [net_recv], "network_upload": [net_sent],
                 "key_stream": "Question ID: {id}\n---\n{ans}".format(id=self.question_no, ans=self.answer)}

    database_api.postExamData(token, course, exam, userid, **exam_data)
