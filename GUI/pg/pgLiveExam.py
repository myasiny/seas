from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.listview import ListItemButton
from kivy.uix.floatlayout import FloatLayout
from kivy.adapters.listadapter import ListAdapter

import sys, collections
sys.path.append("../..")

from functools import partial
from GUI.func import database_api
from GUI.func.date_time import date_time, min_timer

def on_pre_enter(self):
    temp_selected_lect = open("data/temp_selected_lect.seas", "r")
    self.data_selected_lect = temp_selected_lect.readlines()

    self.ids["txt_info_head"].text = self.data_selected_lect[0].replace("\n", " ") + "- " + self.data_selected_lect[2]

    self.duration = 0
    self.ids["txt_duration_clock"].text = str(self.duration)

    self.over = False
    Clock.schedule_interval(partial(date_time, self.ids["txt_clock"]), 1.0)
    Clock.schedule_interval(partial(min_timer, self.ids["txt_duration_clock"], self), 60.0)

    # self.ids["txt_info_date"].text = DatabaseAPI...

    # self.ids["txt_info_time"].text = DatabaseAPI...

    self.ids["txt_info_duration"].text = "%d mins" % self.duration

    self.ids["btn_monitor_back"].disabled = True
    self.ids["btn_monitor_play"].disabled = True
    self.ids["btn_monitor_pause"].disabled = True
    self.ids["btn_monitor_forward"].disabled = True
    self.ids["btn_monitor_live"].disabled = True

    self.ids["img_monitor_back"].opacity = 0.25
    self.ids["img_monitor_play"].opacity = 0.25
    self.ids["img_monitor_pause"].opacity = 0.25
    self.ids["img_monitor_forward"].opacity = 0.25
    self.ids["img_monitor_live"].opacity = 0.25

    # data = DatabaseAPI...
    data = [["TODO", 0, "0.0.0.0"]]

    with open("data/temp_student_list.seas", "w+") as temp_student_list:
        for d in data:
            temp_student_list.write("{ip} > {no} > {name}".format(ip=d[2], no=str(d[1]), name=d[0]) + "\n")
        temp_student_list.close()

    temp_student_list = open("data/temp_student_list.seas", "r")
    self.data_student_list = temp_student_list.readlines()

    args_converter = lambda row_index, i: {"text": i,
                                           "background_normal": "img/widget_75_black_crop.png",
                                           "font_name": "font/CaviarDreams_Bold.ttf", "font_size": self.height / 50,
                                           "size_hint_y": None, "height": self.height / 25}
    self.ids["list_participants"].adapter = ListAdapter(data=[i.replace("\n", "") for i in self.data_student_list],
                                                        cls=ListItemButton, args_converter=args_converter,
                                                        allow_empty_selection=False)
    self.ids["list_participants"].adapter.bind(on_selection_change=self.on_participant_selected)

def on_participant_selected(self):
    self.x_time = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110]
    self.y_rate = [10, 22, 35, 35, 35, 35, 42, 46, 87, 90, 90, 90, 90, 150, 200, 200, 205, 206, 210, 210, 210, 210, 210]
    self.z_tend = [0]

    # self.answer_dict = DatabaseAPI...
    self.answer_dict = {0: {0: "", 1: "TODO"}}

    for i, j in self.answer_dict.items():
        self.ordered_answer_dict = collections.OrderedDict(sorted(j.items()))
    self.ordered_answer_dict_len = len(self.ordered_answer_dict)

    self.ids["slider_monitor"].value_track = True
    self.ids["slider_monitor"].value_track_color = (0,0,0,1)
    self.ids["slider_monitor"].min = 0
    self.ids["slider_monitor"].max = self.ordered_answer_dict_len - 1
    self.ids["slider_monitor"].bind(value=self.on_value)

    self.ids["btn_monitor_back"].disabled = False
    self.ids["btn_monitor_play"].disabled = False
    self.ids["btn_monitor_pause"].disabled = True
    self.ids["btn_monitor_forward"].disabled = False
    self.ids["btn_monitor_live"].disabled = False

    self.ids["img_monitor_back"].opacity = 1
    self.ids["img_monitor_play"].opacity = 1
    self.ids["img_monitor_pause"].opacity = 0.25
    self.ids["img_monitor_forward"].opacity = 1
    self.ids["img_monitor_live"].opacity = 1

    pass
    # TODO: Participant Selected

