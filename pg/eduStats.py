"""
eduStats
========

`eduStats` is a toolbox for main app, it contains necessary methods that EduStats page requires.
"""

from functools import partial
from matplotlib import pyplot

from kivy.cache import Cache
from kivy.clock import Clock

from func import check_connection
from func.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

__author__ = "Muhammed Yasin Yildirim"


def on_pre_enter(self):
    """
    This method adds image button to go back as well as it updates profile picture widget and so on.
    :param self: It is for handling class structure.
    :return:
    """

    # layout_menubar = self.ids["layout_menubar"]
    # layout_menubar.remove_widget(self.btn_logout)
    # layout_menubar.add_widget(image_button.add_button("data/img/ico_back.png",
    #                                                   "data/img/ico_back_select.png",
    #                                                   .075,
    #                                                   {"x": 0, "y": 0},
    #                                                   self.on_back
    #                                                   )
    #                           )

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

    info_type = Cache.get("data",
                          "type"
                          )
    self.ids["txt_type"].text = info_type.title() + " Statistics"

    info_select = Cache.get("data",
                            "select"
                            )
    self.ids["txt_select"].text = info_select

    pyplot.figure(1)
    pyplot.bar([5, 10, 15],
               [3, 6, 9],
               color="blue"
               )
    pyplot.xlabel("Y")
    pyplot.ylabel("X")
    pyplot.grid(True)
    pyplot.axes().set_aspect("equal")
    pyplot.tight_layout()
    self.ids["layout_graph_top_right"].add_widget(FigureCanvasKivyAgg(pyplot.gcf()))

    pyplot.figure(2)
    pyplot.plot([5, 10, 15],
                [3, 6, 9],
                color="green"
                )
    pyplot.xlabel("Y")
    pyplot.ylabel("X")
    pyplot.grid(True)
    pyplot.axes().set_aspect("equal")
    pyplot.tight_layout()
    self.ids["layout_graph_bottom_right"].add_widget(FigureCanvasKivyAgg(pyplot.gcf()))

    pyplot.figure(3)
    pyplot.pie([5, 10, 15],
               labels=["good", "none", "bad"],
               explode=(0.1, 0, 0)
               )
    pyplot.grid(True)
    pyplot.axes().set_aspect("equal")
    pyplot.tight_layout()
    self.ids["layout_graph_bottom_left"].add_widget(FigureCanvasKivyAgg(pyplot.gcf()))

    self.ids["txt_analysis"].text = "TODO"
