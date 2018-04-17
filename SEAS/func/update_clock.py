"""
update_clock
============

`update_clock` updates either clock every second or timer every minute.
"""

from time import *

__author__ = "Muhammed Yasin Yildirim"


def date_time(watch, dt):
    """
    This method updates clock every second.
    :param watch: It is clock.
    :param dt: It is for handling callback input.
    :return:
    """

    watch.text = strftime("%H:%M:%S",
                          localtime()
                          )


def min_timer(watch, self, dt):
    """
    This method updates timer every minute.
    :param watch: It is timer.
    :param self: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return:
    """

    watch.text = str(self.duration - 1)
    self.duration -= 1

    if self.duration <= 0:
        self.over = True
        self.on_exam_finish()
    else:
        self.over = False
