from kivy.cache import Cache
from kivy.logger import Logger
from kivy.uix.spinner import Spinner

from functools import partial
from SEAS.func import database_api

'''
    This method creates multiple choice fields and makes right column invisible before entering PgNewQuestion
    Necessary fields get visible according to question type selected through top-right radio buttons
    Additionally, it checks whether question is already created or not
    Accordingly, it leaves fields empty or connects to server for filling fields with given information
'''

def on_pre_enter(self):
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

    Logger.info("pgNewQuestion: Radio buttons and fields for various question types created")

    # temp_login = open("data/temp_login.seas", "r")
    # self.data_login = temp_login.readlines()

    # temp_selected_lect = open("data/temp_selected_lect.seas", "r")
    # self.data_selected_lect = temp_selected_lect.readlines()

    self.question_type = "none"

    self.data_detailed_exam = database_api.getExam(Cache.get("info", "token"),
                                                   Cache.get("lect", "code"),
                                                   Cache.get("lect", "exam"))["Questions"]

    self.ids["txt_question_no"].text = "Question"

    # if len(self.data_detailed_exam) > 0:
    #     Logger.info("pgNewQuestion: Exam already exists, editing mode on")
    #
    #     self.question_no = self.data_detailed_exam.keys()[0]
    #     self.ids["txt_question_no"].text = "Question ID: %s" % self.question_no
    #
    #     question_details = self.data_detailed_exam[self.data_detailed_exam.keys()[0]]
    #
    #     self.ids["input_subject"].text = question_details["subject"]
    #     self.ids["input_tags"].text = question_details["tags"]
    #     self.ids["input_grade"].text = str(question_details["value"])
    #     self.ids["input_question_body"].text = question_details["text"]
    #
    #     self.question_type = question_details["type"]
    #     if self.question_type == "programming":
    #         self.correct_answer.size_hint_y = 0
    #         self.correct_answer.opacity = 0
    #         self.ids["input_answer_a"].size_hint_y = 0
    #         self.ids["input_answer_a"].opacity = 0
    #         self.ids["input_answer_b"].size_hint_y = 0
    #         self.ids["input_answer_b"].opacity = 0
    #         self.ids["input_answer_c"].size_hint_y = 0
    #         self.ids["input_answer_c"].opacity = 0
    #         self.ids["input_answer_d"].size_hint_y = 0
    #         self.ids["input_answer_d"].opacity = 0
    #         self.ids["input_answer_e"].size_hint_y = 0
    #         self.ids["input_answer_e"].opacity = 0
    #         self.ids["input_short_answer"].size_hint_y = 0
    #         self.ids["input_short_answer"].opacity = 0
    #         self.ids["input_input"].size_hint_y = 0.3
    #         self.ids["input_input"].opacity = 1
    #         self.ids["input_output"].size_hint_y = 0.3
    #         self.ids["input_output"].opacity = 1
    #
    #         self.ids["input_input"].text = question_details["inputs"]
    #         self.ids["input_output"].text = question_details["outputs"]
    #     elif self.question_type == "short_answer":
    #         self.correct_answer.size_hint_y = 0
    #         self.correct_answer.opacity = 0
    #         self.ids["input_input"].size_hint_y = 0
    #         self.ids["input_input"].opacity = 0
    #         self.ids["input_output"].size_hint_y = 0
    #         self.ids["input_output"].opacity = 0
    #         self.ids["input_answer_a"].size_hint_y = 0
    #         self.ids["input_answer_a"].opacity = 0
    #         self.ids["input_answer_b"].size_hint_y = 0
    #         self.ids["input_answer_b"].opacity = 0
    #         self.ids["input_answer_c"].size_hint_y = 0
    #         self.ids["input_answer_c"].opacity = 0
    #         self.ids["input_answer_d"].size_hint_y = 0
    #         self.ids["input_answer_d"].opacity = 0
    #         self.ids["input_answer_e"].size_hint_y = 0
    #         self.ids["input_answer_e"].opacity = 0
    #         self.ids["input_short_answer"].size_hint_y = 0.675
    #         self.ids["input_short_answer"].opacity = 1
    #
    #         self.ids["input_short_answer"].text = question_details["answer"]
    #     else:
    #         self.ids["input_input"].size_hint_y = 0
    #         self.ids["input_input"].opacity = 0
    #         self.ids["input_output"].size_hint_y = 0
    #         self.ids["input_output"].opacity = 0
    #         self.ids["input_short_answer"].size_hint_y = 0
    #         self.ids["input_short_answer"].opacity = 0
    #         self.ids["input_answer_a"].size_hint_y = 0.1
    #         self.ids["input_answer_a"].opacity = 1
    #         self.ids["input_answer_b"].size_hint_y = 0.1
    #         self.ids["input_answer_b"].opacity = 1
    #         self.ids["input_answer_c"].size_hint_y = 0.1
    #         self.ids["input_answer_c"].opacity = 1
    #         self.ids["input_answer_d"].size_hint_y = 0.1
    #         self.ids["input_answer_d"].opacity = 1
    #         self.ids["input_answer_e"].size_hint_y = 0.1
    #         self.ids["input_answer_e"].opacity = 1
    #         self.correct_answer.size_hint_y = 0.05
    #         self.correct_answer.opacity = 1


