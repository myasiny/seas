import sys

sys.path.append("../..")

from Server import DatabaseAPI
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.listview import ListItemButton
from kivy.adapters.listadapter import ListAdapter

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

    self.ids["txt_lect_code"].opacity = 1
    self.ids["txt_lect_name"].opacity = 1

    for lect in data:
        if txt in " ".join(lect.split("_")).upper():
            self.ids["txt_lect_code"].text = txt
            self.ids["txt_lect_name"].text = " ".join(lect.split("_")[2:]).title()
            break

    self.ids["img_info_top"].opacity = 0
    self.ids["img_info_body"].opacity = 0
    self.ids["txt_info_head"].opacity = 0
    self.ids["txt_info_head"].text = "..."

    self.ids["txt_status_head"].opacity = 0
    self.ids["txt_status_body"].opacity = 0
    self.ids["txt_status_body"].text = "..."

    self.ids["txt_options_head"].opacity = 0
    self.ids["btn_exam_edit"].opacity = 0
    self.ids["btn_exam_delete"].opacity = 0
    self.ids["btn_exam_start"].opacity = 0

    on_exams(self)

def on_exams(self):
    self.ids["layout_exams"].opacity = 1
    self.ids["layout_participants"].opacity = 0

    args_converter = lambda row_index, i: {"text": i,
                                           "background_normal": "img/widget_75_black_crop.png",
                                           "font_name": "font/CaviarDreams_Bold.ttf", "font_size": self.height/25,
                                           "size_hint_y": None, "height": self.height/10}
    self.ids["list_exams"].adapter = ListAdapter(data=[i for i in ["Quiz 1","Quiz 2","Midterm 1","Make Up","Quiz 3","Final"]], cls=ListItemButton,
                                                 args_converter=args_converter, allow_empty_selection=False)
    self.ids["list_exams"].adapter.bind(on_selection_change=self.on_exam_selected)

def on_exam_selected(self):
    self.ids["img_info_top"].opacity = 0.5
    self.ids["img_info_body"].opacity = 0.5
    self.ids["txt_info_head"].opacity = 1
    self.ids["txt_info_head"].text = self.ids["list_exams"].adapter.selection[0].text

    self.ids["txt_status_head"].opacity = 1
    self.ids["txt_status_body"].opacity = 1
    self.ids["txt_status_body"].text = "Unknown"

    self.ids["txt_options_head"].opacity = 1
    self.ids["btn_exam_edit"].opacity = 1
    self.ids["btn_exam_delete"].opacity = 1
    self.ids["btn_exam_start"].opacity = 1

def on_participants(self):
    self.ids["layout_exams"].opacity = 0
    self.ids["layout_participants"].opacity = 1

def on_class_statistics(self):
    pass # TODO: Re-direct To Class Statistics