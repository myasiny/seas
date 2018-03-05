from keyboard import on_press, wait
import time
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.codeinput import CodeInput
from kivy.config import Config
from kivy.clock import Clock
from kivy.extras.highlight import PythonLexer
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
import numpy as np
import threading
import collections
from GUI.grdn.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
key_dict = {}
key_list = []





class MyApp(App):
    def build(self):
        Window.size = (1200, 500)
        flt = FloatLayout()
        self.codeinput = CodeInput(lexer=PythonLexer(), size_hint=(None, None), size=(500, 500), pos=(5, 5))
        self.graph = BoxLayout(size_hint=(.5, .2), pos=(540, 5))
        flt.add_widget(self.codeinput)
        flt.add_widget(self.graph)
        self.id = 0
        Clock.schedule_interval(self.graphmakerscheduled, 5)
        return flt

    def graphmaker(self):
        key_dict[self.id] = len(key_list)
        od = collections.OrderedDict(sorted(key_dict.items()))
        x = od.keys()
        y = od.values()
        z = [0]
        for i in range(1, len(y)):
            z.append((y[i] - y[i - 1]) / 5.0)

        plt.plot(x, z, color='green')
        plt.xlabel('Time (from beginning to now)')
        plt.ylabel('Total Number of Keys Pressed')
        plt.title('Student Activity\nAli Emre Oz - 213950785')
        plt.grid(True)
        self.id += 5
        return plt

    def graphmakerscheduled(self, dt):
        for child in list(self.graph.children):
            self.graph.remove_widget(child)
        graph_widget = FigureCanvasKivyAgg(self.graphmaker().gcf())
        self.graph.add_widget(graph_widget)

def gui():
    MyApp().run()
def KeyPressed(event):
    if len(event.name) == 1 or str(event.name) == "tab"  or str(event.name) == "space" or str(event.name) == "enter":
        key_list.append(event.name)
def wewewe():
    on_press(KeyPressed)
    gui()
    wait()
wewewe()