from KivyCalendar import CalendarWidget
from kivy.garden import *

import sys
sys.path.append("../..")

from Server import DatabaseAPI

def on_pre_enter(self):
    temp_selected_lect = open("data/temp_selected_lect.seas", "r")
    data_selected_lect = temp_selected_lect.readlines()

    self.ids["txt_lect_code"].text = data_selected_lect[0].replace("\n", "")
    self.ids["txt_lect_name"].text = data_selected_lect[1]

    self.add_widget(CalendarWidget(font_name="font/LibelSuit.ttf",
                                   font_size=self.height / 40,
                                   size_hint=(.3, .3),
                                   pos_hint={"center_x": .75, "center_y": .6}))