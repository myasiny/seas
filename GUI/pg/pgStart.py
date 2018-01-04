from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

import webbrowser
from functools import partial
from GUI.func.round_image import round_image

def on_pre_enter(self):
    round_image()
    self.ids["img_user"].reload()

def faq_status(sign, dt):
    if sign.text == "+":
        sign.text = "-"
    else:
        sign.text = "+"

def on_faq(self, no):
    faq_status(self.ids["txt_faq_%s_click" % no], None)

    popup_content = GridLayout(cols=1)
    popup = Popup(title=self.ids["txt_faq_%s" % no].text,
                  content=popup_content, separator_color=[140/255., 55/255., 95/255., 1.],
                  size_hint=(None, None), size=(self.width/2, self.height/2))
    if no == 1:
        popup_content.add_widget(Label(text="Hello World 1", font_name="font/CaviarDreams.ttf", font_size=self.width/50))
    elif no == 2:
        popup_content.add_widget(Label(text="Hello World 2", font_name="font/CaviarDreams.ttf", font_size=self.width/50))
    elif no == 3:
        popup_content.add_widget(Label(text="Hello World 3", font_name="font/CaviarDreams.ttf", font_size=self.width/50))
    else:
        popup_content.add_widget(Label(text="Hello World 4", font_name="font/CaviarDreams.ttf", font_size=self.width/50))
    popup_content.add_widget(Button(text="Close",
                                    font_name="font/LibelSuit.ttf",
                                    font_size=self.height/40,
                                    background_normal="img/widget_100.png",
                                    background_down="img/widget_100_selected.png",
                                    size_hint_y=None, height=self.height/20,
                                    on_release=popup.dismiss))
    popup.bind(on_dismiss=partial(faq_status, self.ids["txt_faq_%s_click" % no]))
    popup.open()

def on_follow(this):
    if this == "twitter":
        webbrowser.open("https://twitter.com/wivernsoft/")
    elif this == "instagram":
        webbrowser.open("https://instagram.com/wivernsoft/")
    elif this == "linkedin":
        webbrowser.open("https://linkedin.com/company/11379247/")