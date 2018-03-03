from time import *

def date_time(clock, dt):
    clock.text = strftime("%H:%M:%S", localtime())

def min_timer(clock, self, dt):
    clock.text = str(self.duration - 1)
    self.duration -= 1

    if self.duration <= 0:
        self.over = True
        self.on_finish_exam()
    else:
        self.over = False