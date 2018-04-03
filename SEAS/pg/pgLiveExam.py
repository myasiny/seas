from kivy.cache import Cache
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.listview import ListItemButton
from kivy.uix.floatlayout import FloatLayout
from kivy.adapters.listadapter import ListAdapter

import collections
import matplotlib.pyplot as plt

import threading, socket, json
from functools import partial
from SEAS.func import database_api
from collections import OrderedDict
from SEAS.func.date_time import date_time, min_timer
from SEAS.grdn.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

'''
    This method updates exam information and imports participants of exam to list on SEAS before entering PgLiveExam
'''

def on_pre_enter(self):
    self.cipher = Cache.get("config", "cipher")

    # temp_login = open("data/temp_login.seas", "r")
    # self.data_login = temp_login.readlines()

    # temp_selected_lect = open("data/temp_selected_lect.seas", "r")
    # self.data_selected_lect = temp_selected_lect.readlines()

    self.data_exam = database_api.getExam(Cache.get("info", "token"),
                                          Cache.get("lect", "code"),
                                          Cache.get("lect", "exam"))

    self.ids["txt_info_head"].text = Cache.get("lect", "code") + " - " + Cache.get("lect", "exam")

    self.duration = int(self.data_exam["Duration"])
    self.ids["txt_duration_clock"].text = str(self.duration)

    self.over = False
    self.date_time = Clock.schedule_interval(partial(date_time, self.ids["txt_clock"]), 1.0)
    self.min_timer = Clock.schedule_interval(partial(min_timer, self.ids["txt_duration_clock"], self), 60.0)

    timestamp = self.data_exam["Time"].split(" ")

    self.ids["txt_info_date"].text = timestamp[1] + " " + timestamp[2] + " " + timestamp[3]

    self.ids["txt_info_time"].text = timestamp[4]

    self.ids["txt_info_duration"].text = "%s mins" % str(self.duration)

    Logger.info("pgLiveExam: Exam information successfully imported from server")

    self.ids["btn_monitor_back"].disabled = True
    self.ids["btn_monitor_play"].disabled = True
    self.ids["btn_monitor_pause"].disabled = True
    self.ids["btn_monitor_forward"].disabled = True
    self.ids["btn_monitor_live"].disabled = True

    self.ids["img_monitor_back"].opacity = 0.25
    self.ids["img_monitor_play"].opacity = 0.25
    self.ids["img_monitor_pause"].opacity = 0.25
    self.ids["img_monitor_forward"].opacity = 0.25
    self.ids["img_monitor_live"].opacity = 0.25

    data = database_api.getCourseStudents(Cache.get("info", "token"), Cache.get("lect", "code"))

    with open("data/temp_student_list.seas", "w+") as temp_student_list:
        std = []
        for d in data:
            std.append(d[0].title() + " " + d[1].title() + " - " + str(d[2]))
        temp_student_list.write(self.cipher.encrypt(str("*[SEAS-NEW-LINE]*".join(std))))
        temp_student_list.close()
    print "bok"
    temp_student_list = open("data/temp_student_list.seas", "r")
    self.data_student_list = self.cipher.decrypt(temp_student_list.read()).split("*[SEAS-NEW-LINE]*")

    args_converter = lambda row_index, i: {"text": i,
                                           "background_normal": "img/widget_75_black_crop.png",
                                           "font_name": "font/CaviarDreams_Bold.ttf", "font_size": self.height / 50,
                                           "size_hint_y": None, "height": self.height / 25}
    self.ids["list_participants"].adapter = ListAdapter(data=[i.replace("\n", "") for i in self.data_student_list],
                                                        cls=ListItemButton, args_converter=args_converter,
                                                        allow_empty_selection=False)
    self.ids["list_participants"].adapter.bind(on_selection_change=self.on_participant_selected)

    Logger.info("pgLiveExam: Participants of exam successfully imported from server")

    # server = threading.Thread(target=self.threaded_server)
    # server.daemon = True
    # server.start()

'''
    This method receives amount of keys pressed and code answer written by students periodically through p2p
'''

