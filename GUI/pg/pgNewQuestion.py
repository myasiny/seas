from kivy.uix.spinner import Spinner

import sys
sys.path.append("../..")

from functools import partial
from GUI.func import database_api

def on_pre_enter(self):
    # self.question_no = DatabaseAPI...
    self.question_no = 0

    self.ids["txt_question_no"].text = "Question %d" % self.question_no

    self.correct_answer = Spinner(text="Correct Answer", values=("A", "B", "C", "D", "E"),
                                  color=(1, 1, 1, 1),
                                  font_name="font/CaviarDreams_Bold.ttf",
                                  font_size=self.height / 40,
                                  background_normal="img/widget_100.png",
                                  background_down="img/widget_100_selected.png",
                                  size_hint=(.4, .05), pos_hint={"center_x": .75, "center_y": .075})
    self.correct_answer.bind(text=partial(on_correct_answer_selected, self))
    self.correct_answer.option_cls.font_name = "font/CaviarDreams_Bold.ttf"
    self.correct_answer.option_cls.background_normal = "img/widget_75_black_crop.png"
    self.correct_answer.option_cls.background_down = "img/widget_100_selected.png"
    self.correct_answer.text_autoupdate = True
    self.add_widget(self.correct_answer)

    self.correct_answer.size_hint_y = 0
    self.correct_answer.opacity = 0
    self.ids["input_input"].size_hint_y = 0
    self.ids["input_input"].opacity = 0
    self.ids["input_output"].size_hint_y = 0
    self.ids["input_output"].opacity = 0
    self.ids["input_answer_a"].size_hint_y = 0
    self.ids["input_answer_a"].opacity = 0
    self.ids["input_answer_b"].size_hint_y = 0
    self.ids["input_answer_b"].opacity = 0
    self.ids["input_answer_c"].size_hint_y = 0
    self.ids["input_answer_c"].opacity = 0
    self.ids["input_answer_d"].size_hint_y = 0
    self.ids["input_answer_d"].opacity = 0
    self.ids["input_answer_e"].size_hint_y = 0
    self.ids["input_answer_e"].opacity = 0
    self.ids["input_short_answer"].size_hint_y = 0
    self.ids["input_short_answer"].opacity = 0

    check_1 = self.ids["check_1"]
    check_1.background_radio_normal = "img/widget_75_black_circle.png"
    check_1.background_radio_down = "img/widget_75_black_circle_selected.png"
    check_1.bind(active=partial(on_type_checked, self, "programming"))

    check_2 = self.ids["check_2"]
    check_2.background_radio_normal = "img/widget_75_black_circle.png"
    check_2.background_radio_down = "img/widget_75_black_circle_selected.png"
    check_2.bind(active=partial(on_type_checked, self, "short_answer"))

    check_3 = self.ids["check_3"]
    check_3.background_radio_normal = "img/widget_75_black_circle.png"
    check_3.background_radio_down = "img/widget_75_black_circle_selected.png"
    check_3.bind(active=partial(on_type_checked, self, "multiple_choice"))

    self.question_type = "none"

def on_type_checked(self, name, checkbox, value):
    if name == "programming":
        self.question_type = "programming"

        self.correct_answer.size_hint_y = 0
        self.correct_answer.opacity = 0
        self.ids["input_answer_a"].size_hint_y = 0
        self.ids["input_answer_a"].opacity = 0
        self.ids["input_answer_b"].size_hint_y = 0
        self.ids["input_answer_b"].opacity = 0
        self.ids["input_answer_c"].size_hint_y = 0
        self.ids["input_answer_c"].opacity = 0
        self.ids["input_answer_d"].size_hint_y = 0
        self.ids["input_answer_d"].opacity = 0
        self.ids["input_answer_e"].size_hint_y = 0
        self.ids["input_answer_e"].opacity = 0
        self.ids["input_short_answer"].size_hint_y = 0
        self.ids["input_short_answer"].opacity = 0
        self.ids["input_input"].size_hint_y = 0.3
        self.ids["input_input"].opacity = 1
        self.ids["input_output"].size_hint_y = 0.3
        self.ids["input_output"].opacity = 1
    elif name == "short_answer":
        self.question_type = "short_answer"

        self.correct_answer.size_hint_y = 0
        self.correct_answer.opacity = 0
        self.ids["input_input"].size_hint_y = 0
        self.ids["input_input"].opacity = 0
        self.ids["input_output"].size_hint_y = 0
        self.ids["input_output"].opacity = 0
        self.ids["input_answer_a"].size_hint_y = 0
        self.ids["input_answer_a"].opacity = 0
        self.ids["input_answer_b"].size_hint_y = 0
        self.ids["input_answer_b"].opacity = 0
        self.ids["input_answer_c"].size_hint_y = 0
        self.ids["input_answer_c"].opacity = 0
        self.ids["input_answer_d"].size_hint_y = 0
        self.ids["input_answer_d"].opacity = 0
        self.ids["input_answer_e"].size_hint_y = 0
        self.ids["input_answer_e"].opacity = 0
        self.ids["input_short_answer"].size_hint_y = 0.675
        self.ids["input_short_answer"].opacity = 1
    else:
        self.question_type = "multiple_choice"

        self.ids["input_input"].size_hint_y = 0
        self.ids["input_input"].opacity = 0
        self.ids["input_output"].size_hint_y = 0
        self.ids["input_output"].opacity = 0
        self.ids["input_short_answer"].size_hint_y = 0
        self.ids["input_short_answer"].opacity = 0
        self.ids["input_answer_a"].size_hint_y = 0.1
        self.ids["input_answer_a"].opacity = 1
        self.ids["input_answer_b"].size_hint_y = 0.1
        self.ids["input_answer_b"].opacity = 1
        self.ids["input_answer_c"].size_hint_y = 0.1
        self.ids["input_answer_c"].opacity = 1
        self.ids["input_answer_d"].size_hint_y = 0.1
        self.ids["input_answer_d"].opacity = 1
        self.ids["input_answer_e"].size_hint_y = 0.1
        self.ids["input_answer_e"].opacity = 1
        self.correct_answer.size_hint_y = 0.05
        self.correct_answer.opacity = 1

