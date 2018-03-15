from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

import threading, socket, json

class MainPage(Screen):
    def on_pre_enter(self, *args):
        self.text_input = Label(text="Loading...", size_hint=(.9, .9), pos=(25, 25))
        self.add_widget(self.text_input)

        server = threading.Thread(target=self.receive_data)
        server.daemon = True
        server.start()

    def receive_data(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("0.0.0.0", 8888))
        sock.listen(1)
        while 1:
            conn, addr = sock.accept()
            # data = pickle.loads(conn.recv(1024).decode("base64"))
            data = json.loads(conn.recv(1024))
            if data:
                try:
                    self.text_input.text = data[sorted(data.keys())[-4]]
                except:
                    self.text_input.text = data[sorted(data.keys())[-2]]

screen = ScreenManager()
screen.add_widget(MainPage(name="MainPage"))

class MyApp(App):
    Window.title = "SERVER"
    Window.size = (750, 500)

    def build(self):
        screen.current = "MainPage"
        return screen

if __name__ == "__main__":
    MyApp().run()