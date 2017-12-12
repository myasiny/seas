from time import localtime, strftime

def date_time(clock, dt):
    clock.text = strftime("%H:%M:%S", localtime())