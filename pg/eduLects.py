"""
eduLects
========

`eduLects` is a toolbox for main app, it contains necessary methods that EduLects page requires.
"""

import imghdr
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from functools import partial

from kivy.adapters.listadapter import ListAdapter
from kivy.cache import Cache
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.listview import ListItemButton, ListView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from func import database_api, excel_to_csv, image_button

__author__ = "Muhammed Yasin Yildirim"


def load_buttons(self):
    """
    This method adds image buttons to quit and logout as well as it updates profile picture widget.
    :param self: It is for handling class structure.
    :return:
    """

    layout_menubar = self.ids["layout_menubar"]

    layout_menubar.add_widget(image_button.add_button("data/img/ico_quit.png",
                                                      "data/img/ico_quit_select.png",
                                                      .075,
                                                      {"x": .925, "y": 0},
                                                      self.on_quit
                                                      )
                              )

    layout_menubar.add_widget(image_button.add_button("data/img/ico_logout.png",
                                                      "data/img/ico_logout_select.png",
                                                      .075,
                                                      {"x": 0, "y": 0},
                                                      self.on_logout
                                                      )
                              )

    layout_menubar.add_widget(image_button.add_button("data/img/ico_picture.png",
                                                      "data/img/ico_picture_select.png",
                                                      .075,
                                                      {"x": .075, "y": 0},
                                                      self.on_profile
                                                      )
                              )

    self.ico_user_picture = Image(allow_scretch=True,
                                  size_hint_x=.02,
                                  pos_hint={"center_x": .1125, "center_y": .5}
                                  )
    try:
        if Cache.get("info", "pict") and imghdr.what("data/img/pic_user_current.png") == "png":
            self.ico_user_picture.source = "data/img/pic_user_current.png"
        else:
            self.ico_user_picture.source = "data/img/pic_user.png"
    except:
        self.ico_user_picture.source = "data/img/pic_user.png"
    finally:
        self.ico_user_picture.reload()
        layout_menubar.add_widget(self.ico_user_picture)


def on_pre_enter(self):
    """
    This method imports lectures given by educator and puts them into dropdown list.
    :param self: It is for handling class structure.
    :return:
    """

    self.cipher = Cache.get("config", "cipher")

    self.data = []
    data_lectures = database_api.getUserCourses(Cache.get("info", "token"),
                                                Cache.get("info", "nick")
                                                )
    for i in data_lectures:
        self.data.append("{i1}_{i0}".format(i1=i[1],
                                            i0=i[0])
                         )

    list_dropdown = DropDown()

    for lect in self.data:
        btn_lect = Button(text=" ".join(lect.split("_")[:2]).upper(),
                          color=(0, 0, 0, 1),
                          font_name="data/font/LibelSuit.ttf",
                          font_size=self.height / 40,
                          background_normal="data/img/widget_gray_75.png",
                          background_down="data/img/widget_gray_75_select.png",
                          size_hint_y=None,
                          height=self.height / 10
                          )
        btn_lect.bind(on_release=lambda btn_lect: self.on_lect_select(self,
                                                                      list_dropdown,
                                                                      btn_lect.text
                                                                      )
                      )
        list_dropdown.add_widget(btn_lect)

    btn_main = Button(text="Select A Lecture",
                      font_name="data/font/LibelSuit.ttf",
                      font_size=self.height / 40,
                      background_normal="data/img/widget_black_75.png",
                      background_down="data/img/widget_gray_75.png",
                      size_hint=(.2, .1),
                      pos=(self.x, self.height * 8.25 / 10))
    btn_main.bind(on_release=list_dropdown.open)

    list_dropdown.bind(on_select=lambda instance, x: setattr(btn_main,
                                                             "text",
                                                             x
                                                             )
                       )

    self.add_widget(btn_main)


