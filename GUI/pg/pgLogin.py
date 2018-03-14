from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from functools import partial
from GUI.func import database_api
from GUI.func.check_connection import check_connection

'''
    This method loads design file for given page
'''

def load_string(name):
    with open("css/%s.seas" % name, "r") as design:
        Builder.load_string(design.read())

    Logger.info("pg%s: Design successfully applied" % name.title())

'''
    This method triggers check_connection every 5 seconds
'''

def on_enter(self):
    Clock.schedule_interval(partial(check_connection, self.ids["img_connection"]), 5.0)

'''
    This method checks whether username and password are provided or not
    Accordingly, it raises warning or connects to server for logging in
    If credentials are correct, it directs to either PgLects or PgStdLects according to account type
    If not, it raises error and process for logging in fails
'''

def on_login(self, pages, screen, pgEdu, pgStd):
    btn_login = self.ids["btn_login"]
    btn_login.disabled = True

    img_status = self.ids["img_status"]
    img_status.source = "img/ico_loading.gif"
    img_status.opacity = 0
    img_status.reload()

    anim_status = Animation(opacity=1, duration=1)
    anim_status.start(img_status)

    input_username = self.ids["input_username"].text
    input_password = self.ids["input_password"].text
    if input_username == "" or input_password == "":
        anim_status.stop(img_status)

        img_status.source = "img/ico_warning.png"
        img_status.opacity = 1
        img_status.reload()

        btn_login.disabled = False

        Logger.info("pgLogin: Required fields are not filled")
    else:
        try:
            data = database_api.signIn(input_username, input_password)

            Logger.info("pgLogin: User credentials successfully sent to server")
        except:
            data = None

            Logger.error("pgLogin: Server is not reachable")

        if isinstance(data, list):
            anim_status.stop(img_status)

            img_status.source = "img/ico_success.png"
            img_status.opacity = 1
            img_status.reload()

            btn_login.disabled = False

            with open("data/temp_login.seas", "w+") as temp_login:
                for d in data:
                    temp_login.write(str(d) + "\n")
                temp_login.close()

            if data[4] != "student":
                pages.append(pgEdu(name="PgLects"))
            else:
                pages.append(pgStd(name="PgStdLects"))

            try:
                screen.switch_to(pages[2])
            except:
                screen.current = pages[2].name

            del pages[1]

            Logger.info("pgLogin: User successfully logged in")
        else:
            anim_status.stop(img_status)

            img_status.source = "img/ico_fail.png"
            img_status.opacity = 1
            img_status.reload()

            btn_login.disabled = False

            Logger.info("pgLogin: User couldn't log in due to incorrect credentials")

'''
    This method asks user to confirm whether he or she wants to quit or not
    Accordingly, program stops running or confirmation pop-up disappears
'''

def on_quit(self):
    Logger.info("quit: This is sad :(")

    popup_content = FloatLayout()
    popup = Popup(title="Quit",
                  content=popup_content, separator_color=[140 / 255., 55 / 255., 95 / 255., 1.],
                  size_hint=(None, None), size=(self.width / 5, self.height / 5))
    popup_content.add_widget(Label(text="Are you sure?", color=(1,1,1,1),
                                   font_name="font/CaviarDreams.ttf", font_size=self.width / 50,
                                   pos_hint={"center_x": .5, "center_y": .625}))
    popup_content.add_widget(Button(text="Yes",
                                    font_name="font/LibelSuit.ttf",
                                    font_size=self.height / 40,
                                    background_normal="img/widget_100_green.png",
                                    background_down="img/widget_100_green_selected.png",
                                    size_hint_x=None, width=self.width/ 11,
                                    size_hint_y=None, height=self.height / 25,
                                    pos_hint={"center_x": .25, "y": .01},
                                    on_release=App.get_running_app().stop))
    popup_content.add_widget(Button(text="No",
                                    font_name="font/LibelSuit.ttf",
                                    font_size=self.height / 40,
                                    background_normal="img/widget_100_red.png",
                                    background_down="img/widget_100_red_selected.png",
                                    size_hint_x=None, width=self.width/ 11,
                                    size_hint_y=None, height=self.height / 25,
                                    pos_hint={"center_x": .75, "y": .01},
                                    on_release=popup.dismiss))
    popup.open()