import code
import sys
from StringIO import StringIO

import os
from keyboard import on_press, wait
import time
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.codeinput import CodeInput
from kivy.clock import Clock
import subprocess32
from kivy.extras.highlight import PythonLexer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import psutil

class MyApp(App):
    def build(self):
        self.file_list = []
        Window.size = (920, 520)
        flt = FloatLayout()
        self.codeinput = CodeInput(lexer=PythonLexer(), size_hint=(None, None), size=(500, 500), pos=(5, 5))
        self.button = Button(size_hint=(None,None),size=(50,20),pos=(510,485),on_press=self.runn)
        self.output = CodeInput(lexer=PythonLexer(),text="OUTPUT",size_hint=(None,None), pos=(510,5),size=(400,250),)
        flt.add_widget(self.codeinput)
        flt.add_widget(self.button)
        flt.add_widget(self.output)
        proc = psutil.Process()
        for i in proc.open_files():
            self.file_list.append(i.path)

        return flt
    def runn(self, button):

        to_compile = open("temp_student_code.py", "w")
        to_compile.write(self.codeinput.text)
        to_compile.close()
        try:
            try:
                temp_output = subprocess32.check_output(["python", "temp_student_code.py"], stderr=subprocess32.STDOUT, timeout=10)
                old_stdout = sys.stdout
                sys.stdout = StringIO()
                redirected_output = sys.stdout
                script = self.codeinput.text
                co = code.compile_command(script, "<stdin>", "exec")
                exec co
                sys.stdout = old_stdout
                temp_output = redirected_output.getvalue()
            except subprocess32.CalledProcessError as e:
                temp_output = e.output.split("\n")[-3][:-1] + "\n" + e.output.split("\n")[-2][:-1]
        except:
            temp_output = "TimeoutError: infinite loop or something"
        file_list_run = []
        file_path = []
        proc = psutil.Process()
        for i in proc.open_files():
            file_list_run.append(i.path)
        for i in list(set(file_list_run) - set(self.file_list)):
            if os.path.splitext(i)[1] != ".ttf":
                file_path.append(os.path.splitext(i))
        if len(file_path) == 0:
            self.output.text = temp_output
        else:
            self.output.text = "Karsim niye kopya cekiyon :("
            print file_path



def gui():
    MyApp().run()
gui()