# def threaded_server(self):
#     Logger.info("pgLiveExam: Peer-to-peer server successfully started")
#
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.bind(("0.0.0.0", 8888))
#     # sock.listen(1)
#     while 1:
#         conn, addr = sock.accept()
#         data = json.loads(conn.recv(4096))
#         if data:
#             timestamp = OrderedDict(sorted(data.items())).values()[-1]
#             stdanswer = timestamp[0]
#             keystroke = timestamp[1]

'''
    This method creates keystroke graph and monitoring tool whenever educator selects student
'''

def on_participant_selected(self):
    pass
    # TODO
    # def keystroke_graph():
    #     # self.x_time = TODO (p2p)
    #     # self.y_rate = TODO (p2p)
    #     # self.z_tend = TODO (p2p)
    #
    #     for i in range(1, len(self.y_rate)):
    #         self.z_tend.append((self.y_rate[i] - self.y_rate[i - 1]) / 5.0)
    #
    #     plt.plot(self.x_time, self.z_tend, color="green")
    #     plt.xlabel("Time")
    #     plt.ylabel("Keystroke")
    #     plt.grid(True)
    #     plt.axes().set_aspect("equal")
    #     plt.tight_layout()
    #     return plt
    #
    # try:
    #     self.ids["layout_rate"].remove_widget(self.graph_widget)
    # except:
    #     pass
    # finally:
    #     self.graph_widget = FigureCanvasKivyAgg(keystroke_graph().gcf())
    #     self.ids["layout_rate"].add_widget(self.graph_widget)
    #
    # Logger.info("pgLiveExam: Keystroke graph successfully created")
    #
    # # self.answer_dict = TODO (p2p)
    #
    # for i, j in self.answer_dict.items():
    #     self.ordered_answer_dict = collections.OrderedDict(sorted(j.items()))
    # self.ordered_answer_dict_len = len(self.ordered_answer_dict)
    #
    # Logger.info("pgLiveExam: Monitoring tool successfully created")
    #
    # self.ids["slider_monitor"].value_track = True
    # self.ids["slider_monitor"].value_track_color = (0,0,0,1)
    # self.ids["slider_monitor"].min = 0
    # self.ids["slider_monitor"].max = self.ordered_answer_dict_len - 1
    # self.ids["slider_monitor"].bind(value=self.on_value)
    #
    # self.ids["btn_monitor_back"].disabled = False
    # self.ids["btn_monitor_play"].disabled = False
    # self.ids["btn_monitor_pause"].disabled = True
    # self.ids["btn_monitor_forward"].disabled = False
    # self.ids["btn_monitor_live"].disabled = False
    #
    # self.ids["img_monitor_back"].opacity = 1
    # self.ids["img_monitor_play"].opacity = 1
    # self.ids["img_monitor_pause"].opacity = 0.25
    # self.ids["img_monitor_forward"].opacity = 1
    # self.ids["img_monitor_live"].opacity = 1

'''
    This method updates text shown on monitor according to time that educator watches at the moment
'''

def on_value(self, bright):
    pass
    # TODO
    # self.ids["txt_monitor"].text = self.ordered_answer_dict.items()[int(bright)][1].replace("\t", "   ")

'''
    This method is to enable educator rewinding text shown on monitor through button
'''

def on_monitor_backward(self):
    pass
    # TODO
    # if self.ids["slider_monitor"].value - 1 >= 0:
    #     self.ids["slider_monitor"].value -= 1
    # else:
    #     self.ids["slider_monitor"].value = 0

'''
    This method is to enable educator playing text on monitor automatically
'''

def on_monitor_play(self):
    pass
    # TODO
    # self.event = Clock.schedule_interval(self.on_monitor_forward, 0.5)
    #
    # self.ids["btn_monitor_back"].disabled = True
    # self.ids["btn_monitor_play"].disabled = True
    # self.ids["btn_monitor_pause"].disabled = False
    # self.ids["btn_monitor_forward"].disabled = True
    # self.ids["btn_monitor_live"].disabled = True
    #
    # self.ids["img_monitor_back"].opacity = 0.25
    # self.ids["img_monitor_play"].opacity = 0.25
    # self.ids["img_monitor_pause"].opacity = 1
    # self.ids["img_monitor_forward"].opacity = 0.25
    # self.ids["img_monitor_live"].opacity = 0.25