'''
    This method either shows or hides widgets on PgNewQuestion whenever selected question type changes
'''

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

'''
    This method is to store correct answer selected by educator for multiple choice question
'''

def on_correct_answer_selected(self, spinner, text):
    self.multiple_choice_answer = text

'''
    This method submits question information by connecting to server and directs to PgNewQuestion again
'''

def on_new_question_next(self):
    on_submit(self)
    return True

'''
    This method submits question information by connecting to server and directs to PgNewQuestion again
'''

def on_new_question_previous(self):
    on_submit(self)
    return True

'''
    This method submits question information by connecting to server and directs to PgLects
'''

def on_new_question_complete(self):
    on_submit(self)

'''
    This method directs to PgLects without submiting question information and educator leaves question creation screen
'''

def on_new_question_cancel(self):
    pass

'''
    This method checks whether required question information provided or not
    Accordingly, it raises warning or connects to server for either creating or updating question
'''

def on_submit(self):
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
            yson = {"type": self.question_type,
                    "subject": self.ids["input_subject"].text,
                    "text": self.ids["input_question_body"].text,
                    "answer": None,
                    "inputs": [self.ids["input_input"].text.split(",")],
                    "outputs": [self.ids["input_output"].text.split(",")],
                    "value": int(self.ids["input_grade"].text),
                    "tags": self.ids["input_tags"].text.split(",")}

            database_api.addQuestionToExam(Cache.get("info", "token"),
                                           Cache.get("lect", "code"),
                                           Cache.get("lect", "exam"), yson)

            Logger.info("pgNewQuestion: Programming question created and sent to server")
        elif self.question_type == "short_answer":
            yson = {"type": self.question_type,
                    "subject": self.ids["input_subject"].text,
                    "text": self.ids["input_question_body"].text,
                    "answer": self.ids["input_short_answer"].text,
                    "inputs": None,
                    "outputs": None,
                    "value": int(self.ids["input_grade"].text),
                    "tags": self.ids["input_tags"].text.split(",")}

            database_api.addQuestionToExam(Cache.get("info", "token"),
                                           Cache.get("lect", "code"),
                                           Cache.get("lect", "exam"), yson)

            Logger.info("pgNewQuestion: Short answer question created and sent to server")
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
                yson = {"type": self.question_type,
                        "subject": self.ids["input_subject"].text,
                        "text": "{q}\n\nA) {a}\nB) {b}\nC) {c}\nD) {d}\nE) {e}".format(q=self.ids["input_question_body"].text,
                                                                                       a=self.ids["input_answer_a"].text,
                                                                                       b=self.ids["input_answer_b"].text,
                                                                                       c=self.ids["input_answer_c"].text,
                                                                                       d=self.ids["input_answer_d"].text,
                                                                                       e=self.ids["input_answer_e"].text),
                        "answer": self.multiple_choice_answer,
                        "inputs": None,
                        "outputs": None,
                        "value": int(self.ids["input_grade"].text),
                        "tags": self.ids["input_tags"].text.split(",")}

                database_api.addQuestionToExam(Cache.get("info", "token"),
                                               Cache.get("lect", "code"),
                                               Cache.get("lect", "exam"), yson)

                Logger.info("pgNewQuestion: Multiple choice question created and sent to server")
        else:
            self.ids["img_wrong_question_type"].opacity = 1
            return