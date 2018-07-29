"""
eduLive
=======

`eduLive` is a toolbox for main app, it contains necessary methods that EduLive page requires.
"""

from collections import OrderedDict
from functools import partial
from matplotlib import pyplot

from kivy.adapters.listadapter import ListAdapter
from kivy.cache import Cache
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.listview import ListItemButton
from kivy.uix.popup import Popup

from func import database_api, update_clock, image_button
from func.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

__author__ = "Muhammed Yasin Yildirim"
__credits__ = ["Ali Emre Oz"]


def on_pre_enter(self):
    """
    This method updates exam information and imports participants through server.
    :param self: It is for handling class structure.
    :return:
    """

    self.btn_monitor_back = image_button.add_button("data/img/ico_monitor_back.png",
                                                    "data/img/ico_monitor_back_select.png",
                                                    (.05, True),
                                                    {"x": .93, "y": .35},
                                                    partial(on_monitor_backward,
                                                            self
                                                            )
                                                    )

    self.btn_monitor_play = image_button.add_button("data/img/ico_monitor_play.png",
                                                    "data/img/ico_monitor_play_select.png",
                                                    (.05, True),
                                                    {"x": .93, "y": .275},
                                                    partial(on_monitor_play,
                                                            self
                                                            )
                                                    )

    self.btn_monitor_stop = image_button.add_button("data/img/ico_monitor_stop.png",
                                                    "data/img/ico_monitor_stop_select.png",
                                                    (.05, True),
                                                    {"x": .93, "y": .2},
                                                    partial(on_monitor_pause,
                                                            self
                                                            )
                                                    )

    self.btn_monitor_forw = image_button.add_button("data/img/ico_monitor_forw.png",
                                                    "data/img/ico_monitor_forw_select.png",
                                                    (.05, True),
                                                    {"x": .93, "y": .125},
                                                    partial(on_monitor_forward,
                                                            self
                                                            )
                                                    )

    self.btn_monitor_live = image_button.add_button("data/img/ico_monitor_live.png",
                                                    "data/img/ico_monitor_live_select.png",
                                                    (.05, True),
                                                    {"x": .93, "y": .05},
                                                    partial(on_participant_select,  # TODO
                                                            self
                                                            )
                                                    )

    watch = [self.btn_monitor_back,
             self.btn_monitor_play,
             self.btn_monitor_stop,
             self.btn_monitor_forw,
             self.btn_monitor_live
             ]
    for btn in watch:
        btn.disabled = True
        btn.opacity = .25
        self.add_widget(btn)

    self.cipher = Cache.get("config",
                            "cipher"
                            )

    self.data_exam = database_api.getExam(Cache.get("info", "token"),
                                          Cache.get("lect", "code"),
                                          Cache.get("lect", "exam")
                                          )

    self.ids["txt_info_head"].text = "{code} - {name}".format(code=Cache.get("lect", "code"),
                                                              name=Cache.get("lect", "exam")
                                                              )

    self.duration = int(self.data_exam["Duration"])
    self.ids["txt_duration_clock"].text = str(self.duration)

    self.over = False
    self.date_time = Clock.schedule_interval(partial(update_clock.date_time,
                                                     self.ids["txt_clock"]
                                                     ),
                                             1.0
                                             )
    self.min_timer = Clock.schedule_interval(partial(update_clock.min_timer,
                                                     self.ids["txt_duration_clock"],
                                                     self
                                                     ),
                                             60.0
                                             )

    timestamp = self.data_exam["Time"].split(" ")

    self.ids["txt_info_date"].text = timestamp[0]

    self.ids["txt_info_time"].text = timestamp[1]

    self.ids["txt_info_duration"].text = "{dur} mins".format(dur=str(self.duration))

    data = database_api.getCourseStudents(Cache.get("info", "token"),
                                          Cache.get("lect", "code")
                                          )

    with open("data/participants.fay", "w+") as participants:
        std = []
        for d in data:
            std.append("{d0} {d1} - {d2}".format(d0=d[0].title(),
                                                 d1=d[1].title(),
                                                 d2=str(d[2])
                                                 )
                       )
        participants.write(self.cipher.encrypt(str("*[SEAS-NEW-LINE]*".join(std))))
        participants.close()

    participants = open("data/participants.fay", "r")
    self.data_student_list = self.cipher.decrypt(participants.read()).split("*[SEAS-NEW-LINE]*")

    args_converter = lambda row_index, i: {"text": i,
                                           "selected_color": (.843, .82, .82, 1),
                                           "deselected_color": (.57, .67, .68, 1),
                                           "background_down": "data/img/widget_gray_75.png",
                                           "font_name": "data/font/CaviarDreams_Bold.ttf",
                                           "font_size": self.height / 50,
                                           "size_hint_y": None,
                                           "height": self.height / 25
                                           }
    self.ids["list_participants"].adapter = ListAdapter(data=[i.replace("\n", "") for i in self.data_student_list],
                                                        cls=ListItemButton,
                                                        args_converter=args_converter,
                                                        allow_empty_selection=False
                                                        )
    self.ids["list_participants"].adapter.bind(on_selection_change=partial(on_participant_select,
                                                                           self
                                                                           )
                                               )


