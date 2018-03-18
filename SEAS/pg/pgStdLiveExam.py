from kivy.logger import Logger
from kivy.uix.spinner import Spinner

import subprocess32, psutil, code, sys, os, json
from StringIO import StringIO
from SEAS.func import database_api
from functools import partial
from pygments.lexers.python import PythonLexer

'''
    This method updates question information, creates multiple choice fields before entering PgStdLiveExam
    Necessary fields get visible according to question type
'''

def on_pre_enter(self):
    temp_login = open("data/temp_login.seas", "r")
    self.data_login = temp_login.readlines()

    temp_selected_lect = open("data/temp_selected_lect.seas", "r")
    self.data_selected_lect = temp_selected_lect.readlines()

    self.data_detailed_exam = database_api.getExam(self.data_login[8].replace("\n", ""),
                                                   self.data_selected_lect[0].replace("\n", ""),
                                                   self.data_selected_lect[2].replace("\n", ""))
    self.data_detailed_exam = self.data_detailed_exam["Questions"]

    self.question_no = str(self.data_detailed_exam.keys()[0])
    self.ids["txt_question_no"].text = "Question %s" % self.question_no

    question_details = json.loads(self.data_detailed_exam[self.data_detailed_exam.keys()[0]])

    self.question_type = question_details["type"]

    self.question_grade = str(question_details["value"])
    self.ids["txt_question_grade"].text = "Grade: %s" % self.question_grade

    self.question_body = question_details["text"]
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

    self.list_progs_pre = []
    proc = psutil.Process()
    for i in proc.open_files():
        self.list_progs_pre.append(i.path)

    Logger.info("pgStdLiveExam: Question %s successfully imported from server" % self.question_no)

'''
    This method is to store final answer given by student for multiple choice question
'''

def on_correct_answer_selected(self, spinner, text):
    self.multiple_choice_answer = text

'''
    This method enables student compiling code written by him or her and seeing its output
    If compiling takes more than 10 seconds, it raises timeout exception and stops compiling
'''

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

                old_stdout = sys.stdout
                sys.stdout = StringIO()
                redirected_output = sys.stdout
                script = self.ids["input_code_answer"].text
                co = code.compile_command(script, "<stdin>", "exec")
                exec co
                sys.stdout = old_stdout
                temp_output = redirected_output.getvalue()
            except subprocess32.CalledProcessError as e:
                temp_output = e.output.split("\n")[-3][:-1] + "\n" + e.output.split("\n")[-2][:-1]
        except:
            temp_output = "TimeoutError: infinite loop or something"

            Logger.error("pgStdLiveExam: Compiling student's code took more than 10 seconds, raised timeout error")
        finally:
            self.list_progs_post = []
            self.list_progs_ban = []
            proc = psutil.Process()
            for i in proc.open_files():
                self.list_progs_post.append(i.path)
            for i in list(set(self.list_progs_post) - set(self.list_progs_pre)):
                if os.path.splitext(i)[1] != ".ttf":
                    self.list_progs_ban.append(os.path.splitext(i))
            if len(self.list_progs_ban) == 0:
                self.ids["txt_code_output"].text = temp_output

                self.ids["img_run"].source = "img/ico_run.png"
                self.ids["img_run"].reload()

                self.run_or_pause = "run"
            else:
                self.ids["txt_code_output"].text = "CheatingError: do not be an asshole"
    else:
        self.ids["img_run"].source = "img/ico_run.png"
        self.ids["img_run"].reload()

        self.run_or_pause = "run"

'''
    This method TODO
'''

def on_question_previous(self):
    on_submit(self)
    return True

'''
    This method TODO
'''

def on_question_next(self):
    on_submit(self)
    return True

'''
    This method submits student's answer to current question by connecting to server and directs to PgStdLects
'''

def on_question_save(self):
    on_submit(self)

'''
    This method directs to PgStdLects without submiting student's answer to current question and student leaves exam
'''

def on_question_remove(self):
    pass

'''
    This method connects to server for saving student's answer
'''

def on_submit(self):
    if self.question_type == "programming":
        database_api.sendAnswers(self.data_login[8].replace("\n", ""), self.data_selected_lect[0].replace("\n", ""),
                                 self.data_detailed_exam.keys()[0], self.data_login[0].replace("\n", ""),
                                 self.ids["input_code_answer"].text)

        Logger.info("pgStdLiveExam: Student's answer for programming question sent to server")
    elif self.question_type == "short_answer":
        database_api.sendAnswers(self.data_login[8].replace("\n", ""), self.data_selected_lect[0].replace("\n", ""),
                                 self.data_detailed_exam.keys()[0], self.data_login[0].replace("\n", ""),
                                 self.ids["input_short_answer"].text)

        Logger.info("pgStdLiveExam: Student's answer for short answer question sent to server")
    elif self.question_type == "multiple_choice":
        database_api.sendAnswers(self.data_login[8].replace("\n", ""), self.data_selected_lect[0].replace("\n", ""),
                                 self.data_detailed_exam.keys()[0], self.data_login[0].replace("\n", ""),
                                 self.multiple_choice_answer)

        Logger.info("pgStdLiveExam: Student's answer for multiple choice question sent to server")