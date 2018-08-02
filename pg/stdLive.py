"""
stdLive
=======

`stdLive` is a toolbox for main app, it contains necessary methods that StdLive page requires.
"""

import os
import psutil
import subprocess32
from functools import partial
from pygments.lexers.python import PythonLexer

from kivy.adapters.listadapter import ListAdapter
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.popup import Popup
from kivy.cache import Cache
from kivy.clock import Clock
from kivy.uix.spinner import Spinner

from func import database_api, image_button, update_clock, datacollect_api, keyboard_listener

__author__ = "Muhammed Yasin Yildirim"
__credits__ = ["Ali Emre Oz"]


def on_pre_enter(self):
    """
    This method maintains order of questions to provide one by one.
    :param self: It is for handling class structure.
    :return:
    """

    self.add_widget(keyboard_listener.KeyboardListener(self))

    self.date_time = Clock.schedule_interval(partial(update_clock.date_time,
                                                     self.ids["txt_clock"]
                                                     ),
                                             1.0
                                             )

    self.cipher = Cache.get("config",
                            "cipher"
                            )

    self.ids["txt_exam_name"].text = Cache.get("lect",
                                               "code"
                                               )

    questions = open("data/questions.fay", "r")
    try:
        self.data_exam_order = self.cipher.decrypt(questions.read()).split("*[SEAS-NEW-LINE]*")
    except:
        self.data_exam_order = questions.readlines()
    questions.close()

    if len(self.data_exam_order) < 1:
        self.data_detailed_exam = database_api.getExam(Cache.get("info", "token"),
                                                       Cache.get("lect", "code"),
                                                       Cache.get("lect", "exam")
                                                       )["Questions"]

        with open("data/questions.fay", "w+") as questions:
            i = 0
            q = ""
            for key, value in self.data_detailed_exam.iteritems():
                if i == 0:
                    i += 1
                else:
                    q += str(value["ID"]) + "*[SEAS-NEW-LINE]*" + \
                         str(value["type"]) + "*[SEAS-NEW-LINE]*" + \
                         str(value["value"]) + "*[SEAS-NEW-LINE]*" + \
                         str(value["text"]) + "*[SEAS-NEW-LINE]*"
            questions.write(self.cipher.encrypt(q))
            questions.close()

        self.question_no = str(self.data_detailed_exam.values()[0]["ID"])
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
            is_next = self.data_exam_order[4] + self.data_exam_order[5] + self.data_exam_order[6]
        except:
            is_next = None

            with open("data/questions.fay", "w+") as questions:
                questions.write(self.cipher.encrypt("*[SEAS-EXAM]**[SEAS-NEW-LINE]**[SEAS-IS]**[SEAS-NEW-LINE]**[SEAS-OVER]*"))
                questions.close()

        if is_next is not None:
            with open("data/questions.fay", "w+") as questions:
                questions.write(self.cipher.encrypt("*[SEAS-NEW-LINE]*".join(self.data_exam_order[4:])))
                questions.close()

    self.btn_question_change = image_button.add_button("data/img/ico_menu.png",
                                                       "data/img/ico_menu_select.png",
                                                       (.025, True),
                                                       {"x": .045, "y": .8725},
                                                       partial(on_question_change,
                                                               self
                                                               )
                                                       )
    self.add_widget(self.btn_question_change)

    self.btn_run = image_button.add_button("data/img/ico_monitor_play.png",
                                           "data/img/ico_monitor_play_select.png",
                                           (.025, True),
                                           {"x": .955, "y": .81},
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
                                  size_hint=(.5, .05),
                                  pos_hint={"center_x": .71, "y": .025}
                                  )
    self.correct_answer.bind(text=partial(on_correct_answer_select,
                                          self
                                          )
                             )
    self.correct_answer.option_cls.font_name = "data/font/CaviarDreams_Bold.ttf"
    self.correct_answer.option_cls.background_down = "data/img/widget_purple_75_select.png"
    self.add_widget(self.correct_answer)

    if self.question_type == "programming":
        self.ids["img_right_side_bg"].source = "data/img/widget_green_select.png"
        self.ids["img_right_side_bg"].reload()

        self.temp_stdout = ""
        self.temp_output = ""

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
        self.ids["img_right_side_bg"].source = "data/img/widget_yellow_select.png"
        self.ids["img_right_side_bg"].reload()

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
        self.ids["img_right_side_bg"].source = "data/img/widget_red_select.png"
        self.ids["img_right_side_bg"].reload()

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

        question_body = self.ids["txt_question_body"].text.split("*[SEAS-CHOICES]*")
        self.ids["txt_question_body"].text = question_body[0]
        self.ids["txt_multiple_choices"].text = question_body[1]

    self.list_progs_pre = []
    proc = psutil.Process()
    for i in proc.open_files():
        self.list_progs_pre.append(i.path)

    self.listen = Clock.schedule_interval(partial(datacollect_api.post_data,
                                                  Cache.get("info", "token"),
                                                  Cache.get("lect", "code"),
                                                  Cache.get("lect", "exam"),
                                                  Cache.get("info", "id"),
                                                  self
                                                  ),
                                          5
                                          )

    # self.watch = Clock.schedule_interval(partial(database_api.postStats(Cache.get("lect", "code"),
    #                                                                     Cache.get("info", "id"),
    #                                                                     {"TODO": 0}
    #                                                                     )
    #                                              ),
    #                                      10
    #                                      )
    #
    # self.prtsc = Clock.schedule_interval(partial(database_api.postScreenshots(Cache.get("lect", "code"),
    #                                                                           Cache.get("lect", "exam"),
    #                                                                           Cache.get("info", "id"),
    #                                                                           {"TODO": 0}
    #                                                                           )
    #                                              ),
    #                                      10
    #                                      )


