from kivy.logger import Logger
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout

from SEAS.func import image_button
from SEAS.func import database_api

'''
    This method implements necessary image buttons
'''

def on_pre_enter(self):
    image_button.add_button(self, "img/ico_quit.png", "img/ico_quit_pressed.png",
                            (.05, .05), {"x": .95, "center_y": .95},
                            self.on_quit)

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
            data = ["TODO"]

            Logger.info("tabReset: User credentials successfully sent to server")
        except:
            data = None

            Logger.error("tabReset: Server is not reachable")

        if isinstance(data, list):
            anim_status.stop(img_status)

            img_status.source = "img/ico_success.png"
            img_status.opacity = 1
            img_status.reload()

            popup_content = FloatLayout()
            self.popup = Popup(title="Reset Your Password",
                               content=popup_content, separator_color=[140 / 255., 55 / 255., 95 / 255., 1.],
                               size_hint=(None, None), size=(self.width / 3, self.height / 3))
            self.input_key = TextInput(hint_text="Confirmation Key", write_tab=False, multiline=False,
                                       font_name="font/CaviarDreams_Bold.ttf", font_size=self.height / 36,
                                       background_normal="img/widget_75_gray.png",
                                       background_active="img/widget_75_selected.png",
                                       background_disabled_normal="img/widget_75_black.png",
                                       padding_y=[self.height / 36, 0], size_hint=(.9, .3),
                                       pos_hint={"center_x": .5, "center_y": .8})
            popup_content.add_widget(self.input_key)
            self.input_new_password = TextInput(hint_text="New Password", write_tab=False, multiline=False, password=True,
                                                font_name="font/CaviarDreams_Bold.ttf", font_size=self.height / 36,
                                                background_normal="img/widget_75_gray.png",
                                                background_active="img/widget_75_selected.png",
                                                background_disabled_normal="img/widget_75_black.png",
                                                padding_y=[self.height / 36, 0], size_hint=(.9, .3),
                                                pos_hint={"center_x": .5, "center_y": .4})
            popup_content.add_widget(self.input_new_password)
            self.img_confirm_status = Image(source="img/ico_wrong.png", allow_stretch=True, opacity=0,
                                            size_hint=(.15, .15), pos_hint={"center_x": .9, "center_y": .8})
            popup_content.add_widget(self.img_confirm_status)
            popup_content.add_widget(Button(text="Submit",
                                            font_name="font/LibelSuit.ttf",
                                            font_size=self.height / 40,
                                            background_normal="img/widget_100_green.png",
                                            background_down="img/widget_100_green_selected.png",
                                            size_hint_x=.5,
                                            size_hint_y=None, height=self.height / 20,
                                            pos_hint={"center_x": .25, "y": .0},
                                            on_release=self.on_reset_confirm))
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
        else:
            anim_status.stop(img_status)

            img_status.source = "img/ico_fail.png"
            img_status.opacity = 1
            img_status.reload()

'''
    This method checks whether confirmation code for resetting password is correct or not by connecting to server
    Accordingly, it raises warning or connects to server for updating user's password
'''

def on_reset_confirm(self):
    self.img_confirm_status.opacity = 0

    if self.input_key.text == "" or self.input_new_password.text == "":
        self.img_confirm_status.opacity = 1
    else:
        if "TODO":
            Logger.info("tabReset: Password successfully reset")

            self.popup.dismiss()
            self.on_back()
        else:
            self.img_confirm_status.opacity = 1

'''
    This method switches screen to new added one and deletes current screen in order to refresh in case user comes back
'''

def on_back(pages, screen):
    try:
        screen.switch_to(pages[2])
    except:
        screen.current = pages[2].name

    del pages[1]