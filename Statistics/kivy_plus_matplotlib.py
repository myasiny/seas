from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def pie():
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    total = [40,26,20,14]
    title = plt.title('Sample Pie Chart')
    title.set_ha("left")
    plt.gca().axis("equal")
    pie = plt.pie(total, startangle=0, colors=colors)
    labels=["Section 1", "Section 2", "Section 3", "Section 4"]
    plt.legend(pie[0],labels, bbox_to_anchor=(1,0.5), loc="center right", fontsize=10, bbox_transform=plt.gcf().transFigure)
    plt.subplots_adjust(left=0.2, bottom=0, right=0.7)
    return plt

class MyApp(App):
    def build(self):
        box = BoxLayout()
        box.add_widget(FigureCanvasKivyAgg(pie().gcf()))
        return box

MyApp().run()