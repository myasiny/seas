from kivy.logger import Logger

from GUI.func import database_api

'''
    This method ...
'''

def on_reset(self):
    # database_api TODO

    Logger.info("tabReset: Password successfully reset")

'''
    This method switches screen to new added one and deletes current screen in order to refresh in case user comes back
'''

def on_back(pages, screen):
    try:
        screen.switch_to(pages[2])
    except:
        screen.current = pages[2].name

    del pages[1]