"""
eduGrade
========

`eduGrade` is a toolbox for main app, it contains necessary methods that EduGrade page requires.
"""

from kivy.cache import Cache

from func import database_api

__author__ = "Muhammed Yasin Yildirim"


def on_pre_enter(self):
    """
    TODO
    :param self: It is for handling class structure.
    :return:
    """

    self.ids["txt_student_name"].text = Cache.get("lect",
                                                  "std_name"
                                                  )

    data_detailed_exam = database_api.getExam(Cache.get("info", "token"),
                                              Cache.get("lect", "code"),
                                              Cache.get("lect", "exam")
                                              )["Questions"]

    self.ids["txt_question_no"].text = "Question ID: " + str(data_detailed_exam.values()[0]["ID"])

    self.ids["txt_question_body"].text = "Question:\n" + data_detailed_exam[data_detailed_exam.keys()[0]]["text"]

    self.ids["txt_answer_body"].text = "Answer:\n" + data_detailed_exam[data_detailed_exam.keys()[0]]["answer"]

    data_student_answer = database_api.getAnswersOfStudent(Cache.get("info", "token"),
                                                           Cache.get("lect", "code"),
                                                           Cache.get("lect", "exam"),
                                                           Cache.get("lect", "std_id")
                                                           )

    self.ids["txt_answer_student"].text = "Student's Answer:\n" + data_student_answer[0][3]

    self.ids["txt_answer_summary"].text = "Summary:\n"
