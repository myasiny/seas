from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.codeinput import CodeInput
from kivy.uix.screenmanager import Screen, ScreenManager
from pygments.lexers.python import PythonLexer

import time, threading, socket, json
from keyboard import on_press

data = {}
data_keystroke = []

class MainPage(Screen):
    def on_pre_enter(self, *args):
        self.code_input = CodeInput(lexer=PythonLexer(), size_hint=(.5, .9), pos=(25, 25))
        self.add_widget(self.code_input)

        self.start = time.time()
        Clock.schedule_interval(self.get_monitor, 5)

        on_press(self.get_keystroke)

        threading.Thread(target=self.send_data).start()

    def get_monitor(self, dt):
        data[time.time() - self.start] = self.code_input.text

    def get_keystroke(self, event):
        events = ["space", "enter", "tab", "left ctrl", "right ctrl"]
        if event.name in events or len(event.name) == 1:
            data_keystroke.append(event.name)

    def send_data(self):
        def tcp(dt):
            data["keystroke"] = len(data_keystroke)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("localhost", 8888))
            # sock.sendall(pickle.dumps(data).encode("base64"))
            sock.sendall(json.dumps(data))
            sock.close()
        Clock.schedule_interval(tcp, 5)

screen = ScreenManager()
screen.add_widget(MainPage(name="MainPage"))

class MyApp(App):
    Window.title = "CLIENT"
    Window.size = (750, 500)

    def build(self):
        screen.current = "MainPage"
        return screen

MyApp().run()