def on_correct_answer_selected(self, spinner, text):
    self.multiple_choice_answer = text

def on_new_question_next(self):
    self.ids["img_wrong_grade"].opacity = 0
    self.ids["img_wrong_question_body"].opacity = 0
    self.ids["img_wrong_a"].opacity = 0
    self.ids["img_wrong_b"].opacity = 0
    self.ids["img_wrong_c"].opacity = 0
    self.ids["img_wrong_d"].opacity = 0
    self.ids["img_wrong_e"].opacity = 0
    self.ids["img_wrong_question_type"].opacity = 0

    if self.ids["input_grade"].text == "":
        self.ids["img_wrong_grade"].opacity = 1
        return
    elif self.ids["input_question_body"].text == "":
        self.ids["img_wrong_question_body"].opacity = 1
        return
    else:
        if self.question_type == "programming":
            yson = {self.question_no: {"type": self.question_type,
                                       "subject": self.ids["input_subject"].text,
                                       "text": self.ids["input_question_body"].text,
                                       "answer": None,
                                       "inputs": [self.ids["input_input"].text.split(";")],
                                       "outputs": [self.ids["input_output"].text.split(";")],
                                       "value": int(self.ids["input_value"].text),
                                       "tags": self.ids["input_tags"].text.split(",")}
                    }
        elif self.question_type == "short_answer":
            yson = {self.question_no: {"type": self.question_type,
                                       "subject": self.ids["input_subject"].text,
                                       "text": self.ids["input_question_body"].text,
                                       "answer": self.ids["input_short_answer"].text,
                                       "inputs": None,
                                       "outputs": None,
                                       "value": int(self.ids["input_value"].text),
                                       "tags": self.ids["input_tags"].text.split(",")}
                    }
        elif self.question_type == "multiple_choice":
            if self.ids["input_answer_a"].text == "":
                self.ids["img_wrong_a"].opacity = 1
                return
            elif self.ids["input_answer_b"].text == "":
                self.ids["img_wrong_b"].opacity = 1
                return
            elif self.ids["input_answer_c"].text == "":
                self.ids["img_wrong_c"].opacity = 1
                return
            elif self.ids["input_answer_d"].text == "":
                self.ids["img_wrong_d"].opacity = 1
                return
            elif self.ids["input_answer_e"].text == "":
                self.ids["img_wrong_e"].opacity = 1
                return
            else:
                yson = {self.question_no: {"type": self.question_type,
                                           "subject": self.ids["input_subject"].text,
                                           "text": self.ids["input_question_body"].text + "\n\n" +
                                                   "A)\t" + self.ids["input_answer_a"].text + "\n" +
                                                   "B)\t" + self.ids["input_answer_b"].text + "\n" +
                                                   "C)\t" + self.ids["input_answer_c"].text + "\n" +
                                                   "D)\t" + self.ids["input_answer_d"].text + "\n" +
                                                   "E)\t" + self.ids["input_answer_e"].text,
                                           "answer": self.multiple_choice_answer,
                                           "inputs": None,
                                           "outputs": None,
                                           "value": int(self.ids["input_value"].text),
                                           "tags": self.ids["input_tags"].text.split(",")}
                        }
        else:
            self.ids["img_wrong_question_type"].opacity = 1
            return

        temp_selected_lect = open("data/temp_selected_lect.seas", "r")
        self.data_selected_lect = temp_selected_lect.readlines()

        database_api.createExam("http://192.168.43.164:8888", "istanbul sehir university",
                                self.data_selected_lect[0].replace("\n", ""),
                                self.data_selected_lect[2].replace("\n", ""),
                                self.data_selected_lect[4],
                                int(self.data_selected_lect[3].replace("\n", "")),
                                yson)
    # TODO: Next Question

def on_new_question_previous(self):
    pass
    # TODO: Previous Question

def on_new_question_complete(self):
    pass
    # TODO: Complete Exam Creation