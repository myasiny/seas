from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.logger import Logger
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
import pyHook
from kivy.config import Config
Config.set("kivy", "exit_on_escape", "0")
Config.set("input", "mouse", "mouse, multitouch_on_demand")


class Test(Widget):

    Builder.load_string("""
<Test>:
    Label:
        text: "TEST"
        """)

    def force(self):

        Window.top = 0
        Window.maximize()

    Window.bind(on_cursor_leave=force)

class CoolApp(App):
    title = 'Basic Application'

    def build(self):
        return Test()

def OnKeyboardEvent(event):
    if event.Key.lower() in ["lwin", "lmenu", "rmenu"]:
        return False
    else:
        return True


hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()

if __name__ == "__main__":
    Window.fullscreen = "auto"
    CoolApp().run()