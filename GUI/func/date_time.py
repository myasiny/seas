from time import gmtime, strftime

def date_time(clock, dt):
    clock.text = strftime("%H:%M:%S", gmtime())