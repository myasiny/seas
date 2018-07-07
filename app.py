#!/user/bin/env

"""
SEAS
====

`SEAS` provides a computer-based examination system. Thus, educators get the opportunity to prevent cheating issues,
save time spent on exam evaluation and access exam data remotely. On the other hand, students benefit from the system
by having a chance to test their codes on programming questions during exams. It also provides statistics and analyses
in order to increase lecture efficiencies.
"""

import os
import platform
import sys
from cryptography.fernet import Fernet

from kivy.animation import Animation
from kivy.app import App
from kivy.cache import Cache
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

from func import database_api
from pg import appLogin, appReset, eduLects, eduProfile, eduExam, eduQuestion, eduLive, eduGrade, stdLects, stdLive, \
    eduEdit

__authors__ = ["Muhammed Yasin Yildirim", "Fatih Cagatay Gulmez", "Ali Emre Oz"]
__credits__ = ["Ali Cakmak"]
__version__ = "1.0.0"
__status__ = "Prototype"

sys.path.append("../")

Config.set("kivy", "exit_on_escape", "0")
Config.set("input", "mouse", "mouse, multitouch_on_demand")
# Config.set("kivy", "log_enable", "1")
# Config.set("kivy", "log_maxfiles", "-1")
# Config.set("kivy", "log_name", "seas_%d-%m-%y_%H-%M-%S.fay")
# Config.set("kivy", "log_dir", os.path.dirname(os.path.abspath(__file__)) + "\\data\\log\\")


class StdStats(Screen):
    pass


class StdLive(Screen):
    """
    @group Design: on_pre_enter
    @group Functionality: on_answer_change, on_submit, on_leave
    """

    appLogin.load_string("std_live")

    def __init__(self, **kw):
        super(StdLive, self).__init__(**kw)
        self.answer = ""
        self.counter = 0

    def on_pre_enter(self, *args):
        stdLive.on_pre_enter(self)

    def on_answer_change(self, txt):
        self.answer = txt

    @staticmethod
    def on_lects():
        pages.append(StdLects(name="StdLects"))
        appReset.on_back(pages,
                         screen
                         )

    def on_submit(self):
        if stdLive.on_submit(self):
            pages.append(StdLive(name="StdLive"))
            appReset.on_back(pages,
                             screen
                             )

    def on_leave(self, *args):
        stdLive.on_leave(self)


class StdProfile(Screen):
    """
    @group Design: on_pre_enter
    @group Functionality: on_enter, on_pic_change, on_text_change, on_submit, on_quit, on_leave
    """

    appLogin.load_string("std_profile")

    def on_pre_enter(self, *args):
        eduLects.load_buttons(self)
        eduProfile.on_pre_enter(self)

    def on_enter(self, *args):
        appLogin.on_enter(self)

    @staticmethod
    def on_profile(dt):
        pages.append(StdProfile(name="StdProfile"))
        appReset.on_back(pages,
                         screen
                         )

    @staticmethod
    def on_lects():
        pages.append(StdLects(name="StdLects"))
        appReset.on_back(pages,
                         screen
                         )

    @staticmethod
    def on_stats():
        pages.append(StdStats(name="StdStats"))
        appReset.on_back(pages,
                         screen
                         )

    def on_pic_change(self, dt):
        eduProfile.on_pic_change(self)

    def on_text_change(self, name):
        eduProfile.on_text_change(self, name)

    def on_submit(self):
        eduProfile.on_submit(self)

    @staticmethod
    def on_logout(dt):
        EduLects.on_logout(dt)

    def on_quit(self, dt):
        appLogin.on_quit(self)

    def on_leave(self, *args):
        appLogin.on_leave(self)


