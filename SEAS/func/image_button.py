from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

'''
    This is to create image button by given images along with size and position information
'''

class IconButton(ButtonBehavior, Image):
    def __init__(self, img_path, img_path_pressed, size, pos, **kwargs):
        super(IconButton, self).__init__(**kwargs)
        self.img_path = img_path
        self.img_path_pressed = img_path_pressed
        self.source = self.img_path
        self.size_hint = size
        self.pos_hint = pos

    def on_press(self):
        self.source = self.img_path_pressed

    def on_release(self):
        self.source = self.img_path

'''
    This method creates image button for given functionality and adds to given position with given size
'''

def add_button(self, img, img_press, size, pos, on_do):
    btn = IconButton(img, img_press, size, pos)
    btn.bind(on_release=on_do)
    self.add_widget(btn)