from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

from pg import pgLogin, pgLecturer, tabStart, tabProfile, tabLects, tabStats

class Tab_Stats(Screen):
    pass

class Tab_Lects(Screen):
    def on_pre_enter(self, *args):
        tabLects.on_pre_enter(self)

class Tab_Profile(Screen):
    def on_pre_enter(self, *args):
        tabProfile.on_pre_enter(self)

    def on_change(self):
        tabProfile.on_change(self)

class Tab_Start(Screen):
    def on_faq(self, no):
        tabStart.faq(self, no)

    def on_follow(self, on):
        tabStart.follow(on)

class PgLecturer(Screen):
    pgLogin.load_string("lecturer")

    def on_pre_enter(self, *args):
        pgLecturer.on_pre_enter(self)

    def on_enter(self, *args):
        pgLogin.on_enter(self)

    def on_logout(self):
        pgLecturer.on_logout(pages, screen)

    def on_quit(self):
        pgLogin.on_quit()

    def on_check_connection(self):
        pgLogin.on_check_connection(self)

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
            pgLogin.on_login(self, pages, screen)
        return True

    def on_enter(self, *args):
        pgLogin.on_enter(self)

    def on_login(self):
        #pages.append(PgLecturer(name="PgLecturer"))
        pgLogin.on_login(self, pages, screen)

    def on_quit(self):
        pgLogin.on_quit()

    def on_check_connection(self):
        pgLogin.on_check_connection(self)

class PgSplash(Screen):
    with open("css/splash.seas", "r") as design:
        Builder.load_string(design.read())

    def skip(self, dt):
        screen.switch_to(pages[1])

    def on_enter(self, *args):
        Clock.schedule_once(self.skip, 1)

        anim_fade = Animation(opacity=1, duration=0.5) + Animation(opacity=0, duration=0.5)
        anim_fade.start(self.ids["img_wivern"])

'''
    SMART EXAM ADMINISTRATION SYSTEM
    --- -- --- -- --- -- --- -- ---
    PAGE DESIGNS & RELATED FUNCTIONS    => ABOVE
    APP AND GENERAL SETTINGS            => BELOW
'''

pages = [PgSplash(name="PgSplash"),
         PgLogin(name="PgLogin"),
         PgLecturer(name="PgLecturer")]

screen = ScreenManager(transition=FadeTransition())
screen.add_widget(PgSplash(name="PgSplash"))

class SeasApp(App):
    def build(self):
        screen.current = "PgSplash"
        return screen

if __name__ == "__main__":
    Window.fullscreen = "auto"
    SeasApp().run()