class StdLects(Screen):
    """
    @group Design: on_pre_enter
    @group Functionality: on_enter, on_lect_select, on_exam_join, on_quit, on_leave
    """

    appLogin.load_string("std_lects")

    def on_pre_enter(self, *args):
        eduLects.load_buttons(self)
        eduLects.on_pre_enter(self)

    def on_enter(self, *args):
        appLogin.on_enter(self)

    @staticmethod
    def on_profile(dt):
        pages.append(StdProfile(name="StdProfile"))
        appReset.on_back(pages,
                         screen
                         )

    @staticmethod
    def on_lects():
        pages.append(StdLects(name="StdLects"))
        appReset.on_back(pages,
                         screen
                         )

    @staticmethod
    def on_stats():
        pages.append(StdStats(name="StdStats"))
        appReset.on_back(pages,
                         screen
                         )

    def on_lect_select(self, dt, dropdown, txt):
        stdLects.on_lect_select(self, dropdown, txt)

    def on_exam_join(self):
        if stdLects.on_exam_join(self):
            pages.append(StdLive(name="StdLive"))
            appReset.on_back(pages,
                             screen
                             )

    @staticmethod
    def on_logout(dt):
        EduLects.on_logout(dt)

    def on_quit(self, dt):
        appLogin.on_quit(self)

    def on_leave(self, *args):
        stdLects.on_leave(self)
        appLogin.on_leave(self)


class EduStats(Screen):
    pass


class EduEdit(Screen):
    """
    @group Design: on_pre_enter
    @group Functionality: on_submit
    """

    appLogin.load_string("edu_edit")

    def on_pre_enter(self, *args):
        eduEdit.on_pre_enter(self)

    def on_submit(self):
        if eduEdit.on_submit(self):
            self.on_lects()

    @staticmethod
    def on_lects():
        pages.append(EduLects(name="EduLects"))
        appReset.on_back(pages,
                         screen
                         )


class EduGrade(Screen):
    """
    @group Design: on_pre_enter
    @group Functionality: on_student_change, on_grade_submit
    """

    appLogin.load_string("edu_grade")

    def on_pre_enter(self, *args):
        eduGrade.on_pre_enter(self)

    def on_student_change(self):
        eduGrade.on_exam_grade(self)

    @staticmethod
    def on_grade():
        pages.append(EduGrade(name="EduGrade"))
        appReset.on_back(pages,
                         screen
                         )

    def on_grade_submit(self):
        if eduGrade.on_grade_submit(self):
            self.on_grade()

    @staticmethod
    def on_lects():
        pages.append(EduLects(name="EduLects"))
        appReset.on_back(pages,
                         screen
                         )


class EduLive(Screen):
    """
    @group Design: on_pre_enter
    @group Functionality: on_time_add, on_exam_finish, on_leave
    """

    appLogin.load_string("edu_live")

    def on_pre_enter(self, *args):
        eduLive.on_pre_enter(self)

    @staticmethod
    def on_lects():
        pages.append(EduLects(name="EduLects"))
        appReset.on_back(pages,
                         screen
                         )

    def on_time_add(self):
        eduLive.on_time_add(self)

    def on_exam_finish(self):
        eduLive.on_exam_finish(self)

    def on_leave(self, *args):
        eduLive.on_leave(self)


class EduQuestion(Screen):
    """
    @group Design: on_pre_enter
    @group Functionality: on_submit, on_question_add
    """

    appLogin.load_string("edu_question")

    def on_pre_enter(self, *args):
        eduQuestion.on_pre_enter(self)

    def on_submit(self):
        eduQuestion.on_submit(self)

    def on_question_add(self, command):
        if eduQuestion.on_submit(self):
            if command == "complete":
                self.on_question_cancel()
            else:
                pages.append(EduQuestion(name="EduQuestion"))
                appReset.on_back(pages,
                                 screen
                                 )

    @staticmethod
    def on_question_cancel():
        pages.append(EduLects(name="EduLects"))
        appReset.on_back(pages,
                         screen
                         )


class EduExam(Screen):
    """
    @group Design: on_pre_enter
    @group Functionality: on_enter, on_exam_create, on_quit, on_leave
    """

    appLogin.load_string("edu_exam")

    def on_pre_enter(self, *args):
        eduLects.load_buttons(self)
        eduExam.on_pre_enter(self)

    def on_enter(self, *args):
        appLogin.on_enter(self)

    @staticmethod
    def on_profile(dt):
        pages.append(EduProfile(name="EduProfile"))
        appReset.on_back(pages,
                         screen
                         )

    @staticmethod
    def on_lects():
        pages.append(EduLects(name="EduLects"))
        appReset.on_back(pages,
                         screen
                         )

    @staticmethod
    def on_stats():
        pages.append(EduStats(name="EduStats"))
        appReset.on_back(pages,
                         screen
                         )

    def on_exam_create(self):
        eduExam.on_exam_create(self)

    @staticmethod
    def on_question_add():
        pages.append(EduQuestion(name="EduQuestion"))
        appReset.on_back(pages,
                         screen
                         )

    @staticmethod
    def on_logout(dt):
        EduLects.on_logout(dt)

    def on_quit(self, dt):
        appLogin.on_quit(self)

    def on_leave(self, *args):
        appLogin.on_leave(self)