def on_lect_select(self, dropdown, txt):
    """
    This method updates GUI according to selected lecture.
    :param self: It is for handling class structure.
    :param dropdown: It is dropdown menu.
    :param txt: It is lecture code selected on dropdown menu.
    :return: It is for displaying exams tab on screen as default when lecture is selected.
    """

    dropdown.select(txt)

    self.ids["txt_hint"].opacity = 0

    self.ids["btn_exams"].disabled = False
    self.ids["btn_participants"].disabled = False
    self.ids["btn_stats_class"].disabled = False

    self.ids["txt_lect_code"].opacity = 1
    self.ids["txt_lect_name"].opacity = 1

    for lect in self.data:
        if txt in lect.replace("_", " ").upper():
            self.ids["txt_lect_code"].text = txt
            self.ids["txt_lect_name"].text = " ".join(lect.split("_")[2:]).title()

            Cache.append("lect",
                         "code",
                         txt
                         )
            Cache.append("lect",
                         "name",
                         self.ids["txt_lect_name"].text
                         )

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

    self.ids["img_filter"].source = "data/img/widget_gray_75.png"

    return on_exams(self)


def on_exams(self):
    """
    This method brings exams tab into screen and lists all exams registered for selected course.
    :param self: It is for handling class structure.
    :return:
    """

    if self.ids["layout_exams"] not in list(self.children):
        self.add_widget(self.ids["layout_exams"])

    self.ids["layout_exams"].opacity = 1
    try:
        self.remove_widget(self.ids["layout_participants"])
    except ReferenceError:
        pass

    self.data_exam_details = database_api.getExamsOfLecture(Cache.get("info", "token"),
                                                            self.ids["txt_lect_code"].text
                                                            )

    self.data_exam_filter = {"green": [],
                             "yellow": [],
                             "red": []
                             }

    def color(x):
        """
        This method determines color name and thereby, category for given exam according to its status.
        :param x: It is data of exam.
        :return: It is name of color.
        """

        if x[5] == "graded":
            name = "green"
        elif x[5] == "finished":
            name = "yellow"
        else:
            name = "red"

        self.data_exam_filter[name].append(x)

        return name

    args_converter = lambda row_index, x: {"text": x[1].replace("_", " ").title(),
                                           "selected_color": (.843, .82, .82, 1),
                                           "deselected_color": (.57, .67, .68, 1),
                                           "background_down": "data/img/widget_gray_75.png",
                                           "background_normal": "data/img/widget_list_{x5}.png".format(x5=color(x)),
                                           "font_name": "data/font/CaviarDreams_Bold.ttf",
                                           "font_size": self.height / 25,
                                           "size_hint_y": None,
                                           "height": self.height / 10
                                           }
    self.ids["list_exams"].adapter = ListAdapter(data=[i for i in self.data_exam_details],
                                                 cls=ListItemButton,
                                                 args_converter=args_converter,
                                                 allow_empty_selection=False
                                                 )
    self.ids["list_exams"].adapter.bind(on_selection_change=partial(on_exam_select,
                                                                    self
                                                                    )
                                        )

    def on_filter(clr, dt):
        """
        This method reloads exam list according to selected filter.
        :param clr: It is name of selected color.
        :param dt: It is for handling callback input.
        :return:
        """

        if clr != "all":
            set_exam_filter = set(map(tuple,
                                      self.data_exam_filter[clr]
                                      )
                                  )
            clr_exam_filter = map(list,
                                  set_exam_filter
                                  )
            self.ids["list_exams"].adapter.data = [exam for exam in list(reversed(clr_exam_filter))]

            self.ids["img_filter"].source = "data/img/widget_{x5}.png".format(x5=clr)
        else:
            self.ids["list_exams"].adapter.data = [exam for exam in self.data_exam_details]

            self.ids["img_filter"].source = "data/img/widget_gray_75.png"

    try:
        if self.btn_filter_all in list(self.ids["layout_exams"].children):
            pass
    except:
        for key in self.data_exam_filter.iterkeys():
            if key == "green":
                pos_y = .4725
            elif key == "yellow":
                pos_y = .4225
            else:
                pos_y = .3725

            self.ids["layout_exams"].add_widget(image_button.add_button("data/img/widget_{x5}.png".format(x5=key),
                                                                        "data/img/widget_{x5}_select.png".format(x5=key),
                                                                        (.025, True),
                                                                        {"x": .225, "y": pos_y},
                                                                        partial(on_filter,
                                                                                key
                                                                                )
                                                                        )
                                                )

        self.btn_filter_all = image_button.add_button("data/img/widget_gray_75.png",
                                                      "data/img/widget_gray_75_select.png",
                                                      (.025, True),
                                                      {"x": .225, "y": .5225},
                                                      partial(on_filter,
                                                              "all"
                                                              )
                                                      )
        self.ids["layout_exams"].add_widget(self.btn_filter_all)


