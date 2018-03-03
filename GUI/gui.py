from kivy.config import Config
Config.set("kivy", "exit_on_escape", "0")
Config.set("input", "mouse", "mouse, multitouch_on_demand")

from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

from pg import pgLogin, tabReset, pgStart, pgProfile, pgLects, pgLiveExam, pgNewExam, pgNewQuestion, pgStats, pgStdStart, pgStdLects, pgStdLiveExam, pgStdStats

class PgStdStats(Screen):
    pgLogin.load_string("stdstats")

    def on_enter(self, *args):
        pgLogin.on_enter(self)

    def on_profile(self):
        pages.append(PgStdProfile(name="PgStdProfile"))
        tabReset.on_back(pages, screen)

    def on_start(self):
        pages.append(PgStdStart(name="PgStdStart"))
        tabReset.on_back(pages, screen)

    def on_lects(self):
        pages.append(PgStdLects(name="PgStdLects"))
        tabReset.on_back(pages, screen)

    def on_logout(self):
        pages.append(PgLogin(name="PgLogin"))
        tabReset.on_back(pages, screen)

    def on_quit(self):
        pgLogin.on_quit(self)

class PgStats(Screen):
    pgLogin.load_string("stats")

    def on_enter(self, *args):
        pgLogin.on_enter(self)

    def on_profile(self):
        pages.append(PgProfile(name="PgProfile"))
        tabReset.on_back(pages, screen)

    def on_start(self):
        pages.append(PgStart(name="PgStart"))
        tabReset.on_back(pages, screen)

    def on_lects(self):
        pages.append(PgLects(name="PgLects"))
        tabReset.on_back(pages, screen)

    def on_logout(self):
        pages.append(PgLogin(name="PgLogin"))
        tabReset.on_back(pages, screen)

    def on_quit(self):
        pgLogin.on_quit(self)

class PgStdLiveExam(Screen):
    pgLogin.load_string("stdliveexam")

    def on_pre_enter(self, *args):
        pgStdLiveExam.on_pre_enter(self)

    def on_run(self):
        pgStdLiveExam.on_run(self)

class PgStdLects(Screen):
    pgLogin.load_string("stdlects")

    def on_pre_enter(self, *args):
        pgStdLects.on_pre_enter(self)

    def on_enter(self, *args):
        pgLogin.on_enter(self)

    def on_profile(self):
        pages.append(PgStdProfile(name="PgStdProfile"))
        tabReset.on_back(pages, screen)

    def on_start(self):
        pages.append(PgStdStart(name="PgStdStart"))
        tabReset.on_back(pages, screen)

    def on_stats(self):
        pages.append(PgStdStats(name="PgStdStats"))
        tabReset.on_back(pages, screen)

    def on_exam_selected(self, dt):
        pgStdLects.on_exam_selected(self)

    def on_join_exam(self):
        pages.append(PgStdLiveExam(name="PgStdLiveExam"))
        tabReset.on_back(pages, screen)

    def on_logout(self):
        pages.append(PgLogin(name="PgLogin"))
        tabReset.on_back(pages, screen)

    def on_quit(self):
        pgLogin.on_quit(self)

class PgStdProfile(Screen):
    pgLogin.load_string("stdprofile")

    def on_pre_enter(self, *args):
        pgProfile.on_pre_enter(self)

    def on_enter(self, *args):
        pgLogin.on_enter(self)

    def on_start(self):
        pages.append(PgStdStart(name="PgStdStart"))
        tabReset.on_back(pages, screen)

    def on_lects(self):
        pages.append(PgStdLects(name="PgStdLects"))
        tabReset.on_back(pages, screen)

    def on_stats(self):
        pages.append(PgStdStats(name="PgStdStats"))
        tabReset.on_back(pages, screen)

    def on_text_change(self, name):
        pgProfile.on_text_change(self, name)

    def on_submit(self):
        pgProfile.on_submit(self)

    def on_logout(self):
        pages.append(PgLogin(name="PgLogin"))
        tabReset.on_back(pages, screen)

    def on_quit(self):
        pgLogin.on_quit(self)