class EduProfile(Screen):
    """
    @group Design: on_pre_enter
    @group Functionality: on_enter, on_pic_change, on_text_change, on_submit, on_quit, on_leave
    """

    appLogin.load_string("edu_profile")

    def on_pre_enter(self, *args):
        eduLects.load_buttons(self)
        eduProfile.on_pre_enter(self)

    def on_enter(self, *args):
        appLogin.on_enter(self)

    @staticmethod
    def on_profile(dt):
        pages.append(EduProfile(name="EduProfile"))
        appReset.on_back(pages,
                         screen
                         )

    @staticmethod
    def on_lects():
        pages.append(EduLects(name="EduLects"))
        appReset.on_back(pages,
                         screen
                         )

    @staticmethod
    def on_stats():
        pages.append(EduStats(name="EduStats"))
        appReset.on_back(pages,
                         screen
                         )

    def on_pic_change(self, dt):
        eduProfile.on_pic_change(self)

    def on_text_change(self, name):
        eduProfile.on_text_change(self, name)

    def on_submit(self):
        eduProfile.on_submit(self)

    @staticmethod
    def on_logout(dt):
        EduLects.on_logout(dt)

    def on_quit(self, dt):
        appLogin.on_quit(self)

    def on_leave(self, *args):
        appLogin.on_leave(self)


class EduLects(Screen):
    """
    @group Design: on_pre_enter, on_exams, on_participants
    @group Functionality: on_enter, on_lect_select, on_help, on_contact, on_edit, on_grade, on_quit, on_leave
    """

    appLogin.load_string("edu_lects")

    def on_pre_enter(self, *args):
        eduLects.load_buttons(self)
        eduLects.on_pre_enter(self)

    def on_enter(self, *args):
        appLogin.on_enter(self)

    @staticmethod
    def on_profile(dt):
        pages.append(EduProfile(name="EduProfile"))
        appReset.on_back(pages,
                         screen
                         )

    @staticmethod
    def on_lects():
        pages.append(EduLects(name="EduLects"))
        appReset.on_back(pages,
                         screen
                         )

    @staticmethod
    def on_stats():
        pages.append(EduStats(name="EduStats"))
        appReset.on_back(pages,
                         screen
                         )

    def on_lect_select(self, dt, dropdown, txt):
        eduLects.on_lect_select(self, dropdown, txt)

    @staticmethod
    def on_exam_add():
        pages.append(EduExam(name="EduExam"))
        appReset.on_back(pages,
                         screen
                         )

    def on_exams(self):
        eduLects.on_exams(self)

    def on_participants(self):
        eduLects.on_participants(self)

    def on_help(self):
        eduLects.on_help(self)

    def on_contact(self):
        eduLects.on_contact(self)

    def on_edit(self, no, dt):
        self.popup.dismiss()

        Cache.append("lect",
                     "exam",
                     self.ids["txt_info_head"].text
                     )
        Cache.append("lect",
                     "question",
                     no
                     )

        pages.append(EduEdit(name="EduEdit"))
        appReset.on_back(pages,
                         screen
                         )

    @staticmethod
    def on_grade():
        pages.append(EduGrade(name="EduGrade"))
        appReset.on_back(pages,
                         screen
                         )

    @staticmethod
    def on_live():
        pages.append(EduLive(name="EduLive"))
        appReset.on_back(pages,
                         screen
                         )

    @staticmethod
    def on_logout(dt):
        database_api.signOut(Cache.get("info",
                                       "token"
                                       ),
                             Cache.get("info",
                                       "nick"
                                       )
                             )
        pages.append(AppLogin(name="AppLogin"))
        appReset.on_back(pages,
                         screen
                         )

    def on_quit(self, dt):
        appLogin.on_quit(self)

    def on_leave(self, *args):
        appLogin.on_leave(self)