'''
    This method is to enable educator pausing text stream on monitor through button
'''

def on_monitor_pause(self):
    pass
    # TODO
    # self.event.cancel()
    #
    # self.ids["btn_monitor_back"].disabled = False
    # self.ids["btn_monitor_play"].disabled = False
    # self.ids["btn_monitor_pause"].disabled = True
    # self.ids["btn_monitor_forward"].disabled = False
    # self.ids["btn_monitor_live"].disabled = False
    #
    # self.ids["img_monitor_back"].opacity = 1
    # self.ids["img_monitor_play"].opacity = 1
    # self.ids["img_monitor_pause"].opacity = 0.25
    # self.ids["img_monitor_forward"].opacity = 1
    # self.ids["img_monitor_live"].opacity = 1

'''
    This method is to enable educator skipping forward text shown on monitor through button
'''

def on_monitor_forward(self):
    pass
    # TODO
    # try:
    #     self.ids["slider_monitor"].value += 1
    # except:
    #     self.ids["slider_monitor"].value = 0

'''
    This method ...
'''

def on_monitor_live(self):
    pass  # TODO (p2p)

'''
    This method adds 10 minutes to exam duration left and updates it on both SEAS and server
'''

def on_add_time(self):
    self.duration += 10
    database_api.add_time_to_exam(Cache.get("info", "token"),
                                  Cache.get("lect", "code"),
                                  Cache.get("lect", "exam"), 10)
    self.ids["txt_info_duration"].text = "%s mins" % str(self.duration)
    self.ids["txt_duration_clock"].text = str(self.duration)

    Logger.info("pgLiveExam: Educator successfully added 10 more minutes to exam duration")

'''
    This method asks educator to confirm whether he or she wants to finish exam or not
    Accordingly, confirmation pop-up disappears or exam ends and directs to PgLects
'''

def on_finish_exam(self):
    popup_content = FloatLayout()
    self.popup = Popup(content=popup_content, separator_color=[140 / 255., 55 / 255., 95 / 255., 1.],
                       size_hint=(None, None), size=(self.width / 5, self.height / 5))
    popup_content.add_widget(Label(text="Do you want to proceed?", color=(1, 1, 1, 1),
                                   font_name="font/CaviarDreams.ttf", font_size=self.width / 75,
                                   pos_hint={"center_x": .5, "center_y": .625}))
    popup_content.add_widget(Button(text="Yes",
                                    font_name="font/LibelSuit.ttf",
                                    font_size=self.height / 40,
                                    background_normal="img/widget_100_green.png",
                                    background_down="img/widget_100_green_selected.png",
                                    size_hint_x=None, width=self.width / 11,
                                    size_hint_y=None, height=self.height / 25,
                                    pos_hint={"center_x": .25, "y": .01},
                                    on_release=self.on_lects))
    popup_content.add_widget(Button(text="No",
                                    font_name="font/LibelSuit.ttf",
                                    font_size=self.height / 40,
                                    background_normal="img/widget_100_red.png",
                                    background_down="img/widget_100_red_selected.png",
                                    size_hint_x=None, width=self.width / 11,
                                    size_hint_y=None, height=self.height / 25,
                                    pos_hint={"center_x": .75, "y": .01},
                                    on_release=self.popup.dismiss))
    if self.over:
        self.popup.title = "Time Expired"
        self.over = False

        Logger.info("pgLiveExam: Educator informed about exam timed out, waiting for confirmation")
    else:
        self.popup.title = "Finish Exam"

        Logger.info("pgLiveExam: Educator clicked on finish exam, waiting for confirmation")
    self.popup.open()

'''
    This method finishes exam by connecting to server and directs to PgLects
'''

def on_lects(self):
    self.popup.dismiss()

    database_api.change_status_of_exam(Cache.get("info", "token"),
                                       Cache.get("lect", "code"),
                                       Cache.get("lect", "exam"), "finished")

    Logger.info("pgLiveExam: Educator successfully finished exam")

'''
    This method checks clock event scheduled for connection checking and cancels it to avoid too many requests later on
'''

def on_leave(self):
    self.date_time.cancel()
    self.min_timer.cancel()