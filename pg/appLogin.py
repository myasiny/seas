"""
appLogin
========

`appLogin` is a toolbox for main app, it contains necessary methods that AppLogin page requires.
"""

import os
import platform
from functools import partial

from kivy.app import App
from kivy.cache import Cache
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from func import image_button, check_connection, database_api, round_image, text_button
from func.garden.progressspinner import ProgressSpinner

__author__ = "Muhammed Yasin Yildirim"


def load_string(f):
    """
    This method applies design by reading given file.
    :param f: It is name of design file without extension.
    :return:
    """

    with open("css/{filename}.seas".format(filename=f), "r") as design:
        Builder.load_string(design.read())


def on_pre_enter(self):
    """
    This method adds image button to quit and text button to reset password.
    :param self: It is for handling class structure.
    :return:
    """

    self.ids["layout_menubar"].add_widget(image_button.add_button("data/img/ico_quit.png",
                                                                  "data/img/ico_quit_select.png",
                                                                  .075,
                                                                  {"x": .925, "y": 0},
                                                                  self.on_quit
                                                                  )
                                          )

    self.add_widget(text_button.add_button("Reset Password",
                                           "data/font/CaviarDreams.ttf",
                                           (.3, .025),
                                           {"center_x": .5, "y": .175},
                                           self.on_reset
                                           )
                    )


def on_enter(self):
    """
    This method schedules trigger for checking status of server connection.
    :param self: It is for handling class structure.
    :return:
    """

    Clock.schedule_once(partial(check_connection.is_alive,
                                self.ids["ico_connection"]
                                )
                        )
    self.check_connection = Clock.schedule_interval(partial(check_connection.is_alive,
                                                            self.ids["ico_connection"]
                                                            ),
                                                    5.0
                                                    )


# def authorization(name, pasw, dt):
#     """
#     This method checks if user credentials are valid through server.
#     :param name: It is username.
#     :param pasw: It is password.
#     :param dt: It is for handling callback input.
#     :return: It is list of information of user logged in.
#     """
#
#     data = database_api.signIn(name,
#                                pasw
#                                )
#
#     return data


def on_login(self, pages, screen, edu_lects, std_lects):
    """
    This method creates threading for logging in and updates GUI accordingly.
    :param self: It is for handling class structure.
    :param pages: It is list of pages.
    :param screen: It is screen manager.
    :param edu_lects: It is class of lectures page for educators.
    :param std_lects: It is class of lectures page for students.
    :return:
    """

    btn_login = self.ids["btn_login"]
    btn_login.disabled = True

    ico_status = self.ids["ico_status"]

    ico_spinner = ProgressSpinner(size_hint=(.05, .05),
                                  pos_hint={"center_x": .65, "center_y": .8}
                                  )
    self.add_widget(ico_spinner)

    input_username = self.ids["input_username"].text
    input_password = self.ids["input_password"].text

    if not (input_username.strip() or input_password.strip()):
        self.remove_widget(ico_spinner)

        ico_status.source = "data/img/ico_status_warning.png"
        ico_status.opacity = 1
        ico_status.reload()

        btn_login.disabled = False
    else:
        try:
            # data = Clock.schedule_once(partial(authorization,
            #                                    input_username,
            #                                    input_password
            #                                    )
            #                            )

            data = database_api.signIn(input_username,
                                       input_password
                                       )
        except:
            data = None

        if isinstance(data, list):
            self.remove_widget(ico_spinner)

            ico_status.source = "data/img/ico_status_success.png"
            ico_status.opacity = 1
            ico_status.reload()

            btn_login.disabled = False

            slot = ["nick",
                    "name",
                    "surname",
                    "id",
                    "role",
                    "mail",
                    "dept",
                    "uni",
                    "token"
                    ]

            for i in range(9):
                Cache.append("info",
                             slot[i],
                             data[i]
                             )

            Cache.append("info",
                         "pict",
                         round_image.update_image()
                         )

            if data[4] != "student":
                pages.append(edu_lects(name="EduLects"))
            else:
                pages.append(std_lects(name="StdLects"))

            try:
                screen.switch_to(pages[2])
            except:
                screen.current = pages[2].name
            finally:
                del pages[1]
        else:
            self.remove_widget(ico_spinner)

            ico_status.source = "data/img/ico_status_fail.png"
            ico_status.opacity = 1
            ico_status.reload()

            btn_login.disabled = False


def on_quit(self):
    """
    This method creates pop-up for user to confirm or cancel quit request.
    :param self: It is for handling class structure.
    :return:
    """

    def confirm(dt):
        """
        This method restores operating system settings to default if user is using Linux and stops app.
        :param dt: It is for handling callback input.
        :return:
        """

        database_api.signOut(Cache.get("info",
                                       "token"
                                       ),
                             Cache.get("info",
                                       "nick"
                                       )
                             )

        if platform.system() == "Linux":
            os.system("sh func/sh/restore.sh")

        App.get_running_app().stop()

    popup_content = FloatLayout()
    popup = Popup(title="Quit",
                  content=popup_content,
                  separator_color=[140 / 255., 55 / 255., 95 / 255., 1.],
                  size_hint=(None, None),
                  size=(self.width / 5, self.height / 5)
                  )
    popup_content.add_widget(Label(text="Are you sure?",
                                   color=(1, 1, 1, 1),
                                   font_name="data/font/CaviarDreams.ttf",
                                   font_size=self.width / 50,
                                   pos_hint={"center_x": .5, "center_y": .625}
                                   )
                             )
    popup_content.add_widget(Button(text="Yes",
                                    font_name="data/font/LibelSuit.ttf",
                                    font_size=self.height / 40,
                                    background_normal="data/img/widget_green.png",
                                    background_down="data/img/widget_green_select.png",
                                    size_hint_x=.5,
                                    size_hint_y=None,
                                    height=self.height / 25,
                                    pos_hint={"center_x": .25, "y": 0},
                                    on_release=confirm
                                    )
                             )
    popup_content.add_widget(Button(text="No",
                                    font_name="data/font/LibelSuit.ttf",
                                    font_size=self.height / 40,
                                    background_normal="data/img/widget_red.png",
                                    background_down="data/img/widget_red_select.png",
                                    size_hint_x=.5,
                                    size_hint_y=None,
                                    height=self.height / 25,
                                    pos_hint={"center_x": .75, "y": 0},
                                    on_release=popup.dismiss
                                    )
                             )
    popup.open()


def on_leave(self):
    """
    This method cancels scheduled method to check server connection when user leaves page.
    :param self: It is for handling class structure.
    :return:
    """

    self.check_connection.cancel()