def on_exam_select(self, dt):
    """
    This method updates exam information widget according to selected exam.
    :param self: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return:
    """

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
        try:
            if i[1].replace("_", " ").title() == self.ids["list_exams"].adapter.selection[0].text:
                self.ids["txt_status_body"].text = i[5].title()
                break
        except:
            if i[1].replace("_", " ").title() == self.ids["txt_info_head"].text:
                self.ids["txt_status_body"].text = i[5].title()
                break

    self.ids["txt_options_head"].opacity = 1

    self.ids["btn_exam_delete"].opacity = 1
    if len(self.ids["btn_exam_delete"].get_property_observers("on_release")) < 1:
        self.ids["btn_exam_delete"].bind(on_release=partial(on_exam_delete,
                                                            self
                                                            )
                                         )

    self.ids["btn_exam_edit"].opacity = 1
    if len(self.ids["btn_exam_edit"].get_property_observers("on_release")) > 0:
        self.ids["btn_exam_edit"].unbind(on_release=self.on_start_edit)

    self.on_start_edit = partial(on_exam_edit,
                                 self
                                 )
    self.ids["btn_exam_edit"].bind(on_release=self.on_start_edit)

    self.ids["btn_exam_start_grade"].opacity = 1
    if self.ids["txt_status_body"].text == "Graded":
        self.ids["btn_exam_start_grade"].text = "DOWNLOAD"

        if len(self.ids["btn_exam_start_grade"].get_property_observers("on_release")) > 0:
            self.ids["btn_exam_start_grade"].unbind(on_release=self.start_grade)

        self.start_grade = partial(None,  # TODO
                                   self
                                   )
        self.ids["btn_exam_start_grade"].bind(on_release=self.start_grade)
    elif self.ids["txt_status_body"].text == "Finished":
        self.ids["btn_exam_start_grade"].text = "GRADE"

        if len(self.ids["btn_exam_start_grade"].get_property_observers("on_release")) > 0:
            self.ids["btn_exam_start_grade"].unbind(on_release=self.start_grade)

        self.start_grade = partial(on_exam_grade,
                                   self
                                   )
        self.ids["btn_exam_start_grade"].bind(on_release=self.start_grade)
    else:
        self.ids["btn_exam_start_grade"].text = "START"

        if len(self.ids["btn_exam_start_grade"].get_property_observers("on_release")) > 0:
            self.ids["btn_exam_start_grade"].unbind(on_release=self.start_grade)

        self.start_grade = partial(on_exam_start,
                                   self
                                   )
        self.ids["btn_exam_start_grade"].bind(on_release=self.start_grade)


def on_exam_delete(self, dt):
    """
    This method deletes selected exam through server and refreshes list of exams.
    :param self: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return: It is for updating both exam list and categories when exam is deleted.
    """

    try:
        database_api.deleteExam(Cache.get("info", "token"),
                                self.ids["list_exams"].adapter.selection[0].text,
                                self.ids["txt_lect_code"].text
                                )
    except:
        database_api.deleteExam(Cache.get("info", "token"),
                                self.ids["txt_info_head"].text,
                                self.ids["txt_lect_code"].text
                                )

    return on_exams(self)


def on_exam_start(self, dt):
    """
    This method changes selected exam's status to active through server.
    :param self: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return: It is for changing screen to live exam page when exam is started.
    """

    Cache.append("lect",
                 "code",
                 self.ids["txt_lect_code"].text
                 )
    Cache.append("lect",
                 "name",
                 self.ids["txt_lect_name"].text
                 )
    Cache.append("lect",
                 "exam",
                 self.ids["txt_info_head"].text
                 )

    database_api.change_status_of_exam(Cache.get("info", "token"),
                                       self.ids["txt_lect_code"].text,
                                       self.ids["txt_info_head"].text,
                                       "active"
                                       )

    return self.on_live()


