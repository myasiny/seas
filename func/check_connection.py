"""
check_connection
================

`check_connection` checks status of communication with server and updates image widget accordingly.
"""

from func import database_api

__author__ = "Muhammed Yasin Yildirim"


def is_alive(img, dt):
    """
    This method checks if that server is alive and updates image shown on given widget accordingly.
    :param img: It is image widget updated according to status of server communication.
    :param dt: It is for handling callback input.
    :return:
    """

    try:
        if database_api.testConnection():
            img.source = "data/img/ico_connection_success.png"
        else:
            img.source = "data/img/ico_connection_fail.png"
    except:
        img.source = "data/img/ico_connection_wait.png"
    finally:
        img.reload()
