from kivy.logger import Logger
from kivy.animation import Animation

import time
from GUI.func import database_api
from GUI.func.round_image import round_image
from GUI.func.barcode_png import barcode_png

'''
    This method updates top-mid identity card widget according to user information before entering PgProfile
'''

def on_pre_enter(self):
    temp_login = open("data/temp_login.seas", "r")
    self.data_login = temp_login.readlines()

    round_image()
    self.ids["img_user"].reload()

    barcode_png(self.data_login[3].replace("\n", ""))
    self.ids["img_barcode_1"].reload()
    self.ids["img_barcode_2"].reload()

    self.ids["txt_username"].text = self.data_login[1].replace("\n", " ").replace("_", " ").title() +\
                                    self.data_login[2].replace("\n", "").replace("_", " ").title()
    self.ids["txt_usermail"].text = self.data_login[5].replace("\n", "")
    self.ids["txt_userdept"].text = self.data_login[6].replace("\n", "").replace("_", " ").title()
    self.ids["txt_useruniv"].text = self.data_login[7].replace("\n", "").replace("_", " ").title()

    self.ids["input_new_password"].disabled = True
    self.ids["input_new_mail"].disabled = True

    Logger.info("pgProfile: Detailed user information successfully written onto identity card")

'''
    This method runs every time text in current password field changes
    Accordingly, it enables or disables new password and new e-mail fields
'''

def on_text_change(self, name):
    if name == "current_password":
        if not self.ids["input_current_password"].text == "":
            self.ids["input_new_password"].disabled = False
            self.ids["input_new_mail"].disabled = False
        else:
            self.ids["input_new_password"].disabled = True
            self.ids["input_new_mail"].disabled = True
    elif name == "new_password":
        if not self.ids["input_new_password"].text == "":
            self.ids["input_new_mail"].disabled = True
        else:
            self.ids["input_new_mail"].disabled = False
    elif name == "new_mail":
        if not self.ids["input_new_mail"].text == "":
            self.ids["input_new_password"].disabled = True
        else:
            self.ids["input_new_password"].disabled = False

'''
    This method checks whether new password or new e-mail are provided along with current password or not
    Accordingly, it raises warning or connects to server for changing either password or e-mail
    If current password is correct, it updates password or e-mail and directs to PgLogin
    If not, it raises error and process for changing password or e-mail fails
'''

def on_submit(self):
    img_wrong = self.ids["img_wrong"]
    img_wrong.opacity = 0
    img_change_done = self.ids["img_change_done"]
    img_change_done.opacity = 0
    img_change_failed = self.ids["img_change_failed"]
    img_change_failed.opacity = 0

    input_current_password = self.ids["input_current_password"]
    input_new_password = self.ids["input_new_password"]
    input_new_mail = self.ids["input_new_mail"]

    if input_current_password.text == "":
        anim_appear = Animation(opacity=1, duration=1)
        anim_appear.start(img_wrong)
    else:
        if len(input_new_password.text) > 0 and input_new_password.disabled is False:
            result = database_api.changePassword(self.data_login[7].replace("\n", ""),
                                                 self.data_login[0].replace("\n", ""),
                                                 input_current_password.text, input_new_password.text,
                                                 isMail=False)
            if result == "Password Changed":
                Logger.info("pgProfile: Password successfully changed")

                anim_appear = Animation(opacity=1, duration=1)
                anim_appear.start(img_change_done)
                time.sleep(1)
                self.on_logout()
            else:
                anim_appear = Animation(opacity=1, duration=1)
                anim_appear.start(img_change_failed)
        elif len(input_new_mail.text) > 0 and input_new_mail.disabled is False:
            result = database_api.changePassword(self.data_login[7].replace("\n", ""),
                                                 self.data_login[0].replace("\n", ""),
                                                 input_current_password.text, input_new_mail.text,
                                                 isMail=True)
            if result == "Mail Changed":
                Logger.info("pgProfile: E-mail successfully changed")

                anim_appear = Animation(opacity=1, duration=1)
                anim_appear.start(img_change_done)
                time.sleep(1)
                self.on_logout()
            else:
                anim_appear = Animation(opacity=1, duration=1)
                anim_appear.start(img_change_failed)