def on_exam_grade(s, dt):
    """
    This method creates pop-up that lists students and their grades.
    :param s: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return:
    """

    def on_exam_grade_select(self, dt):
        """
        This method switches screen for grading selected student.
        :param self: It is for handling class structure.
        :param dt: It is for handling callback input.
        :return: It is for changing screen to grading page.
        """

        self.popup.dismiss()

        Cache.append("lect",
                     "code",
                     self.ids["txt_lect_code"].text
                     )
        Cache.append("lect",
                     "exam",
                     self.ids["txt_info_head"].text
                     )

        for x in self.data_students_joined:
            if "{x0} {x1} ".format(x0=x[0], x1=x[1]).title() == self.list_grades.adapter.selection[0].text.split("(")[0]:
                Cache.append("lect",
                             "std_id",
                             x[2]
                             )
                Cache.append("lect",
                             "std_nick",
                             x[4]
                             )
                Cache.append("lect",
                             "std_name",
                             "{x0} {x1}".format(x0=x[0], x1=x[1]).title()
                             )
                break

        with open("data/questions.fay", "w+") as questions:
            questions.close()

        return self.on_grade()

    def on_exam_grade_complete(self, dt):
        """
        This method completes grading for selected exam.
        :param self: It is for handling class structure.
        :param dt: It is for handling callback input.
        :return:
        """

        database_api.change_status_of_exam(Cache.get("info", "token"),
                                           self.ids["txt_lect_code"].text,
                                           self.ids["txt_info_head"].text,
                                           "graded"
                                           )

        self.ids["txt_status_body"].text = "Graded"

        self.ids["btn_exam_start_grade"].text = "DOWNLOAD"

        if len(self.ids["btn_exam_start_grade"].get_property_observers("on_release")) > 0:
            self.ids["btn_exam_start_grade"].unbind(on_release=self.start_grade)

        self.start_grade = partial(None,  # TODO
                                   self
                                   )
        self.ids["btn_exam_start_grade"].bind(on_release=self.start_grade)

        self.popup.dismiss()

    popup_content = FloatLayout()
    s.popup = Popup(title="Grades",
                    content=popup_content,
                    separator_color=[140 / 255., 55 / 255., 95 / 255., 1.],
                    size_hint=(None, None),
                    size=(s.width / 2, s.height / 2)
                    )

    s.data_students_joined = database_api.getCourseStudents(Cache.get("info", "token"),
                                                            s.ids["txt_lect_code"].text
                                                            )

    data_students_graded = database_api.getGradesOfExam(Cache.get("info", "token"),
                                                        s.ids["txt_lect_code"].text,
                                                        s.ids["list_exams"].adapter.selection[0].text
                                                        )
    data_students_merged = {}

    for std in s.data_students_joined:
        std_name = "{name} {surname}".format(name=std[0].title(),
                                             surname=std[1].title()
                                             )

        data_students_merged[std[4]] = [std_name, "None"]

        for grade in data_students_graded:
            if grade[0] == std[4] and grade[1] is not None:
                data_students_merged[std[4]] = [std_name, "{0:0=2d}".format(int(grade[1]))]
                break

    def color_hex(x):
        """
        This method determines hex color code for given student according to his or her grade.
        :param x: It is student's grade.
        :return: It is hex code of color.
        """

        grade_hex = {"NaN": "CAC3C3",
                     "30": "FF4530",
                     "45": "FF7363",
                     "60": "FCAA03",
                     "75": "FDBF41",
                     "90": "84C463",
                     "100": "5CB130"
                     }

        if x == "None":
            hex_code = grade_hex["NaN"]
        elif int(x.strip()) <= 30:
            hex_code = grade_hex["30"]
        elif 30 < int(x.strip()) <= 45:
            hex_code = grade_hex["45"]
        elif 45 < int(x.strip()) <= 60:
            hex_code = grade_hex["60"]
        elif 60 < int(x.strip()) <= 75:
            hex_code = grade_hex["75"]
        elif 75 < int(x.strip()) <= 90:
            hex_code = grade_hex["90"]
        else:
            hex_code = grade_hex["100"]

        return hex_code

    s.list_grades = ListView(size_hint=(.9, .8),
                             pos_hint={"center_x": .5, "center_y": .55}
                             )
    args_converter = lambda row_index, x: {"text": "{name} ([color=#{hex}]{grade}[/color])".format(name=x[0],
                                                                                                   hex=color_hex(x[1]),
                                                                                                   grade=x[1]
                                                                                                   ),
                                           "markup": True,
                                           "selected_color": (.843, .82, .82, 1),
                                           "deselected_color": (.57, .67, .68, 1),
                                           "background_down": "data/img/widget_gray_75.png",
                                           "font_name": "data/font/CaviarDreams_Bold.ttf",
                                           "font_size": s.height / 50,
                                           "size_hint_y": None,
                                           "height": s.height / 20,
                                           "on_release": partial(on_exam_grade_select,
                                                                 s
                                                                 )
                                           }
    s.list_grades.adapter = ListAdapter(data=[i for i in data_students_merged.itervalues()],
                                        cls=ListItemButton,
                                        args_converter=args_converter,
                                        allow_empty_selection=False
                                        )
    popup_content.add_widget(s.list_grades)
    popup_content.add_widget(Button(text="Complete",
                                    font_name="data/font/LibelSuit.ttf",
                                    font_size=s.height / 40,
                                    background_normal="data/img/widget_green.png",
                                    background_down="data/img/widget_green_select.png",
                                    size_hint_x=.5,
                                    size_hint_y=None,
                                    height=s.height / 20,
                                    pos_hint={"center_x": .25, "y": .0},
                                    on_release=partial(on_exam_grade_complete,
                                                       s
                                                       )
                                    )
                             )
    popup_content.add_widget(Button(text="Close",
                                    font_name="data/font/LibelSuit.ttf",
                                    font_size=s.height / 40,
                                    background_normal="data/img/widget_red.png",
                                    background_down="data/img/widget_red_select.png",
                                    size_hint_x=.5,
                                    size_hint_y=None,
                                    height=s.height / 20,
                                    pos_hint={"center_x": .75, "y": .0},
                                    on_release=s.popup.dismiss)
                             )
    s.popup.open()


