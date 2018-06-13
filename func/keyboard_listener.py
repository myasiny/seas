"""
keyboard_listener
=================

`keyboard_listener` tracks all keys pressed by user and counts them.
"""

from kivy.core.window import Window
from kivy.uix.widget import Widget

__author__ = "Muhammed Yasin Yildirim"
__credits__ = ["Ali Emre Oz"]


class KeyboardListener(Widget):
    """
    @group Functionality: _keyboard_closed, _on_keyboard_down
    """

    def __init__(self, s, **kwargs):
        """
        This method constructs self parameter.
        :param kwargs: It is for handling Kivy.
        """

        super(KeyboardListener, self).__init__(**kwargs)
        self.s = s
        self._keyboard = Window.request_keyboard(self._keyboard_closed,
                                                 self,
                                                 "text"
                                                 )
        if self._keyboard.widget:
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        """
        This method initializes keyboard listener.
        :return:
        """

        pass

    def _on_keyboard_down(self, keyboard, keycode, text, mods):
        """
        This method counts how many keys pressed.
        :param keyboard: It is keyboard that is being listened.
        :param keycode: It is information of key pressed.
        :param text: It is text written.
        :param mods: It is modifiers for key pressed.
        :return: It is boolean for accepting key.
        """

        unnecessary_list = ["rshift",
                            "shift",
                            "alt",
                            "rctrl",
                            "lctrl",
                            "super",
                            "alt-gr",
                            "compose",
                            "pipe",
                            "capslock",
                            "escape",
                            # "spacebar",
                            "pageup",
                            "pagedown",
                            "end",
                            "home",
                            "left",
                            "up",
                            "right",
                            "down",
                            "insert",
                            "delete",
                            "numlock",
                            "print",
                            "screenlock",
                            "pause",
                            "f1",
                            "f2",
                            "f3",
                            "f4",
                            "f5",
                            "f6",
                            "f7",
                            "f8",
                            "f9",
                            "f10",
                            "f11",
                            "f12",
                            "f13",
                            "f14",
                            "f15"
                            ]

        if keycode[1] not in unnecessary_list:
            self.s.counter += 1

        # if keycode[1] == "escape":
        #     keyboard.release()

        return True