class PgStdStart(Screen):
    pgLogin.load_string("stdstart")

    def on_pre_enter(self, *args):
        pgStart.on_pre_enter(self)

    def on_enter(self, *args):
        pgLogin.on_enter(self)

    def on_profile(self):
        pages.append(PgStdProfile(name="PgStdProfile"))
        tabReset.on_back(pages, screen)

    def on_lects(self):
        pages.append(PgStdLects(name="PgStdLects"))
        tabReset.on_back(pages, screen)

    def on_stats(self):
        pages.append(PgStdStats(name="PgStdStats"))
        tabReset.on_back(pages, screen)

    def on_faq(self, no):
        pgStdStart.on_faq(self, no)

    def on_follow(self, name):
        pgStart.on_follow(name)

    def on_logout(self):
        pages.append(PgLogin(name="PgLogin"))
        tabReset.on_back(pages, screen)

    def on_quit(self):
        pgLogin.on_quit(self)

class PgNewQuestion(Screen):
    pgLogin.load_string("newquestion")

    def on_pre_enter(self, *args):
        pgNewQuestion.on_pre_enter(self)

    def on_new_question_next(self):
        pgNewQuestion.on_new_question_next(self)

    def on_new_question_previous(self):
        pgNewQuestion.on_new_question_previous(self)

    def on_new_question_cancel(self):
        pages.append(PgLects(name="PgLects"))
        tabReset.on_back(pages, screen)

    def on_new_question_complete(self):
        pgNewQuestion.on_new_question_complete(self)

class PgNewExam(Screen):
    pgLogin.load_string("newexam")

    def on_pre_enter(self, *args):
        pgNewExam.on_pre_enter(self)

    def on_enter(self, *args):
        pgLogin.on_enter(self)

    def on_profile(self):
        pages.append(PgProfile(name="PgProfile"))
        tabReset.on_back(pages, screen)

    def on_start(self):
        pages.append(PgStart(name="PgStart"))
        tabReset.on_back(pages, screen)

    def on_lects(self):
        pages.append(PgLects(name="PgLects"))
        tabReset.on_back(pages, screen)

    def on_stats(self):
        pages.append(PgStats(name="PgStats"))
        tabReset.on_back(pages, screen)

    def on_new_exam_cancel(self):
        pages.append(PgLects(name="PgLects"))
        tabReset.on_back(pages, screen)

    def on_new_exam_create(self):
        if pgNewExam.on_new_exam_create(self):
            pages.append(PgNewQuestion(name="PgNewQuestion"))
            tabReset.on_back(pages, screen)

    def on_logout(self):
        pages.append(PgLogin(name="PgLogin"))
        tabReset.on_back(pages, screen)

    def on_quit(self):
        pgLogin.on_quit(self)

class PgLiveExam(Screen):
    pgLogin.load_string("liveexam")

    def on_pre_enter(self, *args):
        pgLiveExam.on_pre_enter(self)

    def on_value(self, instance, brightness):
        pgLiveExam.on_value(self, brightness)

    def on_monitor_backward(self):
        pgLiveExam.on_monitor_backward(self)

    def on_monitor_play(self):
        pgLiveExam.on_monitor_play(self)

    def on_monitor_pause(self):
        pgLiveExam.on_monitor_pause(self)

    def on_monitor_forward(self, dt):
        pgLiveExam.on_monitor_forward(self)

    def on_monitor_live(self):
        pgLiveExam.on_monitor_live(self)

    def on_add_time(self):
        pgLiveExam.on_add_time(self)

    def on_finish_exam(self):
        pgLiveExam.on_finish_exam(self)

    def on_participant_selected(self, dt):
        pgLiveExam.on_participant_selected(self)

    def on_lects(self, dt):
        pgLiveExam.on_lects(self)
        pages.append(PgLects(name="PgLects"))
        tabReset.on_back(pages, screen)

class PgLects(Screen):
    pgLogin.load_string("lects")

    def on_pre_enter(self, *args):
        pgLects.on_pre_enter(self)

    def on_enter(self, *args):
        pgLogin.on_enter(self)

    def on_profile(self):
        pages.append(PgProfile(name="PgProfile"))
        tabReset.on_back(pages, screen)

    def on_start(self):
        pages.append(PgStart(name="PgStart"))
        tabReset.on_back(pages, screen)

    def on_stats(self):
        pages.append(PgStats(name="PgStats"))
        tabReset.on_back(pages, screen)

    def on_add_exam(self):
        pages.append(PgNewExam(name="PgNewExam"))
        tabReset.on_back(pages, screen)

    def on_exams(self):
        pgLects.on_exams(self)

    def on_exam_selected(self, dt):
        pgLects.on_exam_selected(self)

    def on_start_exam(self, dt):
        with open("data/temp_selected_lect.seas", "a+") as temp_selected_lect:
            temp_selected_lect.write("\n" + self.ids["txt_info_head"].text)
            temp_selected_lect.close()
        pages.append(PgLiveExam(name="PgLiveExam"))
        tabReset.on_back(pages, screen)

    def on_participants(self):
        pgLects.on_participants(self)

    def on_participant_selected(self, dt):
        pgLects.on_participant_selected(self)

    def on_participant_deleted(self, dt):
        pgLects.on_participant_deleted(self)

    def on_import_list(self, dt):
        pgLects.on_import_list(self)

    def on_import_list_selected(self, widget_name, file_path, mouse_pos):
        pgLects.on_import_list_selected(self, widget_name, file_path, mouse_pos)

    def on_class_statistics(self):
        pgLects.on_class_statistics(self)

    def on_logout(self):
        pages.append(PgLogin(name="PgLogin"))
        tabReset.on_back(pages, screen)

    def on_quit(self):
        pgLogin.on_quit(self)

