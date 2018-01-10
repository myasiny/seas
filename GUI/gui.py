from kivy.config import Config
Config.set("kivy", "exit_on_escape", "0")
Config.set("input", "mouse", "mouse, multitouch_on_demand")

from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

from pg import pgLogin, tabReset, tabActivate, pgStart, pgProfile, pgLects, pgStats

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
        pgLogin.on_quit()

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

    def on_exams(self):
        pgLects.on_exams(self)

    def on_exam_selected(self, dt):
        pgLects.on_exam_selected(self)

    def on_participants(self):
        pgLects.on_participants(self)

    def on_class_statistics(self):
        pgLects.on_class_statistics(self)

    def on_logout(self):
        pages.append(PgLogin(name="PgLogin"))
        tabReset.on_back(pages, screen)

    def on_quit(self):
        pgLogin.on_quit()

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

    def on_text_change(self, this):
        pgProfile.on_text_change(self, this)

    def on_submit(self):
        pgProfile.on_submit(self)

    def on_logout(self):
        pages.append(PgLogin(name="PgLogin"))
        tabReset.on_back(pages, screen)

    def on_quit(self):
        pgLogin.on_quit()

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

    def on_follow(self, this):
        pgStart.on_follow(this)

    def on_logout(self):
        pages.append(PgLogin(name="PgLogin"))
        tabReset.on_back(pages, screen)

    def on_quit(self):
        pgLogin.on_quit()

class TabActivate(Screen):
    pgLogin.load_string("activate")

    def on_pre_enter(self, *args):
        pgLogin.on_enter(self)

    def on_activate(self):
        tabActivate.on_activate(self)

    def on_back(self):
        pages.append(PgLogin(name="PgLogin"))
        tabReset.on_back(pages, screen)

    def on_quit(self):
        pgLogin.on_quit()

class TabReset(Screen):
    pgLogin.load_string("reset")

    def on_pre_enter(self, *args):
        pgLogin.on_enter(self)

    def on_reset(self):
        tabReset.on_reset(self)

    def on_back(self):
        pages.append(PgLogin(name="PgLogin"))
        tabReset.on_back(pages, screen)

    def on_quit(self):
        pgLogin.on_quit()

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
        pages.append(PgLects(name="PgLects"))
        pgLogin.on_login(self, pages, screen)

    def on_reset(self):
        pages.append(TabReset(name="TabReset"))
        pgLogin.on_reset(pages, screen)

    def on_activate(self):
        pages.append(TabActivate(name="TabActivate"))
        pgLogin.on_activate(pages, screen)

    def on_quit(self):
        pgLogin.on_quit()

class PgSplash(Screen):
    pgLogin.load_string("splash")

    def skip(self, dt):
        screen.switch_to(pages[1])

    def on_enter(self, *args):
        Clock.schedule_once(self.skip, 2)

        anim_fade = Animation(opacity=1, duration=1) + Animation(opacity=0, duration=1)
        anim_fade.start(self.ids["img_developer_dark"])

'''
    SMART EXAM ADMINISTRATION SYSTEM
    --- -- --- -- --- -- --- -- ---
    PAGE DESIGNS & RELATED FUNCTIONS    => ABOVE
    APP AND GENERAL SETTINGS            => BELOW
'''

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