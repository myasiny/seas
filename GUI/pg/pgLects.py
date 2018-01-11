from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.listview import ListItemButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.adapters.listadapter import ListAdapter

import os, sys
sys.path.append("../..")

from functools import partial
from Server import DatabaseAPI

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
    self.ids["btn_exam_start_grade"].opacity = 0

    on_exams(self)

def on_exams(self):
    if self.ids["layout_exams"] not in list(self.children):
        self.add_widget(self.ids["layout_exams"])

    self.ids["layout_exams"].opacity = 1
    self.remove_widget(self.ids["layout_participants"])

    args_converter = lambda row_index, i: {"text": i,
                                           "background_normal": "img/widget_75_black_crop.png",
                                           "font_name": "font/CaviarDreams_Bold.ttf", "font_size": self.height/25,
                                           "size_hint_y": None, "height": self.height/10}
    self.ids["list_exams"].adapter = ListAdapter(data=[i for i in ["Quiz 1","Midterm 1","Make Up","Quiz 2","Final"]], cls=ListItemButton,
                                                 args_converter=args_converter, allow_empty_selection=False)
    self.ids["list_exams"].adapter.bind(on_selection_change=self.on_exam_selected)

def on_exam_selected(self):
    self.ids["img_info_top"].opacity = 0.5
    self.ids["img_info_body"].opacity = 0.5
    self.ids["txt_info_head"].opacity = 1
    self.ids["txt_info_head"].text = self.ids["list_exams"].adapter.selection[0].text

    self.ids["txt_status_head"].opacity = 1
    self.ids["txt_status_body"].opacity = 1
    self.ids["txt_status_body"].text = "TODO"

    self.ids["txt_options_head"].opacity = 1
    self.ids["btn_exam_edit"].opacity = 1
    self.ids["btn_exam_delete"].opacity = 1
    self.ids["btn_exam_start_grade"].opacity = 1

    if self.ids["txt_status_body"].text == "Completed":
        self.ids["btn_exam_start_grade"].text = "GRADE"
    else:
        self.ids["btn_exam_start_grade"].text = "START"

def on_participants(self):
    if self.ids["layout_participants"] not in list(self.children):
        self.add_widget(self.ids["layout_participants"])

    self.ids["layout_participants"].opacity = 1
    self.remove_widget(self.ids["layout_exams"])

    temp_student_list = open("data/temp_student_list.seas", "r")
    data_student_list = temp_student_list.readlines()

    args_converter = lambda row_index, i: {"text": i,
                                           "background_normal": "img/widget_75_black_crop.png",
                                           "font_name": "font/CaviarDreams_Bold.ttf", "font_size": self.height / 50,
                                           "size_hint_y": None, "height": self.height / 25}
    self.ids["list_participants"].adapter = ListAdapter(data=[i.split(",")[0] for i in data_student_list],
                                                        cls=ListItemButton, args_converter=args_converter,
                                                        allow_empty_selection=False)
    self.ids["list_participants"].adapter.bind(on_selection_change=self.on_participant_selected)

    self.ids["btn_import_list"].bind(on_release=self.on_import_list)

def on_participant_selected(self):
    temp_student_list = open("data/temp_student_list.seas", "r")
    data_student_list = temp_student_list.readlines()

    for i in data_student_list:
        if i.split(",")[0] == self.ids["list_participants"].adapter.selection[0].text:
            txt_id_body = i.split(",")[1]
            txt_mail_body = i.split(",")[2].replace("\n","")

    self.ids["img_info_top_2"].opacity = 0.5
    self.ids["img_info_body_2"].opacity = 0.5
    self.ids["txt_info_head_2"].opacity = 1
    try:
        self.ids["txt_info_head_2"].text = self.ids["list_participants"].adapter.selection[0].text
    except:
        self.ids["txt_info_head_2"].text = "Information"

    self.ids["txt_id_head"].opacity = 1
    self.ids["txt_id_body"].opacity = 1
    self.ids["txt_id_body"].text = txt_id_body

    self.ids["txt_mail_head"].opacity = 1
    self.ids["txt_mail_body"].opacity = 1
    self.ids["txt_mail_body"].text = txt_mail_body

    self.ids["txt_options_head_2"].opacity = 1
    self.ids["btn_student_delete"].opacity = 1
    self.ids["btn_student_statistics"].opacity = 1

def on_import_list(self):
    popup_content = FloatLayout()
    self.popup = Popup(title="Import list for %s" % self.ids["txt_lect_code"].text,
                       content=popup_content, separator_color=[140 / 255., 55 / 255., 95 / 255., 1.],
                       size_hint=(None, None), size=(self.width / 2, self.height / 2))
    filechooser = FileChooserListView(path=os.path.expanduser('~'),
                                      size=(self.width, self.height),
                                      pos_hint={"center_x": .5, "center_y": .5})
    filechooser.bind(on_submit=self.on_import_list_selected)
    popup_content.add_widget(filechooser)
    popup_content.add_widget(Button(text="Close",
                                    font_name="font/LibelSuit.ttf",
                                    font_size=self.height / 40,
                                    background_normal="img/widget_100.png",
                                    background_down="img/widget_100_selected.png",
                                    size_hint_y=None, height=self.height / 20,
                                    pos_hint={"center_x": .5, "y": .0},
                                    on_release=self.popup.dismiss))
    self.popup.open()

def on_import_list_selected(self, widget_name, file_path, mouse_pos):
    self.popup.dismiss()

    print file_path[0]

    temp_student_list = open("data/temp_student_list.seas", "r")
    data_student_list = temp_student_list.readlines()

    self.ids["list_participants"].adapter.data = [i.split(",")[0] for i in data_student_list]

def on_class_statistics(self):
    pass # TODO: Re-direct To Class Statistics