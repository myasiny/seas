import sys
sys.path.append("../..")

from Server import DatabaseAPI

def on_new_question_complete(self):
    temp_selected_lect = open("data/temp_selected_lect.seas", "r")
    data_selected_lect = temp_selected_lect.readlines()

    json = {1: {"type": "TODO",
                "subject": self.ids["input_subject"].text,
                "text": self.ids["input_question_body"].text,
                "answer": self.ids["input_answer"].text,
                "inputs": [[self.ids["input_input"].text]],
                "outputs": [[self.ids["input_output"].text]],
                "value": int(self.ids["input_value"].text),
                "tags": [self.ids["input_tags"].text]}
            }

    DatabaseAPI.createExam("http://192.168.43.164:8888", "istanbul sehir university",
                           data_selected_lect[0].replace("\n", ""),
                           data_selected_lect[1],
                           "0000-00-00 00:00:00",
                           0,
                           json)