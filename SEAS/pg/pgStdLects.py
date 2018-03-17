from kivy.clock import Clock
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.listview import ListItemButton
from kivy.adapters.listadapter import ListAdapter

from functools import partial
from SEAS.func import database_api
from SEAS.func.check_std_live_exam import check_std_live_exam

'''
    This method imports all lectures that student registered from server
    Then, puts them into top-left dropdown menu before entering PgLects
'''

def on_pre_enter(self):
    temp_login = open("data/temp_login.seas", "r")
    self.data_login = temp_login.readlines()

    self.data = []

    data_lectures = database_api.getUserCourses(self.data_login[8].replace("\n", ""), self.data_login[0].replace("\n", ""))
    for i in data_lectures:
        self.data.append(i[1] + "_" + i[0])

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

    Logger.info("pgStdLects: Student's lectures successfully imported from server and listed on GUI")

'''
    This method re-organizes page according to information of selected lecture
    Additionally, it imports exams of selected lecture from server and lists on SEAS
'''

def on_lect_select(self, dropdown, txt):
    dropdown.select(txt)

    try:
        self.check_std_live_exam.cancel()
    except:
        pass
    finally:
        Clock.schedule_once(partial(check_std_live_exam, self))
        self.check_std_live_exam = Clock.schedule_interval(partial(check_std_live_exam, self), 5.0)

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

    self.data_exams = database_api.getExamsOfLecture(self.data_login[8].replace("\n", ""), self.ids["txt_lect_code"].text)

    args_converter = lambda row_index, i: {"text": i.replace("_", " ").title(),
                                           "background_normal": "img/widget_75_black_crop.png",
                                           "font_name": "font/CaviarDreams_Bold.ttf", "font_size": self.height / 25,
                                           "size_hint_y": None, "height": self.height / 10}
    self.ids["list_exams"].adapter = ListAdapter(data=[i[1] for i in self.data_exams], cls=ListItemButton,
                                                 args_converter=args_converter, allow_empty_selection=False)
    self.ids["list_exams"].adapter.bind(on_selection_change=self.on_exam_selected)

    Logger.info("pgStdLects: Student selected lecture %s" % txt)

'''
    This method re-organizes bottom-right widget and related button bindings according to information of selected exam
'''

def on_exam_selected(self):
    self.ids["img_info_top"].opacity = 0.5
    self.ids["img_info_body"].opacity = 0.5
    self.ids["txt_info_head"].opacity = 1
    try:
        self.ids["txt_info_head"].text = self.ids["list_exams"].adapter.selection[0].text
    except:
        self.ids["txt_info_head"].text = "Information"

    self.ids["txt_date_head"].opacity = 1
    self.ids["txt_date_body"].opacity = 1
    for i in self.data_exams:
        try:
            if i[1].replace("_", " ").title() == self.ids["list_exams"].adapter.selection[0].text:
                timestamp = i[3].split(" ")
                self.ids["txt_date_body"].text = timestamp[1] + " " + timestamp[2] + " " + timestamp[3]
            break
        except:
            if i[1].replace("_", " ").title() == self.ids["txt_info_head"].text:
                timestamp = i[3].split(" ")
                self.ids["txt_date_body"].text = timestamp[1] + " " + timestamp[2] + " " + timestamp[3]
                break

    self.ids["txt_time_head"].opacity = 1
    self.ids["txt_time_body"].opacity = 1
    for i in self.data_exams:
        try:
            if i[1].replace("_", " ").title() == self.ids["list_exams"].adapter.selection[0].text:
                self.ids["txt_time_body"].text = str(i[4])
            break
        except:
            if i[1].replace("_", " ").title() == self.ids["txt_info_head"].text:
                self.ids["txt_time_body"].text = str(i[4])
                break

    self.ids["txt_options_head"].opacity = 1
    self.ids["btn_exam_statistics"].opacity = 1

def on_join_exam(self):
    with open("data/temp_selected_lect.seas", "w+") as temp_selected_lect:
        temp_selected_lect.write(self.ids["txt_lect_code"].text+ "\n" + self.ids["txt_info_head"].text + "\n" + self.live_exam)
        temp_selected_lect.close()

    Logger.info("pgStdLects: Student successfully requested to join exam")

'''
    This method checks clock event scheduled for connection checking and cancels it to avoid too many requests later on
'''

def on_leave(self):
    self.check_std_live_exam.cancel()

def on_personal_statistics(self):
    pass