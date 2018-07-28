"""
eduStats
========

`eduStats` is a toolbox for main app, it contains necessary methods that EduStats page requires.
"""

from functools import partial

from kivy.clock import Clock

from func import check_connection, image_button

__author__ = "Muhammed Yasin Yildirim"


def on_pre_enter(self):
    """
    This method adds image button to go back as well as it updates profile picture widget and so on.
    :param self: It is for handling class structure.
    :return:
    """

    try:
        self.check_connection.cancel()
    except:
        Clock.schedule_once(partial(check_connection.is_alive,
                                    self.ids["ico_connection"]
                                    )
                            )
        self.check_connection = Clock.schedule_interval(partial(check_connection.is_alive,
                                                                self.ids["ico_connection"]
                                                                ),
                                                        5.0
                                                        )

    layout_menubar = self.ids["layout_menubar"]
    layout_menubar.remove_widget(self.btn_logout)
    layout_menubar.add_widget(image_button.add_button("data/img/ico_back.png",
                                                      "data/img/ico_back_select.png",
                                                      .075,
                                                      {"x": 0, "y": 0},
                                                      self.on_back
                                                      )
                              )