def on_participant_select(s, dt):
    """
    This method creates keystroke graph and live monitoring player when student is selected.
    :param s: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return:
    """

    def keystroke_graph():
        """
        This method creates keystroke graph.
        :return: It is keystroke graph.
        """

        x_time = [0]  # TODO
        y_rate = [0]  # TODO
        z_tend = [0]  # TODO

        for y in range(1, len(y_rate)):
            z_tend.append((y_rate[y] - y_rate[y - 1]) / 5.0)

        pyplot.plot(x_time,
                    z_tend,
                    color="green"
                    )
        pyplot.xlabel("Time")
        pyplot.ylabel("Keystroke")
        pyplot.grid(True)
        pyplot.axes().set_aspect("equal")
        pyplot.tight_layout()

        return pyplot

    try:
        s.ids["layout_rate"].remove_widget(s.graph_widget)
    except:
        pass
    finally:
        s.graph_widget = FigureCanvasKivyAgg(keystroke_graph().gcf())
        s.ids["layout_rate"].add_widget(s.graph_widget)

    answer_dict = {0: database_api.getKeyloggerData(Cache.get("info", "token"),
                                                    Cache.get("lect", "code"),
                                                    Cache.get("lect", "exam"),
                                                    s.ids["list_participants"].adapter.selection[0].text.split(" - ")[1]
                                                    )
                   }

    for i, j in answer_dict.items():
        ordered_answer_dict = OrderedDict(sorted(j.items()))

    s.ids["slider_monitor"].value_track = True
    s.ids["slider_monitor"].value_track_color = (0, 0, 0, 1)
    s.ids["slider_monitor"].min = 0
    s.ids["slider_monitor"].max = len(ordered_answer_dict) - 1

    def on_value(dt, bright, self=s, dict=ordered_answer_dict):
        """
        This method updates text shown on player according to time being watched.
        :param dt: It is for handling callback input.
        :param bright: It is time being watched.
        :return:
        """

        self.ids["txt_monitor"].text = dict.items()[int(bright)][1].replace("\t",
                                                                            "   "
                                                                            )

    s.ids["slider_monitor"].bind(value=on_value)

    watch = [s.btn_monitor_back,
             s.btn_monitor_play,
             s.btn_monitor_forw,
             s.btn_monitor_live
             ]
    for btn in watch:
        btn.disabled = False
        btn.opacity = 1

    s.btn_monitor_stop.disabled = True
    s.btn_monitor_stop.opacity = .25


def on_monitor_backward(self, dt):
    """
    This method enables rewinding text shown on player.
    :param self: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return:
    """

    if self.ids["slider_monitor"].value - 1 >= 0:
        self.ids["slider_monitor"].value -= 1
    else:
        self.ids["slider_monitor"].value = 0


def on_monitor_forward(self, dt):
    """
    This method enables skipping forward text shown on player.
    :param self: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return:
    """

    try:
        self.ids["slider_monitor"].value += 1
    except:
        self.ids["slider_monitor"].value = 0


