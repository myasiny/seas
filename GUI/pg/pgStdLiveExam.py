from kivy.uix.spinner import Spinner

import sys
sys.path.append("../..")

import subprocess32
from functools import partial
from GUI.func import database_api
from pygments.lexers.python import PythonLexer

def on_pre_enter(self):
    # self.question_type = DatabaseAPI...
    self.question_type = "programming"

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
    self.correct_answer.option_cls.font_name = "font/CaviarDreams_Bold.ttf"
    self.correct_answer.option_cls.background_normal = "img/widget_75_black_crop.png"
    self.correct_answer.option_cls.background_down = "img/widget_100_selected.png"
    self.correct_answer.text_autoupdate = True
    self.add_widget(self.correct_answer)

    if self.question_type == "programming":
        self.run_or_pause = "run"
        self.ids["input_code_answer"].lexer = PythonLexer()
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

def on_run(self):
    if self.run_or_pause == "run":
        self.ids["img_run"].source = "img/ico_pause.png"
        self.ids["img_run"].reload()

        self.run_or_pause = "pause"

        to_compile = open("data/temp_student_code.py", "w")
        to_compile.write(self.ids["input_code_answer"].text)
        to_compile.close()

        try:
            try:
                temp_output = subprocess32.check_output(["python", "data/temp_student_code.py"], stderr=subprocess32.STDOUT, timeout=10)
            except subprocess32.CalledProcessError as e:
                temp_output = e.output.split("\n")[-3][:-1] + "\n" + e.output.split("\n")[-2][:-1]
        except:
            temp_output = "TimeoutError: infinite loop or something"
            print ("SEAS [ERROR]: pgStdLiveExam > Except > Compiling Took So Long")
        finally:
            self.ids["txt_code_output"].text = temp_output

            self.ids["img_run"].source = "img/ico_run.png"
            self.ids["img_run"].reload()

            self.run_or_pause = "run"
    else:
        self.ids["img_run"].source = "img/ico_run.png"
        self.ids["img_run"].reload()

        self.run_or_pause = "run"

        pass
        # TODO: Threading & stop running when pressed