def on_exam_edit(self, dt):
    """
    TODO
    :param self: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return:
    """

    popup_content = FloatLayout()
    self.popup = Popup(title=self.ids["txt_info_head"].text,
                       content=popup_content,
                       separator_color=[140 / 255., 55 / 255., 95 / 255., 1.],
                       size_hint=(None, None),
                       size=(self.width / 2, self.height / 2)
                       )
    data_exam_questions = database_api.getExam(Cache.get("info", "token"),
                                               self.ids["txt_lect_code"].text,
                                               self.ids["txt_info_head"].text
                                               )["Questions"]
    self.list_edit = ListView(size_hint=(.9, .8),
                              pos_hint={"center_x": .5, "center_y": .55}
                              )
    args_converter = lambda row_index, x: {"text": "Question {:02}".format(int(x)),
                                           "markup": True,
                                           "selected_color": (.843, .82, .82, 1),
                                           "deselected_color": (.57, .67, .68, 1),
                                           "background_down": "data/img/widget_gray_75.png",
                                           "font_name": "data/font/CaviarDreams_Bold.ttf",
                                           "font_size": self.height / 50,
                                           "size_hint_y": None,
                                           "height": self.height / 20,
                                           "on_release": partial(self.on_edit, x)
                                           }
    self.list_edit.adapter = ListAdapter(data=sorted([i for i in data_exam_questions.keys()]),
                                         cls=ListItemButton,
                                         args_converter=args_converter,
                                         allow_empty_selection=False
                                         )
    popup_content.add_widget(self.list_edit)
    popup_content.add_widget(Button(text="Close",
                                    font_name="data/font/LibelSuit.ttf",
                                    font_size=self.height / 40,
                                    background_normal="data/img/widget_red.png",
                                    background_down="data/img/widget_red_select.png",
                                    size_hint_x=1,
                                    size_hint_y=None,
                                    height=self.height / 20,
                                    pos_hint={"center_x": .5, "y": .0},
                                    on_release=self.popup.dismiss)
                             )
    self.popup.open()


