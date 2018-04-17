"""
appReset
========

`appReset` is a toolbox for main app, it contains necessary methods that AppReset page requires.
"""

import threading

from kivy.clock import mainthread
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from func import image_button, text_button
from func.garden.progressspinner import ProgressSpinner

__author__ = "Muhammed Yasin Yildirim"


def on_pre_enter(self):
    """
    This method adds image button to quit and text button to go back.
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

    self.add_widget(text_button.add_button("< Back",
                                           "data/font/CaviarDreams.ttf",
                                           (.3, .025),
                                           {"center_x": .5, "y": .175},
                                           self.on_back
                                           )
                    )


def on_reset(s):
    """
    This method creates threading to handle reset process in background.
    :param s: It is for handling class structure.
    :return:
    """

    def on_reset_confirm(self=s):
        """
        This method TODO
        :return:
        """

        # ico_status_confirm.opacity = 0
        #
        # if not (input_key.text.strip() or input_new_password.text.strip()):
        #     ico_status_confirm.opacity = 1
        # else:
        #     if TODO:
        #         popup.dismiss()
        #         self.on_back()
        #     else:
        #         ico_status_confirm.opacity = 1

        pass

    @mainthread
    def authorize(self=s):
        """
        This method checks if user credentials are valid through server and creates confirmation pop-up accordingly.
        :return: It is for terminating thread.
        """

        btn_reset = self.ids["btn_reset"]
        btn_reset.disabled = True

        ico_status = self.ids["ico_status"]

        ico_spinner = ProgressSpinner(size_hint=(.05, .05),
                                      pos_hint={"center_x": .65, "center_y": .8}
                                      )
        self.add_widget(ico_spinner)

        input_username = self.ids["input_username"].text
        input_email = self.ids["input_email"].text

        if not (input_username.strip() or input_email.strip()):
            self.remove_widget(ico_spinner)

            ico_status.source = "data/img/ico_status_warning.png"
            ico_status.opacity = 1
            ico_status.reload()

            btn_reset.disabled = False
        else:
            try:
                data = None  # TODO
            except:
                data = None

            if isinstance(data, list):
                self.remove_widget(ico_spinner)

                ico_status.source = "data/img/ico_status_success.png"
                ico_status.opacity = 1
                ico_status.reload()

                btn_reset.disabled = False

                popup_content = FloatLayout()
                popup = Popup(title="Reset Password",
                              content=popup_content,
                              separator_color=[140 / 255., 55 / 255., 95 / 255., 1.],
                              size_hint=(None, None),
                              size=(self.width / 3, self.height / 3)
                              )
                input_key = TextInput(hint_text="Confirmation Key",
                                      write_tab=False,
                                      multiline=False,
                                      font_name="data/font/CaviarDreams_Bold.ttf",
                                      font_size=self.height / 36,
                                      background_normal="data/img/widget_gray_75.png",
                                      background_active="data/img/widget_purple_75_select.png",
                                      background_disabled_normal="data/img/widget_black_75.png",
                                      padding_y=[self.height / 36, 0],
                                      size_hint=(.9, .3),
                                      pos_hint={"center_x": .5, "center_y": .8}
                                      )
                popup_content.add_widget(input_key)
                input_new_password = TextInput(hint_text="New Password",
                                               write_tab=False,
                                               multiline=False,
                                               password=True,
                                               font_name="data/font/CaviarDreams_Bold.ttf",
                                               font_size=self.height / 36,
                                               background_normal="data/img/widget_gray_75.png",
                                               background_active="data/img/widget_purple_75_select.png",
                                               background_disabled_normal="data/img/widget_black_75.png",
                                               padding_y=[self.height / 36, 0],
                                               size_hint=(.9, .3),
                                               pos_hint={"center_x": .5, "center_y": .4}
                                               )
                popup_content.add_widget(input_new_password)
                ico_status_confirm = Image(source="data/img/ico_status_wrong.png",
                                           allow_stretch=True,
                                           opacity=0,
                                           size_hint=(.15, .15),
                                           pos_hint={"center_x": .9, "center_y": .8}
                                           )
                popup_content.add_widget(ico_status_confirm)
                popup_content.add_widget(Button(text="Submit",
                                                font_name="data/font/LibelSuit.ttf",
                                                font_size=self.height / 40,
                                                background_normal="data/img/widget_green.png",
                                                background_down="data/img/widget_green_select.png",
                                                size_hint_x=.5,
                                                size_hint_y=None,
                                                height=self.height / 20,
                                                pos_hint={"center_x": .25, "y": .0},
                                                on_release=on_reset_confirm)
                                         )
                popup_content.add_widget(Button(text="Cancel",
                                                font_name="data/font/LibelSuit.ttf",
                                                font_size=self.height / 40,
                                                background_normal="data/img/widget_red.png",
                                                background_down="data/img/widget_red_select.png",
                                                size_hint_x=.5,
                                                size_hint_y=None,
                                                height=self.height / 20,
                                                pos_hint={"center_x": .75, "y": .0},
                                                on_release=popup.dismiss)
                                         )
                popup.open()
            else:
                self.remove_widget(ico_spinner)

                ico_status.source = "data/img/ico_status_fail.png"
                ico_status.opacity = 1
                ico_status.reload()

                btn_reset.disabled = False

            return

    authorization = threading.Thread(target=authorize)
    authorization.daemon = True
    authorization.start()


def on_back(pages, screen):
    """
    This method switches current screen to specified one.
    :param pages: It is list of pages.
    :param screen: It is screen manager.
    :return:
    """

    try:
        screen.switch_to(pages[2])
    except:
        screen.current = pages[2].name
    finally:
        del pages[1]
