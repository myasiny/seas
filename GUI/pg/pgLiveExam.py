from kivy.clock import Clock
from kivy.uix.listview import ListItemButton
from kivy.adapters.listadapter import ListAdapter

import sys
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

    Clock.schedule_interval(partial(date_time, self.ids["txt_clock"]), 1.0)
    Clock.schedule_interval(partial(min_timer, self.ids["txt_duration_clock"], self), 60.0)

    # self.ids["txt_info_date"].text = DatabaseAPI...

    # self.ids["txt_info_time"].text = DatabaseAPI...

    self.ids["txt_info_duration"].text = "%d mins" % self.duration

    # data = DatabaseAPI...
    data = [["TODO", 0, "0.0.0.0"]]

    with open("data/temp_student_list.seas", "w+") as temp_student_list:
        for d in data:
            temp_student_list.write(d[2] + " - " + str(d[1]) + " - " + d[0] + "\n")
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
    pass