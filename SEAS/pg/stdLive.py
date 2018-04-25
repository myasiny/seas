"""
stdLive
=======

`stdLive` is a toolbox for main app, it contains necessary methods that StdLive page requires.
"""

import code
import json
import os
import psutil
import subprocess32
import sys
from functools import partial

from StringIO import StringIO
from kivy.cache import Cache
from kivy.clock import Clock
from kivy.uix.spinner import Spinner
from pygments.lexers.python import PythonLexer

from func import database_api, image_button, update_clock

__author__ = "Muhammed Yasin Yildirim"
__credits__ = ["Ali Emre Oz"]


def on_pre_enter(self):
    """
    This method maintains order of questions to provide one by one.
    :param self: It is for handling class structure.
    :return:
    """

    self.date_time = Clock.schedule_interval(partial(update_clock.date_time,
                                                     self.ids["txt_clock"]
                                                     ),
                                             1.0
                                             )

    self.cipher = Cache.get("config",
                            "cipher"
                            )

    questions = open("data/questions.fay", "r")
    try:
        self.data_exam_order = self.cipher.decrypt(questions.read()).split("*[SEAS-NEW-LINE]*")
    except:
        self.data_exam_order = questions.readlines()

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
                else:
                    questions.write(self.cipher.encrypt(str(key) + "*[SEAS-NEW-LINE]*" +
                                                        str(value["type"]) + "*[SEAS-NEW-LINE]*" +
                                                        str(value["value"]) + "*[SEAS-NEW-LINE]*" +
                                                        str(value["text"]) + "*[SEAS-NEW-LINE]*"
                                                        )
                                    )
            questions.close()

        self.question_no = str(self.data_detailed_exam.keys()[0])
        self.ids["txt_question_no"].text = "Question ID: {id}".format(id=self.question_no)

        question_details = self.data_detailed_exam[self.data_detailed_exam.keys()[0]]

        self.question_type = question_details["type"]

        self.question_grade = str(question_details["value"])
        self.ids["txt_question_grade"].text = "Grade: {point}".format(point=self.question_grade)

        self.question_body = question_details["text"]
        self.ids["txt_question_body"].text = self.question_body.replace("*[SEAS-SLASH-N]*",
                                                                        "\n"
                                                                        )
    else:
        questions = open("data/questions.fay", "r")
        self.data_exam_order = self.cipher.decrypt(questions.read()).split("*[SEAS-NEW-LINE]*")

        if "*[SEAS-EXAM]*" in self.data_exam_order[0]:
            return self.on_lects()

        self.question_no = self.data_exam_order[0]
        self.ids["txt_question_no"].text = "Question ID: {id}".format(id=self.question_no)

        self.question_type = self.data_exam_order[1]

        self.question_grade = self.data_exam_order[2]
        self.ids["txt_question_grade"].text = "Grade: {point}".format(point=self.question_grade)

        self.question_body = self.data_exam_order[3]
        self.ids["txt_question_body"].text = self.question_body.replace("*[SEAS-SLASH-N]*",
                                                                        "\n"
                                                                        )

        try:
            is_next = self.data_exam_order[5] + self.data_exam_order[6] + self.data_exam_order[7]
        except:
            is_next = None

            with open("data/questions.fay", "w+") as questions:
                questions.write(self.cipher.encrypt("*[SEAS-EXAM]**[SEAS-NEW-LINE]**[is]**[SEAS-NEW-LINE]**[SEAS-OVER]*"))
                questions.close()

        if is_next is not None:
            with open("data/questions.fay", "w+") as questions:
                questions.write(self.cipher.encrypt("*[SEAS-NEW-LINE]*".join(self.data_exam_order)))
                questions.close()

    self.btn_run = image_button.add_button("data/img/ico_monitor_play.png",
                                           "data/img/ico_monitor_play_select.png",
                                           (.025, True),
                                           {"x": .95, "y": .7},
                                           partial(on_run,
                                                   self
                                                   )
                                           )
    self.add_widget(self.btn_run)

    self.correct_answer = Spinner(text="Answer",
                                  values=("A", "B", "C", "D", "E"),
                                  color=(1, 1, 1, 1),
                                  font_name="data/font/CaviarDreams_Bold.ttf",
                                  font_size=self.height / 40,
                                  background_normal="data/img/widget_purple_75.png",
                                  background_down="data/img/widget_purple_75_select.png",
                                  size_hint=(.4, .05),
                                  pos_hint={"center_x": .75, "center_y": .075}
                                  )
    self.correct_answer.bind(text=partial(on_correct_answer_select,
                                          self
                                          )
                             )
    self.correct_answer.text_autoupdate = True
    self.correct_answer.option_cls.font_name = "data/font/CaviarDreams_Bold.ttf"
    self.correct_answer.option_cls.background_normal = "data/img/widget_black_75_crop.png"
    self.correct_answer.option_cls.background_down = "data/img/widget_purple_75_select.png"
    self.add_widget(self.correct_answer)

    if self.question_type == "programming":
        self.run_or_pause = "run"
        self.ids["input_code_answer"].lexer = PythonLexer()

        widget = [self.correct_answer,
                  self.ids["txt_multiple_choices_scroll"],
                  self.ids["input_short_answer"]
                  ]
        for name in widget:
            name.opacity = 0
            name.size_hint_y = 0
    elif self.question_type == "short_answer":
        self.btn_run.disabled = True

        widget = [self.correct_answer,
                  self.ids["txt_multiple_choices_scroll"],
                  self.btn_run,
                  self.ids["input_code_answer"],
                  self.ids["img_code_output_bg"],
                  self.ids["txt_code_output_scroll"]
                  ]
        for name in widget:
            name.opacity = 0
            name.size_hint_y = 0
    elif self.question_type == "multiple_choice":
        self.btn_run.disabled = True

        widget = [self.btn_run,
                  self.ids["input_code_answer"],
                  self.ids["img_code_output_bg"],
                  self.ids["txt_code_output_scroll"],
                  self.ids["input_short_answer"]
                  ]
        for name in widget:
            name.opacity = 0
            name.size_hint_y = 0

    self.list_progs_pre = []
    proc = psutil.Process()
    for i in proc.open_files():
        self.list_progs_pre.append(i.path)


