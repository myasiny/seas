'''
    These methods are used for clock and timer on PgLiveExam respectively
    First method returns current hour, minute and second according to local time
    Second method returns duration decreased by 1 and it checks whether exam time is expired or not
    Accordingly, it sets self.over to either True or False in order to let PgLiveExam take necessary actions
'''

from kivy.logger import Logger

from time import *

def date_time(clock, dt):
    clock.text = strftime("%H:%M:%S", localtime())

def min_timer(clock, self, dt):
    clock.text = str(self.duration - 1)
    self.duration -= 1

    if self.duration <= 0:
        self.over = True
        self.on_finish_exam()

        Logger.info("date_time: Exam time expired")
    else:
        self.over = False