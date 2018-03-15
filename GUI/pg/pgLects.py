from kivy.logger import Logger
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.listview import ListItemButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.adapters.listadapter import ListAdapter

import os
from GUI.func import excel_to_csv
from GUI.func import database_api

'''
    This method imports all lectures given by educator from server
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

    Logger.info("pgLects: Educator's lectures successfully imported from server and listed on GUI")

'''
    This method re-organizes page according to information of selected lecture
    Default layout shown at first is exams
'''

def on_lect_select(self, dropdown, txt):
    dropdown.select(txt)

    self.ids["btn_exams"].disabled = False
    self.ids["btn_participants"].disabled = False
    self.ids["btn_class_statistics"].disabled = False

    self.ids["txt_hint"].opacity = 0

    self.ids["txt_lect_code"].opacity = 1
    self.ids["txt_lect_name"].opacity = 1

    for lect in self.data:
        if txt in " ".join(lect.split("_")).upper():
            self.ids["txt_lect_code"].text = txt
            self.ids["txt_lect_name"].text = " ".join(lect.split("_")[2:]).title()

            with open("data/temp_selected_lect.seas", "w+") as temp_selected_lect:
                temp_selected_lect.write(txt + "\n" + self.ids["txt_lect_name"].text)
                temp_selected_lect.close()
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

    Logger.info("pgLects: Educator selected lecture %s" % txt)

    on_exams(self)

'''
    This method tries to make exams layout visible if it is already not
    Then, imports exams of selected lecture from server and lists on GUI
'''

def on_exams(self):
    if self.ids["layout_exams"] not in list(self.children):
        self.add_widget(self.ids["layout_exams"])
    # TODO: Debug here (ReferenceError: weakly-referenced object no longer exists)

    self.ids["layout_exams"].opacity = 1
    self.remove_widget(self.ids["layout_participants"])

    self.data_exam_details = database_api.getExamsOfLecture(self.data_login[8].replace("\n", ""), self.ids["txt_lect_code"].text)

    args_converter = lambda row_index, i: {"text": i,
                                           "background_normal": "img/widget_75_black_crop.png",
                                           "font_name": "font/CaviarDreams_Bold.ttf", "font_size": self.height / 25,
                                           "size_hint_y": None, "height": self.height / 10}
    self.ids["list_exams"].adapter = ListAdapter(data=[i[1] for i in self.data_exam_details], cls=ListItemButton,
                                                 args_converter=args_converter, allow_empty_selection=False)
    self.ids["list_exams"].adapter.bind(on_selection_change=self.on_exam_selected)

    Logger.info("pgLects: Exams of selected lecture successfully imported from server and listed on GUI")

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

    self.ids["txt_status_head"].opacity = 1
    self.ids["txt_status_body"].opacity = 1
    for i in self.data_exam_details:
        if i[1] == self.ids["list_exams"].adapter.selection[0].text:
            self.ids["txt_status_body"].text = i[5]
            break

    self.ids["txt_options_head"].opacity = 1
    self.ids["btn_exam_edit"].opacity = 1
    self.ids["btn_exam_delete"].opacity = 1
    self.ids["btn_exam_start_grade"].opacity = 1

    self.ids["btn_exam_delete"].bind(on_release=self.on_exam_deleted)

    if self.ids["txt_status_body"].text == "finished":
        self.ids["btn_exam_start_grade"].text = "GRADE"
        # TODO
    elif self.ids["txt_status_body"].text == "graded":
        self.ids["btn_exam_start_grade"].text = "DOWNLOAD"
        # TODO
    elif self.ids["txt_status_body"].text == "ready":
        self.ids["btn_exam_start_grade"].text = "PUBLISH"
        # TODO
    else:
        self.ids["btn_exam_start_grade"].text = "START"
        self.ids["btn_exam_start_grade"].bind(on_release=self.on_start_exam)

'''
    This method requests deletion of selected lecture from server and re-lists exams of selected lecture on GUI
'''

def on_exam_deleted(self):
    database_api.deleteExam(self.data_login[8].replace("\n", ""), self.ids["list_exams"].adapter.selection[0].text, self.ids["txt_lect_code"].text)

    self.data_exam_details = database_api.getExamsOfLecture(self.data_login[8].replace("\n", ""), self.ids["txt_lect_code"].text)

    self.ids["list_exams"].adapter.data = [i[1] for i in self.data_exam_details]

    Logger.info("pgLects: Exam successfully deleted")

'''
    This method tries to make participants layout visible if it is already not
    Then, imports participants of selected lecture from server and lists on GUI