def on_question_change(s, dt):
    """
    This method allows jumping to selected question through popup.
    :param s: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return:
    """

    def on_question_select(self, dt):
        """
        This method switches screen for answering selected question.
        :param self: It is for handling class structure.
        :param dt: It is for handling callback input.
        :return: It is for changing screen to selected question's page.
        """

        self.popup.dismiss()

        questions = open("data/questions.fay", "w+")
        questions_all = ""

        question_id = self.list_quests.adapter.selection[0].text.split(" ")[1]
        for key in self.data_all_ids.iterkeys():
            if question_id == key.split("*[SEAS-LIST-VIEW]*")[0]:
                questions_all += self.data_all_ids[key]
                break

        for key, value in self.data_all_ids.iteritems():
            if not question_id == key.split("*[SEAS-LIST-VIEW]*")[0]:
                questions_all += value

        questions.write(self.cipher.encrypt(bytes(questions_all)))
        questions.close()

        return self.on_question_skip()

    def color_hex(x):
        """
        This method determines hex color code for given question according to its type.
        :param x: It is type of question.
        :return: It is hex code of color.
        """

        quest_hex = {"choice": "FF4530",
                     "short": "FCAA03",
                     "code": "5CB130"
                     }

        if x == "programming":
            hex_code = quest_hex["code"]
        elif x == "short_answer":
            hex_code = quest_hex["short"]
        else:
            hex_code = quest_hex["choice"]

        return hex_code

    s.data_all_questions = database_api.getExam(Cache.get("info", "token"),
                                                Cache.get("lect", "code"),
                                                Cache.get("lect", "exam")
                                                )["Questions"]
    s.data_all_ids = {}
    for q in s.data_all_questions.itervalues():
        data_question = str(q["ID"]) + "*[SEAS-NEW-LINE]*" + \
                        q["type"] + "*[SEAS-NEW-LINE]*" + \
                        str(q["value"]) + "*[SEAS-NEW-LINE]*" + \
                        q["text"] + "*[SEAS-NEW-LINE]*"
        s.data_all_ids[str(q["ID"]) + "*[SEAS-LIST-VIEW]*" + q["type"]] = data_question

    popup_content = FloatLayout()
    s.popup = Popup(title="Questions",
                    content=popup_content,
                    separator_color=[140 / 255., 55 / 255., 95 / 255., 1.],
                    size_hint=(None, None),
                    size=(s.width / 2, s.height / 2)
                    )

    s.list_quests = ListView(size_hint=(.9, .8),
                             pos_hint={"center_x": .5, "center_y": .55}
                             )

    args_converter = lambda row_index, x: {"text": "ID: {id} - Type: [color=#{hex}]{qtype}[/color]".format(id=x[0],
                                                                                                           hex=color_hex(x[1]),
                                                                                                           qtype=x[1].replace("_",
                                                                                                                              " "
                                                                                                                              ).title()
                                                                                                           ),
                                           "markup": True,
                                           "selected_color": (.843, .82, .82, 1),
                                           "deselected_color": (.57, .67, .68, 1),
                                           "background_down": "data/img/widget_gray_75.png",
                                           "font_name": "data/font/CaviarDreams_Bold.ttf",
                                           "font_size": s.height / 50,
                                           "size_hint_y": None,
                                           "height": s.height / 20,
                                           "on_release": partial(on_question_select,
                                                                 s
                                                                 )
                                           }
    s.list_quests.adapter = ListAdapter(data=[i.split("*[SEAS-LIST-VIEW]*") for i in s.data_all_ids.iterkeys()],
                                        cls=ListItemButton,
                                        args_converter=args_converter,
                                        allow_empty_selection=False
                                        )
    popup_content.add_widget(s.list_quests)

    popup_content.add_widget(Button(text="Close",
                                    font_name="data/font/LibelSuit.ttf",
                                    font_size=s.height / 40,
                                    background_normal="data/img/widget_red.png",
                                    background_down="data/img/widget_red_select.png",
                                    size_hint_x=1,
                                    size_hint_y=None,
                                    height=s.height / 20,
                                    pos_hint={"center_x": .5, "y": .0},
                                    on_release=s.popup.dismiss)
                             )

    s.popup.open()


