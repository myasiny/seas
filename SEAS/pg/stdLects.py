"""
stdLects
========

`stdLects` is a toolbox for main app, it contains necessary methods that StdLects page requires.
"""

from functools import partial

from kivy.adapters.listadapter import ListAdapter
from kivy.cache import Cache
from kivy.clock import Clock
from kivy.uix.listview import ListItemButton

from func import database_api, check_live_exam

__author__ = "Muhammed Yasin Yildirim"


def on_lect_select(self, dropdown, txt):
    """
    This method updates GUI according to selected lecture.
    :param self: It is for handling class structure.
    :param dropdown: It is dropdown menu.
    :param txt: It is lecture code selected on dropdown menu.
    :return:
    """

    try:
        self.check_live_exam.cancel()
    except:
        pass
    finally:
        Clock.schedule_once(partial(check_live_exam.is_active,
                                    self
                                    )
                            )
        self.check_live_exam = Clock.schedule_interval(partial(check_live_exam.is_active,
                                                               self
                                                               ),
                                                       5.0
                                                       )

    dropdown.select(txt)

    self.ids["txt_hint"].opacity = 0

    self.ids["btn_exams"].disabled = False
    self.ids["btn_stats_personal"].disabled = False

    self.ids["txt_lect_code"].opacity = 1
    self.ids["txt_lect_name"].opacity = 1

    for lect in self.data:
        if txt in lect.replace("_", " ").upper():
            self.ids["txt_lect_code"].text = txt
            self.ids["txt_lect_name"].text = " ".join(lect.split("_")[2:]).title()

            Cache.append("lect",
                         "code",
                         txt
                         )
            Cache.append("lect",
                         "name",
                         self.ids["txt_lect_name"].text
                         )

            break

    self.ids["layout_exams"].opacity = 1

    self.data_exams = database_api.getExamsOfLecture(Cache.get("info", "token"),
                                                     self.ids["txt_lect_code"].text
                                                     )

    args_converter = lambda row_index, x: {"text": x.replace("_", " ").title(),
                                           "selected_color": (.843, .82, .82, 1),
                                           "deselected_color": (.57, .67, .68, 1),
                                           "background_down": "data/img/widget_gray_75.png",
                                           "font_name": "data/font/CaviarDreams_Bold.ttf",
                                           "font_size": self.height / 25,
                                           "size_hint_y": None,
                                           "height": self.height / 10
                                           }
    self.ids["list_exams"].adapter = ListAdapter(data=[i[1] for i in self.data_exams],
                                                 cls=ListItemButton,
                                                 args_converter=args_converter,
                                                 allow_empty_selection=False
                                                 )
    self.ids["list_exams"].adapter.bind(on_selection_change=partial(on_exam_select,
                                                                    self
                                                                    )
                                        )


def on_exam_select(self, dt):
    """
    This method updates exam information widget according to selected exam.
    :param self: It is for handling class structure.
    :param dt: It is for handling callback input.
    :return:
    """

    self.ids["img_info_top"].opacity = 0.5
    self.ids["img_info_body"].opacity = 0.5
    self.ids["txt_info_head"].opacity = 1
    try:
        self.ids["txt_info_head"].text = self.ids["list_exams"].adapter.selection[0].text
    except:
        self.ids["txt_info_head"].text = "Information"

    self.ids["txt_date_head"].opacity = 1
    self.ids["txt_date_body"].opacity = 1
    for i in self.data_exams:
        try:
            if i[1].replace("_", " ").title() == self.ids["list_exams"].adapter.selection[0].text:
                self.ids["txt_date_body"].text = i[3].split(" ")[0]
                break
        except:
            if i[1].replace("_", " ").title() == self.ids["txt_info_head"].text:
                self.ids["txt_date_body"].text = i[3].split(" ")[0]
                break

    self.ids["txt_time_head"].opacity = 1
    self.ids["txt_time_body"].opacity = 1
    for i in self.data_exams:
        try:
            if i[1].replace("_", " ").title() == self.ids["list_exams"].adapter.selection[0].text:
                self.ids["txt_time_body"].text = i[3].split(" ")[1]
                break
        except:
            if i[1].replace("_", " ").title() == self.ids["txt_info_head"].text:
                self.ids["txt_time_body"].text = i[3].split(" ")[1]
                break

    self.ids["txt_options_head"].opacity = 1
    self.ids["btn_exam_statistics"].opacity = 1


def on_exam_join(self):
    """
    This method makes necessary preparation before student joins exam.
    :param self: It is for handling class structure.
    :return: It is boolean for completing preparation before switching page.
    """

    with open("data/questions.fay", "w+") as questions:
        questions.close()

    Cache.append("lect",
                 "code",
                 self.ids["txt_lect_code"].text
                 )
    Cache.append("lect",
                 "name",
                 self.ids["txt_lect_name"].text
                 )
    Cache.append("lect",
                 "exam",
                 self.live_exam
                 )

    return True


def on_leave(self):
    """
    This method cancels scheduled method to check live exam when user leaves page.
    :param self: It is for handling class structure.
    :return:
    """

    try:
        self.check_live_exam.cancel()
    except:
        pass
