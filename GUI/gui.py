from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

from pg import pgLogin, pgLecturer, tabStart

class Tab_Stats(Screen):
    pass

class Tab_Lects(Screen):
    pass

class Tab_Profile(Screen):
    pass

class Tab_Start(Screen):
    def faq(self, no):
        tabStart.faq(self, no)

    def follow(self, on):
        tabStart.follow(on)

class PgLecturer(Screen):
    pgLecturer.load_string()

    def on_quit(self):
        pgLecturer.on_quit()

    def on_enter(self, *args):
        pgLecturer.on_enter(self)

    def on_logout(self):
        pgLecturer.on_logout(pages, screen)

class PgLogin(Screen):
    pgLogin.load_string()

    def on_quit(self):
        pgLogin.on_quit()

    def on_enter(self, *args):
        pgLogin.on_enter(self)

    def on_login(self):
        pgLogin.on_login(self, pages, screen)

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