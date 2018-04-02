from kivy.cache import Cache
from kivy.logger import Logger
from kivy.animation import Animation
from SEAS.grdn.kivycalendar import CalendarWidget
from SEAS.grdn.circulardatetimepicker import CircularTimePicker

from SEAS.func import database_api

'''
    This method updates lecture information, creates calendar and time picker widgets before entering PgNewExam
'''

def on_pre_enter(self):
    temp_selected_lect = open("data/temp_selected_lect.seas", "r")
    self.data_selected_lect = temp_selected_lect.readlines()

    self.ids["txt_lect_code"].text = self.data_selected_lect[0].replace("\n", "")
    self.ids["txt_lect_name"].text = self.data_selected_lect[1]

    self.calendar = CalendarWidget(size_hint=(.3, .3),
                                   pos_hint={"center_x": .525, "y": .15})
    self.add_widget(self.calendar)

    self.time = CircularTimePicker(color=(0.725, 0.463, 0.584, 1),
                                   selector_color=[0.553, 0.216, 0.373, 1],
                                   size_hint=(.25, .25),
                                   pos_hint={"center_x": .825, "center_y": .3})
    self.add_widget(self.time)

    Logger.info("pgNewExam: Calendar and time picker widgets successfully created")

'''
    This method whether exam information is provided or not
    Accordingly, it raises warning or creates exam on local machine
    If required fields are filled, it stores information and directs to PgNewQuestion
    If not, it raises error and process for creating exam fails
'''

def on_new_exam_create(self):
    self.ids["img_wrong_examname"].opacity = 0
    self.ids["img_wrong_duration"].opacity = 0

    day, month, year = self.calendar.active_date
    date = "%04d-%02d-%02d" % (year, month, day)
    time = "%02d:%02d:00" % (self.time.hours, self.time.minutes)

    if self.ids["input_examname"].text != "" and self.ids["input_duration"].text != "":
        with open("data/temp_selected_lect.seas", "w+") as temp_selected_lect:
            temp_selected_lect.write(self.ids["txt_lect_code"].text + "\n" + self.ids["txt_lect_name"].text + "\n" +
                                     "%s\n%s\n%s %s" % (self.ids["input_examname"].text, self.ids["input_duration"].text, date, time))
            temp_selected_lect.close()

        # temp_login = open("data/temp_login.seas", "r")
        # self.data_login = temp_login.readlines()

        database_api.createExam(Cache.get("info", "token"), self.ids["txt_lect_code"].text,
                                self.ids["input_examname"].text, "%s %s" % (date, time),
                                int(self.ids["input_duration"].text))

        Logger.info("pgNewExam: Exam information given, new exam successfully created on local and sent to server")

        return True
    else:
        anim_appear = Animation(opacity=1, duration=1)

        if self.ids["input_examname"].text == "":
            anim_appear.start(self.ids["img_wrong_examname"])
        elif self.ids["input_duration"].text == "":
            anim_appear.start(self.ids["img_wrong_duration"])

        return False