def on_correct_answer_select(self, spinner, text):
    """
    This method assigns option selected from multiple choice spinner as correct answer.
    :param self: It is for handling class structure.
    :param spinner: It is spinner for multiple choice question.
    :param text: It is option selected from multiple choice spinner.
    :return:
    """

    self.answer = text
    self.multiple_choice_answer = text


def read_stdout(self, dt):
    """
    This method updates output widget periodically.
    :param self: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return:
    """

    self.temp_stdout += self.temp_output
    self.ids["txt_code_output"].text = self.temp_output


def on_run(self, dt):
    """
    This method runs student's answer in the background and prints its output.
    :param self: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return:
    """

    if self.run_or_pause == "run":
        self.btn_run.source = "data/img/ico_monitor_stop.png"
        self.btn_run.reload()

        self.run_or_pause = "pause"

        self.temp_output = ""

        to_compile = open("data/temp_student_code.py", "w+")
        to_compile.write(self.ids["input_code_answer"].text)
        to_compile.close()

        try:
            try:
                self.reader = Clock.schedule_interval(partial(read_stdout,
                                                              self),
                                                      0.2)

                self.temp_output = subprocess32.check_output(["python", "data/temp_student_code.py"],
                                                             stderr=subprocess32.STDOUT,
                                                             timeout=5
                                                             )
            except subprocess32.CalledProcessError as e:
                self.temp_output = "{er}\n{ror}".format(er=e.output.split("\n")[-3][:-1],
                                                        ror=e.output.split("\n")[-2][:-1]
                                                        )
                self.ids["txt_code_output"].text = self.temp_output
            except subprocess32.TimeoutExpired:
                self.temp_output = "TimeoutError: infinite loop or something"  # + "\n------------\n" + self.temp_stdout
                self.ids["txt_code_output"].text = self.temp_output
            finally:
                self.reader.cancel()
        except:
            self.temp_output = "CompileError: broken compiler or something"
            self.ids["txt_code_output"].text = self.temp_output
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
                self.ids["txt_code_output"].text = self.temp_output

                self.btn_run.source = "data/img/ico_monitor_play.png"
                self.btn_run.reload()

                self.run_or_pause = "run"
            else:
                self.temp_output = "SuspiciousError: disallowed action or something"
                self.ids["txt_code_output"].text = self.temp_output
    else:
        self.btn_run.source = "data/img/ico_monitor_play.png"
        self.btn_run.reload()

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
        try:
            students_choice = self.multiple_choice_answer
        except:
            students_choice = ""

        database_api.sendAnswers(Cache.get("info", "token"),
                                 Cache.get("lect", "code"),
                                 self.question_no,
                                 Cache.get("info", "nick"),
                                 students_choice
                                 )

        return True
    else:
        return False


def on_leave(self):
    """
    This method cancels scheduled methods to update time widget etc. when user leaves page.
    :param self: It is for handling class structure.
    :return:
    """

    self.date_time.cancel()

    try:
        self.listen.cancel()
    except:
        pass

    # self.watch.cancel()
    # self.prtsc.cancel()
