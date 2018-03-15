from kivy.logger import Logger
from kivy.animation import Animation

import time
from GUI.func import database_api

'''
    This method checks whether username and e-mail are provided or not
    Accordingly, it raises warning or connects to server for resetting password
    If user credentials are correct, it resets password and directs to PgLogin
    If not, it raises error and process for resetting password fails
'''

def on_reset(self):
    img_status = self.ids["img_status"]
    img_status.source = "img/ico_loading.gif"
    img_status.opacity = 0
    img_status.reload()

    anim_status = Animation(opacity=1, duration=1)
    anim_status.start(img_status)

    if self.ids["input_username"].text == "" or self.ids["input_email"].text == "":
        anim_status.stop(img_status)

        img_status.source = "img/ico_warning.png"
        img_status.opacity = 1
        img_status.reload()
    else:
        try:
            # data = TODO

            Logger.info("tabReset: User credentials successfully sent to server")
        except:
            data = None

            Logger.error("tabReset: Server is not reachable")

        if isinstance(data, list):
            anim_status.stop(img_status)

            img_status.source = "img/ico_success.png"
            img_status.opacity = 1
            img_status.reload()

            Logger.info("tabReset: Password successfully reset")

            time.sleep(1)
            self.on_back()

'''
    This method switches screen to new added one and deletes current screen in order to refresh in case user comes back
'''

def on_back(pages, screen):
    try:
        screen.switch_to(pages[2])
    except:
        screen.current = pages[2].name

    del pages[1]