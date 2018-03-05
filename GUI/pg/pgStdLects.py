from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.listview import ListItemButton
from kivy.adapters.listadapter import ListAdapter

import sys
sys.path.append("../..")

from functools import partial
from GUI.func.check_std_live_exam import check_std_live_exam

def on_pre_enter(self):
    temp_login = open("data/temp_login.seas", "r")
    self.data_login = temp_login.readlines()

    self.data = []

    # data_lectures = DatabaseAPI.getLecturerCourses("http://10.50.81.24:8888", "istanbul sehir university", self.data_login[0].replace("\n", ""))
    data_lectures = [["0", "TODO", "TODO"]]
    for i in data_lectures:
        self.data.append(i[1] + "_" + i[0] + "_" + i[2])

    list_dropdown = DropDown()

    for lect in self.data:
        btn_lect = Button(text=" ".join(lect.split("_")[:2]).upper(),
                          color=(0,0,0,1),
                          font_name="font/LibelSuit.ttf",
                          font_size=self.height / 40,
                          background_normal="img/widget_75_gray.png",
                          background_down="img/widget_100_gray.png",
                          size_hint_y=None, height=self.height / 10)
        btn_lect.bind(on_release=lambda btn_lect: on_lect_select(self, list_dropdown, btn_lect.text))
        list_dropdown.add_widget(btn_lect)

    btn_main = Button(text="Select A Lecture",
                      font_name="font/LibelSuit.ttf",
                      font_size=self.height / 40,
                      background_normal="img/widget_75_black.png",
                      background_down="img/widget_75_gray.png",
                      size_hint=(.2, .1),
                      pos=(self.x, self.height * 8 / 10))
    btn_main.bind(on_release=list_dropdown.open)

    list_dropdown.bind(on_select=lambda instance, x: setattr(btn_main, "text", x))

    self.add_widget(btn_main)

    Clock.schedule_interval(partial(check_std_live_exam, self), 1.0 / 10.0)

def on_lect_select(self, dropdown, txt):
    dropdown.select(txt)

    self.ids["btn_exams"].disabled = False
    self.ids["btn_personal_statistics"].disabled = False

    self.ids["txt_hint"].opacity = 0

    self.ids["txt_lect_code"].opacity = 1
    self.ids["txt_lect_name"].opacity = 1

    self.ids["layout_exams"].opacity = 1

    for lect in self.data:
        if txt in " ".join(lect.split("_")).upper():
            self.ids["txt_lect_code"].text = txt
            self.ids["txt_lect_name"].text = " ".join(lect.split("_")[2:]).title()

    # self.data_exams = DatabaseAPI...
    self.data_exams = ["TODO"]

    args_converter = lambda row_index, i: {"text": i,
                                           "background_normal": "img/widget_75_black_crop.png",
                                           "font_name": "font/CaviarDreams_Bold.ttf", "font_size": self.height / 25,
                                           "size_hint_y": None, "height": self.height / 10}
    self.ids["list_exams"].adapter = ListAdapter(data=[i for i in self.data_exams], cls=ListItemButton,
                                                 args_converter=args_converter, allow_empty_selection=False)
    self.ids["list_exams"].adapter.bind(on_selection_change=self.on_exam_selected)

def on_exam_selected(self):
    self.ids["img_info_top"].opacity = 0.5
    self.ids["img_info_body"].opacity = 0.5
    self.ids["txt_info_head"].opacity = 1
    self.ids["txt_info_head"].text = self.ids["list_exams"].adapter.selection[0].text

    self.ids["txt_date_head"].opacity = 1
    self.ids["txt_date_body"].opacity = 1
    self.ids["txt_date_body"].text = "TODO"

    self.ids["txt_time_head"].opacity = 1
    self.ids["txt_time_body"].opacity = 1
    self.ids["txt_time_body"].text = "TODO"

    self.ids["txt_options_head"].opacity = 1
    self.ids["btn_exam_statistics"].opacity = 1

def on_personal_exam_statistics(self):
    pass
    # TODO: Personal Exam Statistics