from kivy.cache import Cache
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.floatlayout import FloatLayout

import os
from SEAS.func import database_api
from SEAS.func.barcode_png import qrcode_png
from SEAS.func.round_image import round_render

'''
    This method updates top-mid identity card widget according to user information before entering PgProfile and PgStdProfile
'''

def on_pre_enter(self):
    # temp_login = open("data/temp_login.seas", "r")
    # self.data_login = temp_login.readlines()

    try:
        self.ids["img_user_card"].source = "img/pic_current_user.png"
        self.ids["img_user_card"].reload()
    except:
        self.ids["img_user_card"].reload()

    qrcode_png(Cache.get("info", "id"))
    self.ids["img_barcode_1"].reload()
    self.ids["img_barcode_2"].reload()

    self.ids["txt_username"].text = Cache.get("info", "name").title() + " " + Cache.get("info", "surname").title()
    self.ids["txt_usermail"].text = Cache.get("info", "mail")
    if Cache.get("info", "dept") is not None:
        self.ids["txt_userdept"].text = Cache.get("info", "dept").title()
    self.ids["txt_useruniv"].text = Cache.get("info", "uni").replace("_", " ").title()

    self.ids["input_new_password"].disabled = True
    self.ids["input_new_mail"].disabled = True

    Logger.info("pgProfile: Detailed user information successfully written onto identity card")

'''
    This method opens pop-up for loading image file as png
    Accordingly, it calls on_pic_selected or disappears
'''

def on_change_pic(self):
    Logger.info("pgProfile: User called change picture pop-up")

    popup_content = FloatLayout()
    self.popup = Popup(title="Change Profile Picture",
                       content=popup_content, separator_color=[140 / 255., 55 / 255., 95 / 255., 1.],
                       size_hint=(None, None), size=(self.width / 2, self.height / 2))
    filechooser = FileChooserIconView(path=os.path.expanduser('~'), filters=["*.png"],
                                      size=(self.width, self.height),
                                      pos_hint={"center_x": .5, "center_y": .5})
    filechooser.bind(on_submit=self.on_pic_selected)
    popup_content.add_widget(filechooser)
    popup_content.add_widget(Button(text="Upload",
                                    font_name="font/LibelSuit.ttf",
                                    font_size=self.height / 40,
                                    background_normal="img/widget_100_green.png",
                                    background_down="img/widget_100_green_selected.png",
                                    size_hint_x=.5,
                                    size_hint_y=None, height=self.height / 20,
                                    pos_hint={"center_x": .25, "y": .0},
                                    on_release=filechooser.on_submit))
    popup_content.add_widget(Button(text="Cancel",
                                    font_name="font/LibelSuit.ttf",
                                    font_size=self.height / 40,
                                    background_normal="img/widget_100_red.png",
                                    background_down="img/widget_100_red_selected.png",
                                    size_hint_x=.5,
                                    size_hint_y=None, height=self.height / 20,
                                    pos_hint={"center_x": .75, "y": .0},
                                    on_release=self.popup.dismiss))
    self.popup.open()

'''
    This method sends uploaded image file to server and refreshes profile picture on either PgProfile or PgStdProfile
'''

def on_pic_selected(self, widget_name, file_path, mouse_pos):
    self.popup.dismiss()

    database_api.uploadProfilePic(Cache.get("info", "token"), Cache.get("info", "nick"), file_path[0])

    round_render()

    Logger.info("pgProfile: User successfully imported image file")

    return True

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
            result = database_api.changePassword(Cache.get("info", "token"),
                                                 Cache.get("info", "nick"),
                                                 input_current_password.text, input_new_password.text,
                                                 isMail=False)
            if result == "Password Changed":
                Logger.info("pgProfile: Password successfully changed")

                anim_appear = Animation(opacity=1, duration=1)
                anim_appear.start(img_change_done)
                def back_to_login(dt):
                    self.on_logout()
                Clock.schedule_once(back_to_login, 1)
            else:
                anim_appear = Animation(opacity=1, duration=1)
                anim_appear.start(img_change_failed)
        elif len(input_new_mail.text) > 0 and input_new_mail.disabled is False:
            result = database_api.changePassword(Cache.get("info", "token"),
                                                 Cache.get("info", "nick"),
                                                 input_current_password.text, input_new_mail.text,
                                                 isMail=True)
            if result == "Mail Changed":
                Logger.info("pgProfile: E-mail successfully changed")

                anim_appear = Animation(opacity=1, duration=1)
                anim_appear.start(img_change_done)
                def back_to_login(dt):
                    self.on_logout()
                Clock.schedule_once(back_to_login, 1)
            else:
                anim_appear = Animation(opacity=1, duration=1)
                anim_appear.start(img_change_failed)