def on_participants(self):
    """
    This method brings participants tab into screen and lists all participants registered for selected course.
    :param self: It is for handling class structure.
    :return:
    """

    try:
        if self.ids["layout_participants"] not in list(self.children):
            self.add_widget(self.ids["layout_participants"])

        self.ids["layout_participants"].opacity = 1
        self.remove_widget(self.ids["layout_exams"])
    except ReferenceError:
        pass

    data = database_api.getCourseStudents(Cache.get("info", "token"),
                                          self.ids["txt_lect_code"].text
                                          )

    with open("data/participants.fay", "w+") as participants:
        std = []
        for d in data:
            std.append("{d0},{d1},{d2},{d3}".format(d0=d[0].title(),
                                                    d1=d[1].title(),
                                                    d2=str(d[2]),
                                                    d3=d[3].lower()
                                                    )
                       )
        participants.write(self.cipher.encrypt(str("*[SEAS-NEW-LINE]*".join(std))))
        participants.close()

    participants = open("data/participants.fay", "r")
    self.data_student_list = self.cipher.decrypt(participants.read()).split("*[SEAS-NEW-LINE]*")

    args_converter = lambda row_index, x: {"text": x,
                                           "selected_color": (.843, .82, .82, 1),
                                           "deselected_color": (.57, .67, .68, 1),
                                           "background_down": "data/img/widget_gray_75.png",
                                           "font_name": "data/font/CaviarDreams_Bold.ttf",
                                           "font_size": self.height / 50,
                                           "size_hint_y": None,
                                           "height": self.height / 25
                                           }
    self.ids["list_participants"].adapter = ListAdapter(data=["{i0} {i1}".format(i0=i.split(",")[0],
                                                                                 i1=i.split(",")[1]
                                                                                 ) for i in self.data_student_list if len(i) > 0],
                                                        cls=ListItemButton,
                                                        args_converter=args_converter,
                                                        allow_empty_selection=False
                                                        )
    self.ids["list_participants"].adapter.bind(on_selection_change=partial(on_participant_select,
                                                                           self
                                                                           )
                                               )

    if len(self.ids["btn_import_list"].get_property_observers("on_release")) < 1:
        self.ids["btn_import_list"].bind(on_release=partial(on_list_import,
                                                            self
                                                            )
                                         )


def on_participant_select(self, dt):
    """
    This method updates participant information widget according to selected participant.
    :param self: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return:
    """

    txt_id_body = "..."
    txt_mail_body = "..."

    for i in self.data_student_list:
        if len(self.ids["list_participants"].adapter.selection) > 0:
            participant = "{i0} {i1}".format(i0=i.split(",")[0],
                                             i1=i.split(",")[1]
                                             )
            if participant == self.ids["list_participants"].adapter.selection[0].text:
                txt_id_body = i.split(",")[2]
                txt_mail_body = i.split(",")[3]

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
    if len(self.ids["btn_student_delete"].get_property_observers("on_release")) < 1:
        self.ids["btn_student_delete"].bind(on_release=partial(on_participant_delete,
                                                               self
                                                               )
                                            )

    self.ids["btn_stats_student"].opacity = 1


def on_participant_delete(self, dt):
    """
    This method deletes selected participant through server and refreshes list of participants.
    :param self: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return:
    """

    database_api.deleteStudentFromLecture(Cache.get("info", "token"),
                                          self.ids["txt_lect_code"].text,
                                          self.ids["txt_id_body"].text
                                          )

    data = database_api.getCourseStudents(Cache.get("info", "token"),
                                          self.ids["txt_lect_code"].text
                                          )

    with open("data/participants.fay", "w+") as participants:
        std = []
        for d in data:
            std.append("{d0},{d1},{d2},{d3}".format(d0=d[0].title(),
                                                    d1=d[1].title(),
                                                    d2=str(d[2]),
                                                    d3=d[3].lower()
                                                    )
                       )
        participants.write(self.cipher.encrypt(str("*[SEAS-NEW-LINE]*".join(std))))
        participants.close()

    participants = open("data/participants.fay", "r")
    self.data_student_list = self.cipher.decrypt(participants.read()).split("*[SEAS-NEW-LINE]*")

    self.ids["list_participants"].adapter.data = ["{i0} {i1}".format(i0=i.split(",")[0],
                                                                     i1=i.split(",")[1]
                                                                     ) for i in self.data_student_list if len(i) > 0]


