"""
eduProfile
==========

`eduProfile` is a toolbox for main app, it contains necessary methods that EduProfile page requires.
"""
from functools import partial

from kivy.animation import Animation
from kivy.cache import Cache
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from func import id_to_qr, database_api, round_image, image_button

__author__ = "Muhammed Yasin Yildirim"


def on_pre_enter(self):
    """
    This method updates identity card widget according to user information.
    :param self: It is for handling class structure.
    :return:
    """

    self.add_widget(image_button.add_button("data/img/ico_picture_change.png",
                                            "data/img/ico_picture_change_select.png",
                                            (.05, True),
                                            {"x": .34, "y": .615},
                                            self.on_pic_change
                                            )
                    )

    self.ids["img_user_card"].source = self.ico_user_picture.source
    self.ids["img_user_card"].reload()

    id_to_qr.generate_qr(Cache.get("info",
                                   "id"
                                   )
                         )

    qrcode = [self.ids["img_qr_1"],
              self.ids["img_qr_2"]
              ]
    for qr in qrcode:
        qr.reload()

    self.ids["txt_username"].text = "{name} {surname}".format(name=Cache.get("info", "name").title(),
                                                              surname=Cache.get("info", "surname").title()
                                                              )
    self.ids["txt_usermail"].text = Cache.get("info",
                                              "mail"
                                              )
    self.ids["txt_useruniv"].text = Cache.get("info",
                                              "uni"
                                              ).replace("_", " ").title()
    if Cache.get("info", "dept") is not None:
        self.ids["txt_userdept"].text = Cache.get("info",
                                                  "dept"
                                                  ).title()

    self.ids["input_new_password"].disabled = True
    self.ids["input_new_mail"].disabled = True


def on_pic_change(s):
    """
    This method creates file chooser pop-up for user to upload profile picture as png file.
    :param s: It is for handling class structure.
    :return:
    """

    def on_pic_select(self, widget_name, file_path, mouse_pos):
        """
        This method uploads selected picture to server and updates related widgets on GUI.
        :param self: It is for handling class structure.
        :param widget_name: It is for handling file chooser input.
        :param file_path: It is path of selected file.
        :param mouse_pos: It is for handling file chooser input.
        :return:
        """

        self.popup.dismiss()

        database_api.uploadProfilePic(Cache.get("info", "token"),
                                      Cache.get("info", "nick"),
                                      file_path[0]
                                      )

        if round_image.update_image():
            Cache.append("info",
                         "pict",
                         True
                         )

            pic = [self.ico_user_picture,
                   self.ids["img_user_card"]
                   ]
            for pp in pic:
                pp.source = "data/img/pic_user_current.png"
                pp.reload()

    popup_content = FloatLayout()
    s.popup = Popup(title="Change Profile Picture",
                    content=popup_content,
                    separator_color=[140 / 255., 55 / 255., 95 / 255., 1.],
                    size_hint=(None, None),
                    size=(s.width / 2, s.height / 2)
                    )
    filechooser = FileChooserIconView(path=Cache.get("config", "path"),
                                      filters=["*.png"],
                                      size=(s.width, s.height),
                                      pos_hint={"center_x": .5, "center_y": .5}
                                      )
    filechooser.bind(on_submit=partial(on_pic_select,
                                       s
                                       )
                     )
    popup_content.add_widget(filechooser)
    popup_content.add_widget(Button(text="Upload",
                                    font_name="data/font/LibelSuit.ttf",
                                    font_size=s.height / 40,
                                    background_normal="data/img/widget_green.png",
                                    background_down="data/img/widget_green_select.png",
                                    size_hint_x=.5,
                                    size_hint_y=None,
                                    height=s.height / 20,
                                    pos_hint={"center_x": .25, "y": .0},
                                    on_release=filechooser.on_submit)  # TODO
                             )
    popup_content.add_widget(Button(text="Cancel",
                                    font_name="data/font/LibelSuit.ttf",
                                    font_size=s.height / 40,
                                    background_normal="data/img/widget_red.png",
                                    background_down="data/img/widget_red_select.png",
                                    size_hint_x=.5,
                                    size_hint_y=None,
                                    height=s.height / 20,
                                    pos_hint={"center_x": .75, "y": .0},
                                    on_release=s.popup.dismiss)
                             )
    s.popup.open()


def on_text_change(self, name):
    """
    This method checks changes made on personal settings widgets and enables or disables them accordingly.
    :param self: It is for handling class structure.
    :param name: It is name of widget where text is changed.
    :return:
    """

    passw_cur = self.ids["input_current_password"]
    passw_new = self.ids["input_new_password"]
    email_new = self.ids["input_new_mail"]

    if name == "current_password":
        if passw_cur.text.strip():
            passw_new.disabled = False
            email_new.disabled = False
        else:
            passw_new.disabled = True
            email_new.disabled = True
    elif name == "new_password":
        if passw_new.text.strip():
            email_new.disabled = True
        else:
            email_new.disabled = False
    elif name == "new_mail":
        if email_new.text.strip():
            passw_new.disabled = True
        else:
            passw_new.disabled = False


def on_submit(self):
    """
    This method changes either password or e-mail of user and redirects to login page accordingly.
    :param self: It is for handling class structure.
    :return:
    """

    ico_status = self.ids["ico_status"]
    ico_status.opacity = 0

    passw_cur = self.ids["input_current_password"]
    passw_new = self.ids["input_new_password"]
    email_new = self.ids["input_new_mail"]

    if not passw_cur.text.strip():
        ico_status.source = "data/img/ico_status_warning.png"
        ico_status.reload()

        anim_appear = Animation(opacity=1,
                                duration=1
                                )
        anim_appear.start(ico_status)
    else:
        if len(passw_new.text) > 0 and passw_new.disabled is False:
            result = database_api.changePassword(Cache.get("info", "token"),
                                                 Cache.get("info", "nick"),
                                                 passw_cur.text,
                                                 passw_new.text,
                                                 isMail=False
                                                 )
            if result == "Password Changed":
                ico_status.source = "data/img/ico_status_success.png"
                ico_status.reload()

                anim_appear = Animation(opacity=1,
                                        duration=1
                                        )
                anim_appear.start(ico_status)

                Clock.schedule_once(self.on_logout, 1)
            else:
                ico_status.source = "data/img/ico_status_fail.png"
                ico_status.reload()

                anim_appear = Animation(opacity=1,
                                        duration=1
                                        )
                anim_appear.start(ico_status)
        elif len(email_new.text) > 0 and email_new.disabled is False:
            result = database_api.changePassword(Cache.get("info", "token"),
                                                 Cache.get("info", "nick"),
                                                 passw_cur.text,
                                                 email_new.text,
                                                 isMail=True
                                                 )
            if result == "Mail Changed":
                ico_status.source = "data/img/ico_status_success.png"
                ico_status.reload()

                anim_appear = Animation(opacity=1,
                                        duration=1
                                        )
                anim_appear.start(ico_status)

                Clock.schedule_once(self.on_logout, 1)
            else:
                ico_status.source = "data/img/ico_status_fail.png"
                ico_status.reload()

                anim_appear = Animation(opacity=1,
                                        duration=1
                                        )
                anim_appear.start(ico_status)
