from kivy.logger import Logger
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

import webbrowser
from functools import partial
from SEAS.func.round_image import round_image

'''
    This method rounds user's profile picture and updates top-left image widget accordingly
'''

def on_pre_enter(self):
    round_image()
    self.ids["img_user"].reload()

'''
    This method is to update sign placed next to FAQ button according to its current status such as clicked, closed
'''

def faq_status(sign, dt):
    if sign.text == "+":
        sign.text = "-"
    else:
        sign.text = "+"

'''
    This method creates pop-up with specified design and given content whenever user clicks FAQ button
'''

def on_faq(self, no):
    Logger.info("pgStart: Educator clicked on FAQ button %s" % no)

    faq_status(self.ids["txt_faq_%s_click" % no], None)

    popup_content = FloatLayout()
    popup = Popup(title=self.ids["txt_faq_%s" % no].text,
                  content=popup_content, separator_color=[140/255., 55/255., 95/255., 1.],
                  size_hint=(None, None), size=(self.width / 2, self.height / 2))
    popup_content.add_widget(Image(source="img/widget_75_gray.png", allow_stretch=True, keep_ratio=False,
                                   size=(self.width, self.height), pos_hint={"center_x": .5, "center_y": .5}))
    if no == 1:
        popup_content.add_widget(Label(text="HelloWorld 1", color=(0,0,0,1),
                                       font_name="font/CaviarDreams.ttf", font_size=self.width / 50,
                                       pos_hint={"center_x": .5, "center_y": .5}))
    elif no == 2:
        popup_content.add_widget(Label(text="HelloWorld 2", color=(0,0,0,1),
                                       font_name="font/CaviarDreams.ttf", font_size=self.width / 50,
                                       pos_hint={"center_x": .5, "center_y": .5}))
    elif no == 3:
        popup_content.add_widget(Label(text="HelloWorld 3", color=(0,0,0,1),
                                       font_name="font/CaviarDreams.ttf", font_size=self.width / 50,
                                       pos_hint={"center_x": .5, "center_y": .5}))
    else:
        popup_content.add_widget(Label(text="HelloWorld 4", color=(0,0,0,1),
                                       font_name="font/CaviarDreams.ttf", font_size=self.width / 50,
                                       pos_hint={"center_x": .5, "center_y": .5}))
    popup_content.add_widget(Button(text="Close",
                                    font_name="font/LibelSuit.ttf",
                                    font_size=self.height / 40,
                                    background_normal="img/widget_100.png",
                                    background_down="img/widget_100_selected.png",
                                    size_hint_y=None, height=self.height / 20,
                                    pos_hint={"center_x": .5, "y": .0},
                                    on_release=popup.dismiss))
    popup.bind(on_dismiss=partial(faq_status, self.ids["txt_faq_%s_click" % no]))
    popup.open()

'''
    This method opens given website on default local web browser when user clicks
'''

def on_follow(name):
    if name == "twitter":
        webbrowser.open("https://twitter.com/wivernsoft/")
    elif name == "instagram":
        webbrowser.open("https://instagram.com/wivernsoft/")
    elif name == "linkedin":
        webbrowser.open("https://linkedin.com/company/wivernsoft/")

    Logger.info("pgStart: Educator clicked on social media link and directed to %s" % name.title())