"""
check_live_exam
===============

`check_live_exam` checks if there is live exam happening currently.
"""

from kivy.cache import Cache

from func import database_api

__author__ = "Muhammed Yasin Yildirim"


def is_active(self, dt):
    """
    This method checks status of selected lecture's exams to inform user if any of them is active.
    :param self: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return:
    """

    self.live_exam = None

    self.data_live_exam = database_api.getExamsOfLecture(Cache.get("info", "token"),
                                                         self.ids["txt_lect_code"].text
                                                         )

    for exam in self.data_live_exam:
        if exam[5] == "active":
            self.live_exam = exam[1].replace("_",
                                             " "
                                             )

            self.ids["txt_info_head"].text = self.live_exam.title()

            self.ids["btn_exam_join"].disabled = False
            self.ids["img_exam_join_name"].source = "data/img/img_container_green.png"
            self.ids["txt_exam_join_name"].color = (1, 1, 1, 1)
            self.ids["txt_exam_join_name"].text = "{exam} has started!".format(exam=self.ids["txt_info_head"].text)

            break
        else:
            self.live_exam = None

    if self.live_exam is None:
        self.ids["btn_exam_join"].disabled = True
        self.ids["img_exam_join_name"].source = "data/img/img_container_gray.png"
        self.ids["txt_exam_join_name"].color = (1, 1, 1, .25)
        self.ids["txt_exam_join_name"].text = "No exam started"
