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
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
key_dict = {}
key_list = []


class MyApp(App):
    def build(self):
        Window.size = (1100,560)
        flt = FloatLayout()
        self.codeinput = CodeInput(lexer=PythonLexer(), size_hint=(None, None), size=(500, 500), pos=(5, 5))
        self.graph = BoxLayout(size_hint=(None, None), size=(400, 400), pos=(550, 10))
        flt.add_widget(self.codeinput)
        flt.add_widget(self.graph)
        self.id = 0
        Clock.schedule_interval(self.graphmakerscheduled, 1)
        return flt

    def graphmaker(self):
        key_dict[self.id] = len(key_list)
        od = collections.OrderedDict(sorted(key_dict.items()))
        x = od.keys()
        y = od.values()
        plt.plot(x,y)
        self.id += 1
        return plt

    def graphmakerscheduled(self, dt):
        for child in list(self.graph.children):
            self.graph.remove_widget(child)
        self.graph.add_widget(FigureCanvasKivyAgg(self.graphmaker().gcf()))


def gui():
    MyApp().run()
def KeyPressed(event):
    key_list.append(event.name)
def wewewe():
    on_press(KeyPressed)
    gui()
    wait()
wewewe()


