from KivyCalendar import CalendarWidget
from kivy.garden.circulardatetimepicker import CircularTimePicker

def on_pre_enter(self):
    temp_selected_lect = open("data/temp_selected_lect.seas", "r")
    data_selected_lect = temp_selected_lect.readlines()

    self.ids["txt_lect_code"].text = data_selected_lect[0].replace("\n", "")
    self.ids["txt_lect_name"].text = data_selected_lect[1]

    self.add_widget(CalendarWidget(size_hint=(.3, .3),
                                   pos_hint={"center_x": .75, "center_y": .55}))

    self.add_widget(CircularTimePicker(size_hint=(.25, .25),
                                       pos_hint={"center_x": .75, "center_y": .255}))