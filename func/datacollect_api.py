from functools import partial

import psutil
from kivy.clock import Clock
from pynput import keyboard
from func import database_api

__author__ = "Ali Emre Oz"

unnecessary_list = ["Key.ctrl",
                    "Key.ctrl_l",
                    "Key.ctrl_r",
                    "Key.alt",
                    "Key.alt_gr",
                    "Key.alt_l",
                    "Key.alt_r",
                    "Key.menu",
                    "Key.cmd_l",
                    "Key.cmd_r",
                    "Key.shift",
                    "Key.shift_l",
                    "Key.shift_r",
                    ]

counter = 0

def on_press(key):
    if str(key) not in unnecessary_list:
        global counter
        counter += 1

def get_data(token, course, exam, userid, dt):
    global counter
    cur_mem_usage = round(float(psutil.virtual_memory().used) / 1024 / 1024, 2)
    net_sent = float(psutil.net_io_counters().bytes_sent) / 1024
    net_recv = float(psutil.net_io_counters().bytes_recv) / 1024

    exam_data = {"keystroke": [counter], "memory_usage": [cur_mem_usage], "network_download": [net_recv],
                 "network_upload": [net_sent], "key_stream": []}

    database_api.postExamData(token, course, exam, userid, **exam_data)

def listen(token, course, exam, userid):
    Clock.schedule_interval(partial(get_data, token, course, exam, userid), 5)

    with keyboard.Listener(
            on_press=on_press,
            ) as listener:
        listener.join()