'''

def on_participants(self):
    if self.ids["layout_participants"] not in list(self.children):
        self.add_widget(self.ids["layout_participants"])

    self.ids["layout_participants"].opacity = 1
    self.remove_widget(self.ids["layout_exams"])

    data = database_api.getCourseStudents(self.data_login[8].replace("\n", ""), self.ids["txt_lect_code"].text)

    with open("data/temp_student_list.seas", "w+") as temp_student_list:
        for d in data:
            temp_student_list.write(d[0] + "," + d[1] + "," + str(d[2]) + "," + d[3] + "\n")
        temp_student_list.close()

    temp_student_list = open("data/temp_student_list.seas", "r")
    self.data_student_list = temp_student_list.readlines()

    args_converter = lambda row_index, i: {"text": i,
                                           "background_normal": "img/widget_75_black_crop.png",
                                           "font_name": "font/CaviarDreams_Bold.ttf", "font_size": self.height / 50,
                                           "size_hint_y": None, "height": self.height / 25}
    self.ids["list_participants"].adapter = ListAdapter(data=[i.split(",")[0] + " " + i.split(",")[1] for i in self.data_student_list],
                                                        cls=ListItemButton, args_converter=args_converter,
                                                        allow_empty_selection=False)
    self.ids["list_participants"].adapter.bind(on_selection_change=self.on_participant_selected)

    self.ids["btn_import_list"].bind(on_release=self.on_import_list)

    Logger.info("pgLects: Participants of selected lecture successfully imported from server and listed on GUI")

'''
    This method re-organizes bottom-right widget and related button bindings according to information of selected student
'''

def on_participant_selected(self):
    txt_id_body = "..."
    txt_mail_body = "..."

    for i in self.data_student_list:
        if len(self.ids["list_participants"].adapter.selection) > 0:
            if i.split(",")[0] + " " + i.split(",")[1] == self.ids["list_participants"].adapter.selection[0].text:
                txt_id_body = i.split(",")[2]
                txt_mail_body = i.split(",")[3].replace("\n", "")

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

    self.ids["btn_student_delete"].bind(on_release=self.on_participant_deleted)

    self.ids["btn_student_statistics"].opacity = 1

'''
    This method requests deletion of selected student from server and re-lists participants of selected lecture on GUI
'''

def on_participant_deleted(self):
    database_api.deleteStudentFromLecture(self.data_login[8].replace("\n", ""), self.ids["txt_lect_code"].text, self.ids["txt_id_body"].text)

    data = database_api.getCourseStudents(self.data_login[8].replace("\n", ""), self.ids["txt_lect_code"].text)

    with open("data/temp_student_list.seas", "w+") as temp_student_list:
        for d in data:
            temp_student_list.write(d[0] + "," + d[1] + "," + str(d[2]) + "," + d[3] + "\n")
        temp_student_list.close()

    temp_student_list = open("data/temp_student_list.seas", "r")
    self.data_student_list = temp_student_list.readlines()

    self.ids["list_participants"].adapter.data = [i.split(",")[0] + " " + i.split(",")[1] for i in self.data_student_list]

    Logger.info("pgLects: Participant successfully deleted")

'''
    This method opens pop-up for importing list of students as either excel or csv
    Accordingly, it calls on_import_list_selected or disappears
'''

def on_import_list(self):
    Logger.info("pgLects: Educator called import list pop-up")

    popup_content = FloatLayout()
    self.popup = Popup(title="* Double click to select a file!",
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

'''
    This method sends imported file containing list of students to server and lists them on GUI
'''

def on_import_list_selected(self, widget_name, file_path, mouse_pos):
    self.popup.dismiss()

    excel_to_csv.xls2csv(file_path[0], "data/perm_student_list.csv")
    database_api.registerStudent(self.data_login[8].replace("\n", ""), self.ids["txt_lect_code"].text,
                                 True, "data/perm_student_list.csv", self.data_login[0].replace("\n", ""))

    data = database_api.getCourseStudents(self.data_login[8].replace("\n", ""), self.ids["txt_lect_code"].text)

    with open("data/temp_student_list.seas", "w+") as temp_student_list:
        for d in data:
            temp_student_list.write(d[0] + "," + d[1] + "," + str(d[2]) + "," + d[3] + "\n")
        temp_student_list.close()

    temp_student_list = open("data/temp_student_list.seas", "r")
    self.data_student_list = temp_student_list.readlines()

    self.ids["list_participants"].adapter.data = [i.split(",")[0] + " " + i.split(",")[1] for i in self.data_student_list]

    Logger.info("pgLects: Educator successfully imported list of students")

'''
    This method TODO
'''

def on_start_exam(self):
    with open("data/temp_selected_lect.seas", "a+") as temp_selected_lect:
        temp_selected_lect.write("\n" + self.ids["txt_info_head"].text)
        temp_selected_lect.close()

    database_api.change_status_of_exam(self.data_login[8].replace("\n", ""),
                                       self.ids["txt_lect_code"].text,
                                       self.ids["txt_info_head"].text, "active")

    Logger.info("pgLects: Educator successfully started exam")

def on_class_statistics(self):
    pass