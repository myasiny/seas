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

    data_student_answer = database_api.getAnswersOfStudent(Cache.get("info", "token"),
                                                           Cache.get("lect", "code"),
                                                           Cache.get("lect", "exam"),
                                                           Cache.get("lect", "std_id")
                                                           )