class PgProfile(Screen):
    pgLogin.load_string("profile")

    def on_pre_enter(self, *args):
        pgProfile.on_pre_enter(self)

    def on_enter(self, *args):
        pgLogin.on_enter(self)

    def on_start(self):
        pages.append(PgStart(name="PgStart"))
        tabReset.on_back(pages, screen)

    def on_lects(self):
        pages.append(PgLects(name="PgLects"))
        tabReset.on_back(pages, screen)

    def on_stats(self):
        pages.append(PgStats(name="PgStats"))
        tabReset.on_back(pages, screen)

    def on_text_change(self, name):
        pgProfile.on_text_change(self, name)

    def on_submit(self):
        pgProfile.on_submit(self)

    def on_logout(self):
        pages.append(PgLogin(name="PgLogin"))
        tabReset.on_back(pages, screen)

    def on_quit(self):
        pgLogin.on_quit(self)

class PgStart(Screen):
    pgLogin.load_string("start")

    def on_pre_enter(self, *args):
        pgStart.on_pre_enter(self)

    def on_enter(self, *args):
        pgLogin.on_enter(self)

    def on_profile(self):
        pages.append(PgProfile(name="PgProfile"))
        tabReset.on_back(pages, screen)

    def on_lects(self):
        pages.append(PgLects(name="PgLects"))
        tabReset.on_back(pages, screen)

    def on_stats(self):
        pages.append(PgStats(name="PgStats"))
        tabReset.on_back(pages, screen)

    def on_faq(self, no):
        pgStart.on_faq(self, no)

    def on_follow(self, name):
        pgStart.on_follow(name)

    def on_logout(self):
        pages.append(PgLogin(name="PgLogin"))
        tabReset.on_back(pages, screen)

    def on_quit(self):
        pgLogin.on_quit(self)

class TabReset(Screen):
    pgLogin.load_string("reset")

    def on_enter(self, *args):
        pgLogin.on_enter(self)

    def on_reset(self):
        tabReset.on_reset(self)

    def on_back(self):
        pages.append(PgLogin(name="PgLogin"))
        tabReset.on_back(pages, screen)

    def on_quit(self):
        pgLogin.on_quit(self)

class PgLogin(Screen):
    pgLogin.load_string("login")

    def __init__(self, **kwargs):
        super(PgLogin, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'enter':
            PgLogin.on_login(self)
        return True

    def on_enter(self, *args):
        pgLogin.on_enter(self)

    def on_login(self):
        pgLogin.on_login(self, pages, screen, PgLects, PgStdLects)

    def on_reset(self):
        pages.append(TabReset(name="TabReset"))
        tabReset.on_back(pages, screen)

    def on_quit(self):
        pgLogin.on_quit(self)

class PgSplash(Screen):
    pgLogin.load_string("splash")

    def skip(self, dt):
        screen.switch_to(pages[1])

    def on_enter(self, *args):
        Clock.schedule_once(self.skip, 2)

        anim_fade = Animation(opacity=1, duration=1) + Animation(opacity=0, duration=1)
        anim_fade.start(self.ids["img_developer_dark"])

pages = [PgSplash(name="PgSplash"),
         PgLogin(name="PgLogin")]

screen = ScreenManager(transition=FadeTransition())
screen.add_widget(PgSplash(name="PgSplash"))

class SeasApp(App):
    icon = "icon.ico"
    title = "Smart Exam Administration System"
    use_kivy_settings = False
    Window.fullscreen = "auto"

    def build(self):
        screen.current = "PgSplash"
        return screen

if __name__ == "__main__":
    SeasApp().run()