def on_value(self, bright):
    self.ids["txt_monitor"].text = self.ordered_answer_dict.items()[int(bright)][1].replace("\t", "   ")

def on_monitor_backward(self):
    if self.ids["slider_monitor"].value - 1 >= 0:
        self.ids["slider_monitor"].value -= 1
    else:
        self.ids["slider_monitor"].value = 0

def on_monitor_play(self):
    self.event = Clock.schedule_interval(self.on_monitor_forward, 0.5)

    self.ids["btn_monitor_back"].disabled = True
    self.ids["btn_monitor_play"].disabled = True
    self.ids["btn_monitor_pause"].disabled = False
    self.ids["btn_monitor_forward"].disabled = True
    self.ids["btn_monitor_live"].disabled = True

    self.ids["img_monitor_back"].opacity = 0.25
    self.ids["img_monitor_play"].opacity = 0.25
    self.ids["img_monitor_pause"].opacity = 1
    self.ids["img_monitor_forward"].opacity = 0.25
    self.ids["img_monitor_live"].opacity = 0.25

def on_monitor_pause(self):
    self.event.cancel()

    self.ids["btn_monitor_back"].disabled = False
    self.ids["btn_monitor_play"].disabled = False
    self.ids["btn_monitor_pause"].disabled = True
    self.ids["btn_monitor_forward"].disabled = False
    self.ids["btn_monitor_live"].disabled = False

    self.ids["img_monitor_back"].opacity = 1
    self.ids["img_monitor_play"].opacity = 1
    self.ids["img_monitor_pause"].opacity = 0.25
    self.ids["img_monitor_forward"].opacity = 1
    self.ids["img_monitor_live"].opacity = 1

def on_monitor_forward(self):
    try:
        self.ids["slider_monitor"].value += 1
    except:
        self.ids["slider_monitor"].value = 0

def on_monitor_live(self):
    pass
    # TODO: Live Monitoring

def on_add_time(self):
    self.duration += 10
    self.ids["txt_info_duration"].text = "%d mins" % self.duration
    self.ids["txt_duration_clock"].text = str(self.duration)

def on_finish_exam(self):
    popup_content = FloatLayout()
    self.popup = Popup(content=popup_content, separator_color=[140 / 255., 55 / 255., 95 / 255., 1.],
                       size_hint=(None, None), size=(self.width / 5, self.height / 5))
    popup_content.add_widget(Label(text="Do you want to proceed?", color=(1, 1, 1, 1),
                                   font_name="font/CaviarDreams.ttf", font_size=self.width / 75,
                                   pos_hint={"center_x": .5, "center_y": .625}))
    popup_content.add_widget(Button(text="Yes",
                                    font_name="font/LibelSuit.ttf",
                                    font_size=self.height / 40,
                                    background_normal="img/widget_100_green.png",
                                    background_down="img/widget_100_green_selected.png",
                                    size_hint_x=None, width=self.width / 11,
                                    size_hint_y=None, height=self.height / 25,
                                    pos_hint={"center_x": .25, "y": .01},
                                    on_release=self.on_lects))
    popup_content.add_widget(Button(text="No",
                                    font_name="font/LibelSuit.ttf",
                                    font_size=self.height / 40,
                                    background_normal="img/widget_100_red.png",
                                    background_down="img/widget_100_red_selected.png",
                                    size_hint_x=None, width=self.width / 11,
                                    size_hint_y=None, height=self.height / 25,
                                    pos_hint={"center_x": .75, "y": .01},
                                    on_release=self.popup.dismiss))
    if self.over:
        self.popup.title = "Time Expired"
    else:
        self.popup.title = "Finish Exam"
    self.popup.open()

def on_lects(self):
    self.popup.dismiss()
    # TODO: Finish Exam