import sys
sys.path.append("../..")

from Server import DatabaseAPI
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

def on_pre_enter(self):
    data = ["Cs_361_Software","Eecs_202_Basic_Digital_Communication","Engr_101_Computer_Skills","Life_101_Biology"]
    #TODO: data = DatabaseAPI...

    list_dropdown = DropDown()

    for lect in data:
        btn_lect = Button(text=" ".join(lect.split("_")[:2]).upper(),
                          color=(0,0,0,1),
                          font_name="font/LibelSuit.ttf",
                          font_size=self.height / 40,
                          background_normal="img/widget_75_gray.png",
                          background_down="img/widget_100_gray.png",
                          size_hint_y=None, height=self.height / 10)
        btn_lect.bind(on_release=lambda btn_lect: on_lect_select(self, data, list_dropdown, btn_lect.text))
        list_dropdown.add_widget(btn_lect)

    btn_main = Button(text="Select a Lecture",
                      font_name="font/LibelSuit.ttf",
                      font_size=self.height / 40,
                      background_normal="img/widget_75_black.png",
                      background_down="img/widget_75_gray.png",
                      size_hint=(.2, .1),
                      pos=(self.x, self.height * 8 / 10))
    btn_main.bind(on_release=list_dropdown.open)

    list_dropdown.bind(on_select=lambda instance, x: setattr(btn_main, "text", x))

    self.add_widget(btn_main)

def on_lect_select(self, data, dropdown, txt):
    dropdown.select(txt)

    self.ids["btn_exams"].disabled = False
    self.ids["btn_participants"].disabled = False
    self.ids["btn_class_statistics"].disabled = False

    self.ids["txt_hint"].opacity = 0

    txt_lect_code = self.ids["txt_lect_code"]
    txt_lect_code.opacity = 1
    txt_lect_name = self.ids["txt_lect_name"]
    txt_lect_name.opacity = 1

    for lect in data:
        if txt in " ".join(lect.split("_")).upper():
            txt_lect_code.text = txt
            txt_lect_name.text = " ".join(lect.split("_")[2:]).title()
            break

    #TODO: When Lecture Selected