def on_list_import(s, dt):
    """
    This method creates file chooser pop-up for user to upload list of participants from excel file.
    :param s: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return:
    """

    def on_list_import_confirm(self, widget_name, file_path, mouse_pos):
        """
        This method converts uploaded excel file to csv and updates participants through server.
        :param self: It is for handling class structure.
        :param widget_name: It is for handling file chooser input.
        :param file_path: It is path of selected file.
        :param mouse_pos: It is for handling file chooser input.
        :return:
        """

        self.popup.dismiss()

        excel_to_csv.xls2csv(file_path[0],
                             "data/participants.csv"
                             )

        database_api.registerStudent(Cache.get("info", "token"),
                                     self.ids["txt_lect_code"].text,
                                     True,
                                     "data/participants.csv",
                                     Cache.get("info", "nick")
                                     )

        data = database_api.getCourseStudents(Cache.get("info", "token"),
                                              self.ids["txt_lect_code"].text
                                              )

        with open("data/participants.fay", "w+") as participants:
            std = []
            for d in data:
                std.append("{d0},{d1},{d2},{d3}".format(d0=d[0].title(),
                                                        d1=d[1].title(),
                                                        d2=str(d[2]),
                                                        d3=d[3].lower()
                                                        )
                           )
            participants.write(self.cipher.encrypt(str("*[SEAS-NEW-LINE]*".join(std))))
            participants.close()

        participants = open("data/participants.fay", "r")
        self.data_student_list = self.cipher.decrypt(participants.read()).split("*[SEAS-NEW-LINE]*")

        self.ids["list_participants"].adapter.data = ["{i0} {i1}".format(i0=i.split(",")[0],
                                                                         i1=i.split(",")[1]
                                                                         ) for i in self.data_student_list]

    popup_content = FloatLayout()
    s.popup = Popup(title="Import List Of Students",
                    content=popup_content,
                    separator_color=[140 / 255., 55 / 255., 95 / 255., 1.],
                    size_hint=(None, None),
                    size=(s.width / 2, s.height / 2)
                    )
    filechooser = FileChooserListView(path=Cache.get("config", "path"),
                                      filters=["*.xlsx"],
                                      size=(s.width, s.height),
                                      pos_hint={"center_x": .5, "center_y": .5}
                                      )
    filechooser.bind(on_submit=partial(on_list_import_confirm,
                                       s
                                       )
                     )
    popup_content.add_widget(filechooser)
    popup_content.add_widget(Button(text="Upload",
                                    font_name="data/font/LibelSuit.ttf",
                                    font_size=s.height / 40,
                                    background_normal="data/img/widget_green.png",
                                    background_down="data/img/widget_green_select.png",
                                    size_hint_x=.5,
                                    size_hint_y=None,
                                    height=s.height / 20,
                                    pos_hint={"center_x": .25, "y": .0},
                                    on_release=filechooser.on_submit)  # TODO
                             )
    popup_content.add_widget(Button(text="Cancel",
                                    font_name="data/font/LibelSuit.ttf",
                                    font_size=s.height / 40,
                                    background_normal="data/img/widget_red.png",
                                    background_down="data/img/widget_red_select.png",
                                    size_hint_x=.5,
                                    size_hint_y=None,
                                    height=s.height / 20,
                                    pos_hint={"center_x": .75, "y": .0},
                                    on_release=s.popup.dismiss)
                             )
    s.popup.open()


def on_help(s):
    pass  # TODO


