from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.uix.button import Button
from kivy.clock import Clock
from functools import partial
import time
import collections
from kivy.uix.slider import Slider
from kivy.uix.gridlayout import GridLayout

class MyApp2(App):

    def build(self):

        self.test_dict = {213950785: {0: '', 1516908288.722: u'def myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i\n\nmyFunction(3, 5)', 1516908290.718: u'\n\ndef myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i\n\nmyFunction(3, 5)', 1516908292.717: u'# Den\n\ndef myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i\n\nmyFunction(3, 5)', 1516908294.722: u'# Deneme\n\ndef myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i\n\nmyFunction(3, 5)', 1516908296.722: u'# Deneme\n\ndef myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i\n\nmyFunction(3, 5)', 1516908298.722: u'# Deneme\n\ndef myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i\n\nmyFunction(3, 5)', 1516908300.724: u'# Deneme\n\ndef myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i\n\nmyFunction(3, 5)', 1516908302.719: u'# Deneme\n\ndef myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i\n\nmyFunction(3, 5)', 1516908304.724: u'# Deneme\n\ndef myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i+1\n\nmyFunction(3, 5)', 1516908306.727: u'# Deneme\n\ndef myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i+1\n\nmyFunction(3, 5)', 1516908308.726: u'# Deneme\n\ndef myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i+1\n\nmyFunction(3, 5)', 1516908310.723: u'# Deneme\n\ndef myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i+1\n\nmyFunction(3, 5)', 1516908220.705: u'', 1516908222.708: u'', 1516908224.709: u'for ', 1516908226.707: u'for i in range', 1516908228.709: u'for i in range()', 1516908230.709: u'for i in range(3, 5)', 1516908232.708: u'for i in range(3, 5):\n', 1516908234.71: u'for i in range(3, 5):\n\t', 1516908236.713: u'for i in range(3, 5):\n\t', 1516908238.714: u'for i in range(3, 5):\n\tpr', 1516908240.717: u'for i in range(3, 5):\n\tprint i', 1516908242.723: u'for i in range(3, 5):\n\tprint i', 1516908244.718: u'for i in range(3, 5):\n\tprint i', 1516908246.725: u'\nfor i in range(3, 5):\n\tprint i', 1516908248.723: u'def my\nfor i in range(3, 5):\n\tprint i', 1516908250.726: u'def myFunck\nfor i in range(3, 5):\n\tprint i', 1516908252.721: u'def myFunction(\nfor i in range(3, 5):\n\tprint i', 1516908254.718: u'def myFunction();\nfor i in range(3, 5):\n\tprint i', 1516908256.716: u'def myFunction():\nfor i in range(3, 5):\n\tprint i', 1516908258.721: u'def myFunction():\n\tfor i in range(3, 5):\n\tprint i', 1516908260.721: u'def myFunction():\n\tfor i in range(3, 5):\n\t\tprint i', 1516908262.724: u'def myFunction():\n\tfor i in range(3, 5):\n\t\tprint i', 1516908264.721: u'def myFunction():\n\tfor i in range(input_1, 5):\n\t\tprint i', 1516908266.723: u'def myFunction():\n\tfor i in range(input_1, input):\n\t\tprint i', 1516908268.723: u'def myFunction(i):\n\tfor i in range(input_1, input_2):\n\t\tprint i', 1516908270.719: u'def myFunction(input_1, i):\n\tfor i in range(input_1, input_2):\n\t\tprint i', 1516908272.716: u'def myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i', 1516908274.716: u'def myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i\n\nmy', 1516908276.713: u'def myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i\n\nmyFunction', 1516908278.713: u'def myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i\n\nmyFunction(3,', 1516908280.707: u'def myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i\n\nmyFunction(3, 5)', 1516908282.71: u'def myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i\n\nmyFunction(3, 5)', 1516908284.715: u'def myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i\n\nmyFunction(3, 5)', 1516908286.719: u'def myFunction(input_1, input_2):\n\tfor i in range(input_1, input_2):\n\t\tprint i\n\nmyFunction(3, 5)'}}

        for i, j in self.test_dict.items():
            self.od = collections.OrderedDict(sorted(j.items()))
            aaa = (len(self.od))

        Config.set('graphics', 'width', '510')
        Config.set('graphics', 'height', '560')

        flt = FloatLayout()
        aa = Image(source="aaa.png", allow_stretch=True, keep_ratio=False, size_hint=(None, None),size=(500, 405), pos=(5,105), opacity = 0.5)
        label = Label(size_hint=(None, None), size=(300, 300),text='Ali Emre Oz', pos=(110, 380))
        textt = " "
        self.text_input = Label(halign = "left", text= textt, color= (0,1,0,1),size_hint=(None, None), size=(500, 405), pos=(5, 105))
        self.slider = Slider(min=0, max=aaa-1, pos = (10,20), size_hint=(None, None), size = (500,100), step = 1)
        self.next_button = Button(text=">>>", pos = (40,20), size_hint=(None, None), size = (50,30))
        self.prev_button = Button(text="<<<", pos=(120, 20), size_hint=(None, None), size=(50, 30))
        self.play_button = Button(text="=>", pos=(200, 20), size_hint=(None, None), size=(50, 30))
        self.pause_button = Button(text="II", pos=(280, 20), size_hint=(None, None), size=(50, 30))
        self.stop_button = Button(text="[]", pos=(360, 20), size_hint=(None, None), size=(50, 30))
        flt.add_widget(aa)
        flt.add_widget(self.text_input)
        flt.add_widget(label)
        flt.add_widget(self.slider)
        flt.add_widget(self.next_button)
        flt.add_widget(self.prev_button)
        flt.add_widget(self.play_button)
        flt.add_widget(self.pause_button)
        flt.add_widget(self.stop_button)
        self.slider.bind(value=self.on_value)
        self.next_button.bind(on_press=self.next_value)
        self.prev_button.bind(on_press=self.prev_value)
        self.play_button.bind(on_press=self.play)
        self.pause_button.bind(on_press=self.pause)
        self.stop_button.bind(on_press=self.stopp)
        return flt

    def on_value(self, instance, brightness):
        self.text_input.text = self.od.items()[int(brightness)][1].replace("\t","   ")

    def next_value(self, instance):
        try:
            self.slider.value = self.slider.value + 1
        except:
            self.slider.value = 0

    def prev_value(self, instance):
        try:
            self.slider.value = self.slider.value - 1
        except:
            self.slider.value = 0

    def play(self, instance):
        self.event = Clock.schedule_interval(self.next_value, 0.5)
        self.play_button.disabled = True
        self.pause_button.disabled = False

    def pause(self, instance):
        self.slider.value = self.slider.value
        self.event.cancel()
        self.pause_button.disabled = True
        self.play_button.disabled = False

    def stopp(self, instance):
        self.slider.value = 0
        self.event.cancel()
        self.play_button.disabled = False
        self.pause_button.disabled = True



MyApp2().run()