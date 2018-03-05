from kivy.animation import Animation
from GUI.grdn.kivycalendar import CalendarWidget
from GUI.grdn.circulardatetimepicker import CircularTimePicker

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

def on_new_exam_create(self):
    self.ids["img_wrong_examname"].opacity = 0
    self.ids["img_wrong_duration"].opacity = 0

    day, month, year = self.calendar.active_date
    date = "%04d-%02d-%02d" % (year, month, day)
    time = "%02d:%02d:00" % (self.time.hours, self.time.minutes)

    if self.ids["input_examname"].text != "" and self.ids["input_duration"].text != "":
        with open("data/temp_selected_lect.seas", "a+") as temp_selected_lect:
            temp_selected_lect.write("\n%s\n%s\n%s %s" % (self.ids["input_examname"].text, self.ids["input_duration"].text, date, time))
            temp_selected_lect.close()

        return True
    else:
        anim_appear = Animation(opacity=1, duration=1)

        if self.ids["input_examname"].text == "":
            anim_appear.start(self.ids["img_wrong_examname"])
        elif self.ids["input_duration"].text == "":
            anim_appear.start(self.ids["img_wrong_duration"])

        return False