def on_correct_answer_select(self, spinner, text):
    """
    This method assigns option selected from multiple choice spinner as correct answer.
    :param self: It is for handling class structure.
    :param spinner: It is spinner for multiple choice question.
    :param text: It is option selected from multiple choice spinner.
    :return:
    """

    self.multiple_choice_answer = text


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
        to_compile.write(self.ids["input_code_answer"].text)
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
                script = self.ids["input_code_answer"].text
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
                self.ids["txt_code_output"].text = temp_output

                self.btn_run.source = "data/img/ico_monitor_play.png"

                self.run_or_pause = "run"
            else:
                self.ids["txt_code_output"].text = "SuspiciousError: disallowed action or something"
    else:
        self.btn_run.source = "data/img/ico_monitor_play.png"

        self.run_or_pause = "run"


def on_submit(self):
    """
    This method submits student's answer to current question through server.
    :param self: It is for handling class structure.
    :return: It is boolean for completing submission before switching page.
    """

    if self.question_type == "programming":
        database_api.sendAnswers(Cache.get("info", "token"),
                                 Cache.get("lect", "code"),
                                 self.question_no,
                                 Cache.get("info", "nick"),
                                 self.ids["input_code_answer"].text.replace("\n",
                                                                            "*[SEAS-SLASH-N]*"
                                                                            )
                                 )

        return True
    elif self.question_type == "short_answer":
        database_api.sendAnswers(Cache.get("info", "token"),
                                 Cache.get("lect", "code"),
                                 self.question_no,
                                 Cache.get("info", "nick"),
                                 self.ids["input_short_answer"].text.replace("\n",
                                                                             "*[SEAS-SLASH-N]*"
                                                                             )
                                 )

        return True
    elif self.question_type == "multiple_choice":
        database_api.sendAnswers(Cache.get("info", "token"),
                                 Cache.get("lect", "code"),
                                 self.question_no,
                                 Cache.get("info", "nick"),
                                 self.multiple_choice_answer
                                 )

        return True
    else:
        return False


def on_leave(self):
    """
    This method cancels scheduled method to update time widget when user leaves page.
    :param self: It is for handling class structure.
    :return:
    """

    self.date_time.cancel()
