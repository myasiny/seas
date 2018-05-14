"""
eduGrade
========

`eduGrade` is a toolbox for main app, it contains necessary methods that EduGrade page requires.
"""

import code
import re
from functools import partial
import os
import psutil
import subprocess32
import sys
from StringIO import StringIO
from gensim.summarization import keywords, summarize

from kivy.adapters.listadapter import ListAdapter
from kivy.cache import Cache
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.popup import Popup

from func import database_api, image_button

__author__ = "Muhammed Yasin Yildirim"
__credits__ = ["Ali Emre Oz"]


def on_pre_enter(self):
    """
    This method maintains order of questions to provide one by one.
    :param self: It is for handling class structure.
    :return:
    """

    cipher = Cache.get("config",
                       "cipher"
                       )

    self.ids["txt_student_name"].text = Cache.get("lect",
                                                  "std_name"
                                                  )

    questions = open("data/questions.fay", "r")
    try:
        self.data_exam_order = cipher.decrypt(questions.read()).split("*[SEAS-NEW-LINE]*")
    except:
        self.data_exam_order = questions.readlines()
    questions.close()

    if len(self.data_exam_order) < 1:
        self.data_detailed_exam = database_api.getExam(Cache.get("info", "token"),
                                                       Cache.get("lect", "code"),
                                                       Cache.get("lect", "exam")
                                                       )["Questions"]

        i = 0
        with open("data/questions.fay", "w+") as questions:
            for key, value in self.data_detailed_exam.iteritems():
                if i == 0:
                    i += 1
                    # questions.write(cipher.encrypt("*[SEAS-PASS]*"))
                else:
                    questions.write(cipher.encrypt(str(value["ID"]) + "*[SEAS-NEW-LINE]*" +
                                                   str(value["type"]) + "*[SEAS-NEW-LINE]*" +
                                                   str(value["value"]) + "*[SEAS-NEW-LINE]*" +
                                                   str(value["text"]) + "*[SEAS-NEW-LINE]*" +
                                                   str(value["answer"]) + "*[SEAS-NEW-LINE]*"
                                                   )
                                    )
            questions.close()

        self.question_no = str(self.data_detailed_exam.values()[0]["ID"])
        self.ids["txt_question_no"].text = "Question ID: {id}".format(id=self.question_no)

        question_details = self.data_detailed_exam[self.data_detailed_exam.keys()[0]]

        self.question_type = question_details["type"]

        self.question_grade = str(question_details["value"])
        self.ids["txt_question_grade"].text = "Out of {point}".format(point=self.question_grade)

        self.question_body = question_details["text"]
        self.ids["txt_question_body"].text = self.question_body.replace("*[SEAS-SLASH-N]*",
                                                                        "\n"
                                                                        )

        self.answer_body = question_details["answer"]
        self.ids["txt_answer_body"].text = self.answer_body.replace("*[SEAS-SLASH-N]*",
                                                                    "\n"
                                                                    )
    else:
        questions = open("data/questions.fay", "r")
        self.data_exam_order = cipher.decrypt(questions.read()).split("*[SEAS-NEW-LINE]*")
        questions.close()

        if "*[SEAS-EXAM]*" in self.data_exam_order[0]:
            return self.on_student_change()

        self.question_no = self.data_exam_order[0]
        self.ids["txt_question_no"].text = "Question ID: {id}".format(id=self.question_no)

        self.question_type = self.data_exam_order[1]

        self.question_grade = self.data_exam_order[2]
        self.ids["txt_question_grade"].text = "Out of {point}".format(point=self.question_grade)

        self.question_body = self.data_exam_order[3]
        self.ids["txt_question_body"].text = self.question_body.replace("*[SEAS-SLASH-N]*",
                                                                        "\n"
                                                                        )

        self.answer_body = self.data_exam_order[4]
        self.ids["txt_answer_body"].text = self.answer_body.replace("*[SEAS-SLASH-N]*",
                                                                    "\n"
                                                                    )

        try:
            is_next = self.data_exam_order[4] + self.data_exam_order[5] + self.data_exam_order[6]
        except:
            is_next = None

            with open("data/questions.fay", "w+") as questions:
                questions.write(cipher.encrypt("*[SEAS-EXAM]**[SEAS-NEW-LINE]**[SEAS-IS]**[SEAS-NEW-LINE]**[SEAS-OVER]*"))
                questions.close()

        if is_next is not None:
            with open("data/questions.fay", "w+") as questions:
                questions.write(cipher.encrypt("*[SEAS-NEW-LINE]*".join(self.data_exam_order)))
                questions.close()

    data_student_answer = database_api.getAnswersOfStudent(Cache.get("info", "token"),
                                                           Cache.get("lect", "code"),
                                                           Cache.get("lect", "exam"),
                                                           Cache.get("lect", "std_id")
                                                           )

    for answer in data_student_answer:
        if str(answer[1]) == self.question_no:
            widget = ["input_grade",
                      "btn_grade_submit"
                      ]
            for name in widget:
                self.ids[name].disabled = False

            self.ids["txt_auto_grade"].text = "Auto Grade: {grade}".format(grade="TODO")  # TODO

            if self.question_type == "short_answer":
                data_summary = summarize(answer[3][1:-1].replace("*[SEAS-SLASH-N]*",
                                                                 "\n"
                                                                 ),
                                         ratio=0.3
                                         )
                self.ids["txt_answer_summary"].text = data_summary

                data_keywords = keywords(answer[3].replace("*[SEAS-SLASH-N]*",
                                                           "\n"
                                                           ),
                                         ratio=0.3
                                         )
                data_keywords = data_keywords.encode("utf-8").split("\n")
                for word in data_keywords:
                    answer[3] = re.sub(r'( |^)({keyword})'.format(keyword=word),
                                       r'\1[color=#FF4530][font=data/font/AndaleMono.ttf][b]\2[/b][/font][/color]',
                                       answer[3],
                                       flags=re.I
                                       )
                self.ids["txt_answer_student"].text = answer[3].replace("*[SEAS-SLASH-N]*", "\n")[1:-1]
            elif self.question_type == "programming":
                self.ids["txt_answer_summary_head"].text = "Output:"

                self.btn_run = image_button.add_button("data/img/ico_monitor_play.png",
                                                       "data/img/ico_monitor_play_select.png",
                                                       (.025, True),
                                                       {"x": .95, "y": .675},
                                                       partial(on_run,
                                                               self
                                                               )
                                                       )
                self.add_widget(self.btn_run)

                self.ids["txt_answer_student"].text = answer[3].replace("*[SEAS-SLASH-N]*",
                                                                        "\n"
                                                                        )
            elif self.question_type == "multiple_choice":
                pass  # TODO

            break


