from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

import webbrowser
from functools import partial

def faq_status(sign, dt):
    if sign.text == "+":
        sign.text = "-"
    else:
        sign.text = "+"

def faq(self, no):
    faq_status(self.ids["bg_faq_%s_click" % no], None)

    popup_content = GridLayout(cols=1)
    popup = Popup(title=self.ids["txt_faq_%s" % no].text,
                  content=popup_content, separator_color=[211/255.,211/255.,211/255.,1.],
                  size_hint=(None, None), size=(self.width/2, self.height/2))
    if no == 1:
        popup_content.add_widget(Label(text="Hello World 1", font_name="font/LibelSuit.ttf", font_size=self.width/50))
    elif no == 2:
        popup_content.add_widget(Label(text="Hello World 2", font_name="font/LibelSuit.ttf", font_size=self.width/50))
    elif no == 3:
        popup_content.add_widget(Label(text="Hello World 3", font_name="font/LibelSuit.ttf", font_size=self.width/50))
    else:
        popup_content.add_widget(Label(text="Hello World 4", font_name="font/LibelSuit.ttf", font_size=self.width/50))
    popup_content.add_widget(Button(text="Close",
                                    font_name="font/LibelSuit.ttf",
                                    font_size=self.width/100,
                                    background_normal="img/bg_box_small.png",
                                    background_down="img/bg_box_small_popup.png",
                                    size_hint_y=None, height=self.height/20,
                                    on_release=popup.dismiss))
    popup.bind(on_dismiss=partial(faq_status, self.ids["bg_faq_%s_click" % no]))
    popup.open()

def follow(on):
    if on == "twitter":
        webbrowser.open("https://twitter.com/wivernsoft/")
    elif on == "instagram":
        webbrowser.open("https://instagram.com/wivernsoft/")
    elif on == "linkedin":
        webbrowser.open("https://linkedin.com/company/11379247/")