def on_monitor_play(self, dt):
    """
    This method enables streaming text on player automatically.
    :param self: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return:
    """

    self.event = Clock.schedule_interval(partial(on_monitor_forward,
                                                 self
                                                 ),
                                         1
                                         )

    watch = [self.btn_monitor_back,
             self.btn_monitor_play,
             self.btn_monitor_forw,
             self.btn_monitor_live
             ]
    for btn in watch:
        btn.disabled = True
        btn.opacity = .25

    self.btn_monitor_stop.disabled = False
    self.btn_monitor_stop.opacity = 1


def on_monitor_pause(self, dt):
    """
    This method enables pausing text stream on player.
    :param self: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return:
    """

    self.event.cancel()

    watch = [self.btn_monitor_back,
             self.btn_monitor_play,
             self.btn_monitor_forw,
             self.btn_monitor_live
             ]
    for btn in watch:
        btn.disabled = False
        btn.opacity = 1

    self.btn_monitor_stop.disabled = True
    self.btn_monitor_stop.opacity = .25


def on_time_add(self):
    """
    This method adds extra time to exam duration through server.
    :param self: It is for handling class structure.
    :return:
    """

    self.duration += 10
    database_api.add_time_to_exam(Cache.get("info", "token"),
                                  Cache.get("lect", "code"),
                                  Cache.get("lect", "exam"),
                                  10
                                  )
    self.ids["txt_duration_clock"].text = str(self.duration)

    duration_prev = self.ids["txt_info_duration"].text
    self.ids["txt_info_duration"].text = "{dur} mins".format(dur=int(duration_prev.split(" ")[0]) + 10)


def on_exam_finish(s):
    """
    This method finishes exam when either time is up or educator requests so.
    :param s: It is for handling class structure.
    :return:
    """

    def on_exam_finish_confirm(self, dt):
        """
        This method changes exam's status to finished through server.
        :param self: It is for handling class structure.
        :param dt: It is for handling callback input.
        :return: It is for switching page back to lectures page.
        """

        popup.dismiss()

        database_api.change_status_of_exam(Cache.get("info", "token"),
                                           Cache.get("lect", "code"),
                                           Cache.get("lect", "exam"),
                                           "finished"
                                           )

        return self.on_lects()

    popup_content = FloatLayout()
    popup = Popup(content=popup_content,
                  separator_color=[140 / 255., 55 / 255., 95 / 255., 1.],
                  size_hint=(None, None),
                  size=(s.width / 5, s.height / 5)
                  )
    popup_content.add_widget(Label(text="Do you want to proceed?",
                                   color=(1, 1, 1, 1),
                                   font_name="data/font/CaviarDreams.ttf",
                                   font_size=s.width / 75,
                                   pos_hint={"center_x": .5, "center_y": .625}
                                   )
                             )
    popup_content.add_widget(Button(text="Yes",
                                    font_name="data/font/LibelSuit.ttf",
                                    font_size=s.height / 40,
                                    background_normal="data/img/widget_green.png",
                                    background_down="data/img/widget_green_select.png",
                                    size_hint_x=None,
                                    width=s.width / 11,
                                    size_hint_y=None,
                                    height=s.height / 25,
                                    pos_hint={"center_x": .25, "y": .01},
                                    on_release=partial(on_exam_finish_confirm,
                                                       s
                                                       )
                                    )
                             )
    popup_content.add_widget(Button(text="No",
                                    font_name="data/font/LibelSuit.ttf",
                                    font_size=s.height / 40,
                                    background_normal="data/img/widget_red.png",
                                    background_down="data/img/widget_red_select.png",
                                    size_hint_x=None,
                                    width=s.width / 11,
                                    size_hint_y=None,
                                    height=s.height / 25,
                                    pos_hint={"center_x": .75, "y": .01},
                                    on_release=popup.dismiss
                                    )
                             )

    if s.over:
        popup.title = "Time Expired"
        s.over = False
    else:
        popup.title = "Finish Exam"

    popup.open()


def on_leave(self):
    """
    This method cancels scheduled methods to update time widgets when user leaves page.
    :param self: It is for handling class structure.
    :return:
    """

    self.date_time.cancel()
    self.min_timer.cancel()
