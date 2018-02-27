from kivy.uix.spinner import Spinner

import sys
sys.path.append("../..")

from functools import partial
from GUI.func import database_api

def on_pre_enter(self):
    # self.question_type = DatabaseAPI...
    self.question_type = "TODO"

    # self.question_no = DatabaseAPI...
    self.question_no = 0
    self.ids["txt_question_no"].text = "Question %d" % self.question_no

    # self.question_grade = DatabaseAPI...
    self.question_grade = 0
    self.ids["txt_question_grade"].text = "Grade: %d" % self.question_grade

    # self.question_body = DatabaseAPI...
    self.question_body = "TODO"
    self.ids["txt_question_body"].text = self.question_body

    self.correct_answer = Spinner(text="Answer", values=("A", "B", "C", "D", "E"),
                                  color=(1, 1, 1, 1),
                                  font_name="font/CaviarDreams_Bold.ttf",
                                  font_size=self.height / 40,
                                  background_normal="img/widget_100.png",
                                  background_down="img/widget_100_selected.png",
                                  size_hint=(.4, .05), pos_hint={"center_x": .75, "center_y": .075})
    self.correct_answer.bind(text=partial(on_correct_answer_selected, self))
    self.add_widget(self.correct_answer)

    if self.question_type == "programming":
        self.correct_answer.size_hint_y = 0
        self.correct_answer.opacity = 0
        self.ids["input_short_answer"].size_hint_y = 0
        self.ids["input_short_answer"].opacity = 0
        self.ids["txt_multiple_choices_scroll"].size_hint_y = 0
        self.ids["txt_multiple_choices_scroll"].opacity = 0
    elif self.question_type == "short_answer":
        self.correct_answer.size_hint_y = 0
        self.correct_answer.opacity = 0
        self.ids["input_code_answer"].size_hint_y = 0
        self.ids["input_code_answer"].opacity = 0
        self.ids["img_run"].size_hint_y = 0
        self.ids["img_run"].opacity = 0
        self.ids["btn_run"].disabled = True
        self.ids["img_code_output_bg"].size_hint_y = 0
        self.ids["img_code_output_bg"].opacity = 0
        self.ids["txt_code_output_scroll"].size_hint_y = 0
        self.ids["txt_code_output_scroll"].opacity = 0
        self.ids["txt_multiple_choices_scroll"].size_hint_y = 0
        self.ids["txt_multiple_choices_scroll"].opacity = 0
    else:
        self.ids["input_code_answer"].size_hint_y = 0
        self.ids["input_code_answer"].opacity = 0
        self.ids["img_run"].size_hint_y = 0
        self.ids["img_run"].opacity = 0
        self.ids["btn_run"].disabled = True
        self.ids["img_code_output_bg"].size_hint_y = 0
        self.ids["img_code_output_bg"].opacity = 0
        self.ids["txt_code_output_scroll"].size_hint_y = 0
        self.ids["txt_code_output_scroll"].opacity = 0
        self.ids["input_short_answer"].size_hint_y = 0
        self.ids["input_short_answer"].opacity = 0

def on_correct_answer_selected(self, spinner, text):
    self.multiple_choice_answer = text