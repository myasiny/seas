"""
text_button
============

`text_button` provides text button with transparent background by using given parameters such as size, position etc.
"""

from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior

__author__ = "Muhammed Yasin Yildirim"


class TransparentButton(ButtonBehavior, Label):
    """
    @group Design: prepare
    @group Functionality: on_press, on_release
    """

    def __init__(self, text, font, size, pos, **kwargs):
        """
        This method constructs self parameter.
        :param text: It is text shown on button.
        :param font: It is font of text shown on button.
        :param size: It is size hint of button on x-axis and y-axis.
        :param pos: It is position hint of button on x-axis and y-axis.
        :param kwargs: It is for handling Kivy.
        """

        super(TransparentButton, self).__init__(**kwargs)
        self.text = text
        self.font_name = font
        self.size_hint = size
        self.pos_hint = pos
        self.prepare()

    def prepare(self):
        """
        This method determines color of text shown on button.
        :return:
        """

        self.color = (0, 0, 0, .5)

    def on_press(self):
        """
        This method changes text color when button is clicked.
        :return:
        """

        self.color = (1, 0, 1, .5)

    def on_release(self):
        """
        This method resets text color to default when button is released.
        :return:
        """

        self.color = (0, 0, 0, .5)


def add_button(txt, font, size, pos, do):
    """
    This method creates image button and binds given command to it.
    :param txt: It is text shown on button.
    :param font: It is font of text shown on button.
    :param size: It is size hint of button on x-axis and y-axis.
    :param pos: It is position hint of button on x-axis and y-axis.
    :param do: It is command to do when button is clicked.
    :return: It is text button created by given parameters.
    """

    text_button = TransparentButton(txt,
                                    font,
                                    size,
                                    pos
                                    )
    text_button.bind(on_release=do)
    return text_button
