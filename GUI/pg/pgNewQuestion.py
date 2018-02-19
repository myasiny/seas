import sys
sys.path.append("../..")

from functools import partial
from Server import DatabaseAPI

def on_pre_enter(self):
    # self.remove_widget(self.ids["input_answer_a"])

    check_1 = self.ids["check_1"]
    check_1.name = "programming"
    check_1.background_radio_normal = "img/widget_75_black_circle.png"
    check_1.background_radio_down = "img/widget_75_black_circle_selected.png"
    check_1.bind(active=partial(on_type_checked, self))

    check_2 = self.ids["check_2"]
    check_2.name = "short_answer"
    check_2.background_radio_normal = "img/widget_75_black_circle.png"
    check_2.background_radio_down = "img/widget_75_black_circle_selected.png"
    check_2.bind(active=partial(on_type_checked, self))

    check_3 = self.ids["check_3"]
    check_3.name = "multiple_choice"
    check_3.background_radio_normal = "img/widget_75_black_circle.png"
    check_3.background_radio_down = "img/widget_75_black_circle_selected.png"
    check_3.bind(active=partial(on_type_checked, self))

def on_type_checked(checkbox, value, self):
    if checkbox.name == "programming":
        pass
    elif checkbox.name == "short_answer":
        pass
    else:
        pass

def on_new_question_complete(self):
    json = {1: {"type": "TODO",
                "subject": self.ids["input_subject"].text,
                "text": self.ids["input_question_body"].text,
                "answer": self.ids["input_answer"].text,
                "inputs": [[self.ids["input_input"].text]],
                "outputs": [[self.ids["input_output"].text]],
                "value": int(self.ids["input_value"].text),
                "tags": [self.ids["input_tags"].text]}
            }

    temp_selected_lect = open("data/temp_selected_lect.seas", "r")
    data_selected_lect = temp_selected_lect.readlines()

    DatabaseAPI.createExam("http://192.168.43.164:8888", "istanbul sehir university",
                           data_selected_lect[0].replace("\n", ""),
                           data_selected_lect[2].replace("\n", ""),
                           data_selected_lect[4],
                           int(data_selected_lect[3].replace("\n", "")),
                           json)