class AppReset(Screen):
    """
    @group Design: on_pre_enter
    @group Functionality: on_enter, on_reset, on_quit, on_leave
    """

    appLogin.load_string("app_reset")

    def on_pre_enter(self, *args):
        appReset.on_pre_enter(self)

    def on_enter(self, *args):
        appLogin.on_enter(self)

    def on_reset(self):
        appReset.on_reset(self)

    @staticmethod
    def on_back(dt):
        pages.append(AppLogin(name="AppLogin"))
        appReset.on_back(pages,
                         screen
                         )

    def on_quit(self, dt):
        appLogin.on_quit(self)

    def on_leave(self, *args):
        appLogin.on_leave(self)


class AppLogin(Screen):
    """
    @group Design: on_pre_enter
    @group Functionality: on_enter, on_login, on_quit, on_leave
    """

    appLogin.load_string("app_login")

    def on_pre_enter(self, *args):
        appLogin.on_pre_enter(self)

    def on_enter(self, *args):
        appLogin.on_enter(self)

    def on_login(self):
        appLogin.on_login(self,
                          pages,
                          screen,
                          EduLects,
                          StdLects
                          )

    @staticmethod
    def on_reset(dt):
        pages.append(AppReset(name="AppReset"))
        appReset.on_back(pages,
                         screen
                         )

    def on_quit(self, dt):
        appLogin.on_quit(self)

    def on_leave(self, *args):
        appLogin.on_leave(self)


class AppSplash(Screen):
    """
    @group Design: on_enter
    @group Functionality: skip
    """

    appLogin.load_string("app_splash")

    @staticmethod
    def skip(dt):
        """
        This method switches current screen to specified one.
        :param dt: It is for handling callback input.
        :return:
        """

        screen.switch_to(pages[1])

    def on_enter(self, *args):
        """
        This method schedules trigger for given callback. Meanwhile, it reveals specified image.
        :param args: It is for handling Kivy.
        :return:
        """

        Clock.schedule_once(self.skip,
                            2
                            )

        anim_fade = Animation(opacity=1, duration=1) + Animation(opacity=0, duration=1)
        anim_fade.start(self.ids["ico_wivern_round"])


pages = [AppSplash(name="AppSplash"),
         AppLogin(name="AppLogin")
         ]

screen = ScreenManager(transition=FadeTransition())
screen.add_widget(pages[0])


class SEASApp(App):
    """
    @group Design: build
    @group Functionality: force
    """

    icon = "icon.ico"
    title = "Smart Exam Administration System"
    use_kivy_settings = False

    Window.fullscreen = "auto"

    @staticmethod
    def force(dt):
        """
        This method keeps window maximized and positioned.
        :param dt: It is for handling callback input.
        :return:
        """

        Window.top = 0
        Window.maximize()
        Window.restore()

    def build(self):
        """
        This method binds given method to cursor event triggered when cursor leaves window and specifies current screen.
        :return: It is screen manager that shows specified page.
        """

        Window.bind(on_cursor_leave=self.force)

        screen.current = "AppSplash"
        return screen


def on_keyboard_event(event):
    """
    This method checks if pressed key is banned or not.
    :param event: It is information held for activated keyboard event.
    :return: It is boolean depending on whether key is banned or not.
    """

    if event.Key.lower() in []:  # God Mode: "lmenu", "lwin", "rwin", "apps", "esc"
        return False
    else:
        return True


if __name__ == "__main__":
    Cache.register("info",
                   limit=10
                   )
    Cache.register("lect",
                   limit=7
                   )
    Cache.register("config",
                   limit=2
                   )

    Cache.append("config",
                 "cipher",
                 Fernet(Fernet.generate_key())
                 )

    if platform.system() == "Windows":
        import pyHook

        hm = pyHook.HookManager()
        hm.KeyDown = on_keyboard_event
        hm.HookKeyboard()

        Cache.append("config",
                     "path",
                     os.path.join(os.path.join(os.environ["USERPROFILE"]),
                                  "Desktop"
                                  )
                     )
    else:
        if platform.system() == "Linux":
            os.system("sh sh/block.sh")

        Cache.append("config",
                     "path",
                     os.path.join(os.path.join(os.path.expanduser("~")),
                                  "Desktop"
                                  )
                     )

    SEASApp().run()