def on_contact(s):
    """
    This method creates pop-up for sending e-mails through form.
    :param s: It is for handling class structure.
    :return:
    """

    def on_contact_send(self, dt):
        """
        This method sends e-mail to specified e-mail address.
        :param self: It is for handling class structure.
        :param dt: It is for handling callback input.
        :return:
        """

        self.ico_status_contact.opacity = 0

        try:
            if self.input_message.text.strip():
                server = smtplib.SMTP("smtp.zoho.com",
                                      587
                                      )
                server.starttls()
                server.login("contact@wivernsoftware.com",
                             "Dragos!2017"
                             )

                send_time = datetime.now().strftime("%d %B %Y, %I:%M%p")

                message = MIMEText("{nick} ({mail}) on {date} via SEAS:\n\n{msg}".format(nick=Cache.get("info", "nick"),
                                                                                         mail=Cache.get("info", "mail"),
                                                                                         date=send_time,
                                                                                         msg=self.input_message.text
                                                                                         )
                                   )
                message["Subject"] = "SEAS: {about}".format(about=self.input_subject.text)

                server.sendmail("contact@wivernsoftware.com",
                                ["wivernsoft@gmail.com",
                                 "alioz@std.sehir.edu.tr",
                                 "fatihgulmez@std.sehir.edu.tr",
                                 "muhammedyildirim@std.sehir.edu.tr"],
                                message.as_string()
                                )
                server.quit()

                self.ico_status_contact.source = "data/img/ico_status_success.png"
                self.ico_status_contact.opacity = 1
            else:
                self.ico_status_contact.source = "data/img/ico_status_warning.png"
                self.ico_status_contact.opacity = 1
        except smtplib.SMTPException:
            self.ico_status_contact.source = "data/img/ico_status_fail.png"
            self.ico_status_contact.opacity = 1
        finally:
            self.popup.dismiss()

    popup_content = FloatLayout()
    s.popup = Popup(title="Contact Us",
                    content=popup_content,
                    separator_color=[140 / 255., 55 / 255., 95 / 255., 1.],
                    size_hint=(None, None),
                    size=(s.width / 2, s.height / 2)
                    )
    s.input_subject = TextInput(hint_text="Subject",
                                write_tab=False,
                                multiline=False,
                                font_name="data/font/CaviarDreams_Bold.ttf",
                                font_size=s.height / 36,
                                background_normal="data/img/widget_gray_75.png",
                                background_active="data/img/widget_purple_75_select.png",
                                background_disabled_normal="data/img/widget_black_75.png",
                                padding_y=[s.height / 36, 0],
                                size_hint=(.9, .2),
                                pos_hint={"center_x": .5, "center_y": .85}
                                )
    popup_content.add_widget(s.input_subject)
    s.input_message = TextInput(hint_text="Message",
                                font_name="data/font/CaviarDreams_Bold.ttf",
                                font_size=s.height / 36,
                                background_normal="data/img/widget_gray_75.png",
                                background_active="data/img/widget_purple_75_select.png",
                                background_disabled_normal="data/img/widget_black_75.png",
                                padding_y=[s.height / 36, 0],
                                size_hint=(.9, .5),
                                pos_hint={"center_x": .5, "center_y": .45}
                                )
    popup_content.add_widget(s.input_message)
    s.ico_status_contact = Image(source="data/img/ico_status_warning.png",
                                 allow_stretch=True,
                                 opacity=0,
                                 size_hint=(.15, .15),
                                 pos_hint={"center_x": .9, "center_y": .85}
                                 )
    popup_content.add_widget(s.ico_status_contact)
    popup_content.add_widget(Button(text="Send",
                                    font_name="data/font/LibelSuit.ttf",
                                    font_size=s.height / 40,
                                    background_normal="data/img/widget_green.png",
                                    background_down="data/img/widget_green_select.png",
                                    size_hint_x=.5,
                                    size_hint_y=None,
                                    height=s.height / 20,
                                    pos_hint={"center_x": .25, "y": .0},
                                    on_release=partial(on_contact_send,
                                                       s
                                                       )
                                    )
                             )
    popup_content.add_widget(Button(text="Cancel",
                                    font_name="data/font/LibelSuit.ttf",
                                    font_size=s.height / 40,
                                    background_normal="data/img/widget_red.png",
                                    background_down="data/img/widget_red_select.png",
                                    size_hint_x=.5,
                                    size_hint_y=None,
                                    height=s.height / 20,
                                    pos_hint={"center_x": .75, "y": .0},
                                    on_release=s.popup.dismiss)
                             )
    s.popup.open()
