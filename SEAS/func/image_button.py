"""
image_button
============

`image_button` turns image into button by using given parameters such as size, position, image, command etc.
"""

from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

__author__ = "Muhammed Yasin Yildirim"


class IconButton(ButtonBehavior, Image):
    """
    @group Design: prepare
    @group Functionality: on_press, on_release
    """

    def __init__(self, img_path, img_path_pressed, size, pos, **kwargs):
        """
        This method constructs self parameter.
        :param img_path: It is path of default image shown on button.
        :param img_path_pressed: It is path of image shown when button is clicked.
        :param size: It is size hint of button on x-axis along with boolean for keeping ratio.
        :param pos: It is position hint of button on x-axis and y-axis.
        :param kwargs: It is for handling Kivy.
        """

        super(IconButton, self).__init__(**kwargs)
        self.img_path = img_path
        self.img_path_pressed = img_path_pressed
        if isinstance(size, tuple):
            self.size_hint = (size[0], size[0])
            self.boolean = size[1]
        else:
            self.size_hint_x = size
            self.boolean = False
        self.pos_hint = pos
        self.prepare()

    def prepare(self):
        """
        This method puts default image onto button and configures it.
        :return:
        """

        self.source = self.img_path
        self.keep_ratio = self.boolean
        self.allow_stretch = True

    def on_press(self):
        """
        This method changes image shown on button when button is clicked.
        :return:
        """

        self.source = self.img_path_pressed

    def on_release(self):
        """
        This method resets image shown on button to default when button is released.
        :return:
        """

        self.source = self.img_path


def add_button(img, img_press, size, pos, do):
    """
    This method creates image button and binds given command to it.
    :param img: It is path of default image shown on button.
    :param img_press: It is path of image shown when button is clicked.
    :param size: It is size hint of button on x-axis.
    :param pos: It is position hint of button on x-axis and y-axis.
    :param do: It is command to do when button is clicked.
    :return: It is image button created by given parameters.
    """

    image_button = IconButton(img,
                              img_press,
                              size,
                              pos
                              )
    image_button.bind(on_release=do)
    return image_button
