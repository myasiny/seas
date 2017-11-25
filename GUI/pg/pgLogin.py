from kivy.app import App
from kivy.lang import Builder
from kivy.animation import Animation

def load_string():
    with open("css/login.seas", "r") as pgLogin:
        Builder.load_string(pgLogin.read())

def on_quit(self):
    App.get_running_app().stop()

def on_login(self): #TODO: Complete Login Stuff
    img_status = self.ids["img_status"]
    anim_status = Animation(opacity=1, duration=1) + Animation(opacity=0, duration=1)
    anim_status.repeat = True
    anim_status.start(img_status)

    input_username = self.ids["input_username"].text
    input_password = self.ids["input_password"].text
    if input_username == "" or input_password == "":
        pass
    elif input_username == "admin" and input_password == "123":
        pass
    else:
        pass