def on_exam_grade(s):
    """
    This method creates pop-up that lists students and their grades.
    :param s: It is for handling class structure.
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
        :return: It is for changing screen to lectures page.
        """

        self.popup.dismiss()

        return self.on_lects()

    popup_content = FloatLayout()
    s.popup = Popup(title="Grades",
                    content=popup_content,
                    separator_color=[140 / 255., 55 / 255., 95 / 255., 1.],
                    size_hint=(None, None),
                    size=(s.width / 2, s.height / 2)
                    )

    s.data_students_joined = database_api.getCourseStudents(Cache.get("info", "token"),
                                                            Cache.get("lect", "code")
                                                            )

    data_students_graded = database_api.getGradesOfExam(Cache.get("info", "token"),
                                                        Cache.get("lect", "code"),
                                                        Cache.get("lect", "exam")
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

    popup_content.add_widget(Button(text="Leave",
                                    font_name="data/font/LibelSuit.ttf",
                                    font_size=s.height / 40,
                                    background_normal="data/img/widget_yellow.png",
                                    background_down="data/img/widget_yellow_select.png",
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


def on_grade_submit(self):
    """
    This method submits grade for current answer through server.
    :param self: It is for handling class structure.
    :return: It is boolean for grading other answers.
    """

    self.ids["ico_status"].opacity = 0

    if not self.ids["input_grade"].text.strip():
        if self.ids["txt_auto_grade"].text.strip(" ")[2].strip():
            grade = self.ids["txt_auto_grade"].text.split(" ")[2]
        else:
            self.ids["ico_status"].opacity = 1

            return False
    else:
        grade = self.ids["input_grade"].text

    database_api.grade_answer(Cache.get("info", "token"),
                              Cache.get("lect", "code"),
                              int(self.question_no),
                              Cache.get("lect", "std_nick"),
                              int(grade)
                              )

    return True


def on_run(self, dt):
    """
    This method runs student's answer in the background and prints its output.
    :param self: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return:
    """

    if self.run_or_pause == "run":
        self.btn_run.source = "data/img/ico_monitor_stop.png"

        self.run_or_pause = "pause"

        to_compile = open("data/temp_student_code.py", "w+")
        to_compile.write(self.ids["txt_answer_student"].text)
        to_compile.close()

        try:
            try:
                temp_output = subprocess32.check_output(["python", "data/temp_student_code.py"],
                                                        stderr=subprocess32.STDOUT,
                                                        shell=True,
                                                        timeout=10
                                                        )
                old_stdout = sys.stdout
                sys.stdout = StringIO()
                redirected_output = sys.stdout
                script = self.ids["txt_answer_student"].text
                co = code.compile_command(script,
                                          "<stdin>",
                                          "exec"
                                          )
                exec co
                sys.stdout = old_stdout
                temp_output = redirected_output.getvalue()
            except subprocess32.CalledProcessError as e:
                temp_output = "{er}\n{ror}".format(er=e.output.split("\n")[-3][:-1],
                                                   ror=e.output.split("\n")[-2][:-1]
                                                   )
        except:
            temp_output = "TimeoutError: infinite loop or something"
        finally:
            self.list_progs_ban = []
            self.list_progs_post = []
            proc = psutil.Process()
            for i in proc.open_files():
                self.list_progs_post.append(i.path)
            for i in list(set(self.list_progs_post) - set(self.list_progs_pre)):
                if os.path.splitext(i)[1] != ".ttf":
                    self.list_progs_ban.append(os.path.splitext(i))
            if len(self.list_progs_ban) == 0:
                self.ids["txt_answer_summary"].text = temp_output

                self.btn_run.source = "data/img/ico_monitor_play.png"

                self.run_or_pause = "run"
            else:
                self.ids["txt_answer_summary"].text = "SuspiciousError: disallowed action or something"
    else:
        self.btn_run.source = "data/img/ico_monitor_play.png"

        self.run_or_pause = "run"
