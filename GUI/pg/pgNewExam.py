from KivyCalendar import CalendarWidget
from kivy.garden.circulardatetimepicker import CircularTimePicker

def on_pre_enter(self):
    temp_selected_lect = open("data/temp_selected_lect.seas", "r")
    data_selected_lect = temp_selected_lect.readlines()

    self.ids["txt_lect_code"].text = data_selected_lect[0].replace("\n", "")
    self.ids["txt_lect_name"].text = data_selected_lect[1]

    self.calendar = CalendarWidget(size_hint=(.3, .3),
                                   pos_hint={"center_x": .525, "y": .15})
    self.add_widget(self.calendar)

    self.time = CircularTimePicker(color=(1,1,1,1),
                                   selector_color=(0,0,0,0.5),
                                   size_hint=(.25, .25),
                                   pos_hint={"center_x": .825, "center_y": .3})
    self.add_widget(self.time)

def on_new_exam_create(self):
    day, month, year = self.calendar.active_date
    date = "%04d-%02d-%02d" % (year, month, day)
    time = "%02d:%02d:00" % (self.time.hours, self.time.minutes)

    with open("data/temp_selected_lect.seas", "a+") as temp_selected_lect:
        temp_selected_lect.write("\n%s\n%s\n%s %s" % (self.ids["input_examname"].text, self.ids["input_duration"].text, date, time))
        temp_selected_lect.close()