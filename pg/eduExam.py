"""
eduExam
=======

`eduExam` is a toolbox for main app, it contains necessary methods that EduExam page requires.
"""

from kivy.animation import Animation
from kivy.cache import Cache
from kivy.uix.image import Image

from func import database_api
from func.garden.circulardatetimepicker import CircularTimePicker
from func.garden.kivycalendar import CalendarWidget

__author__ = "Muhammed Yasin Yildirim"


def on_pre_enter(self):
    """
    This method creates header images as well as calendar and time picker widgets.
    :param self: It is for handling class structure.
    :return:
    """

    self.ids["txt_lect_code"].text = Cache.get("lect",
                                               "code"
                                               )
    self.ids["txt_lect_name"].text = Cache.get("lect",
                                               "name"
                                               )

    hint = [{"x": .05, "y": .8},
            {"x": .2, "y": .8},
            {"x": .35, "y": .8},
            {"x": .5, "y": .8},
            {"x": .65, "y": .8},
            {"x": .8, "y": .8}
            ]
    for pos in hint:
        self.add_widget(Image(source="data/img/img_header.png",
                              keep_ratio=False,
                              allow_stretch=True,
                              size_hint=(.15, .025),
                              pos_hint=pos
                              )
                        )

    self.calendar = CalendarWidget(size_hint=(.3, .3),
                                   pos_hint={"center_x": .525, "y": .175}
                                   )
    self.add_widget(self.calendar)

    self.time = CircularTimePicker(color=(0.725, 0.463, 0.584, 1),
                                   selector_color=[0.553, 0.216, 0.373, 1],
                                   size_hint=(.25, .25),
                                   pos_hint={"center_x": .825, "center_y": .325}
                                   )
    self.add_widget(self.time)


def on_exam_create(self):
    """
    This method creates new exam with given information through server.
    :param self: It is for handling class structure.
    :return: It is for changing screen to new question page when exam is created.
    """

    ico_status = self.ids["ico_status"]
    ico_status.opacity = 0

    day, month, year = self.calendar.active_date
    date = "%04d-%02d-%02d" % (year, month, day)
    time = "%02d:%02d:00" % (self.time.hours, self.time.minutes)

    if self.ids["input_examname"].text.strip() and self.ids["input_duration"].text.strip():
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
                     self.ids["input_examname"].text
                     )

        database_api.createExam(Cache.get("info", "token"),
                                self.ids["txt_lect_code"].text,
                                self.ids["input_examname"].text,
                                "{d} {t}".format(d=date, t=time),
                                self.ids["input_duration"].text
                                )

        return self.on_question_add()
    else:
        anim_appear = Animation(opacity=1,
                                duration=1
                                )

        if not self.ids["input_examname"].text.strip():
            ico_status.pos_hint = {"x": .275, "center_y": .425}
            anim_appear.start(ico_status)
        elif not self.ids["input_duration"].text.strip():
            ico_status.pos_hint = {"x": .275, "center_y": .225}
            anim_appear.start(ico_status)

        return
