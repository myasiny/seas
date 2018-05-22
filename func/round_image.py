"""
round_image
===========

`round_image` imports profile picture of user from server and renders it.
"""

from PIL import Image, ImageOps, ImageDraw

from kivy.cache import Cache

from func import database_api

__author__ = "Muhammed Yasin Yildirim"
__credits__ = ["Ali Emre Oz"]


def render_image():
    """
    This method resizes and crops image roundly.
    :return:
    """

    size = (512, 512)
    mask = Image.new("L",
                     size,
                     0
                     )
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size,
                 fill=255
                 )
    img = Image.open("data/img/pic_user_current.png")
    output = ImageOps.fit(img,
                          mask.size,
                          centering=(0.5, 0.5)
                          )
    output.putalpha(mask)
    output.save("data/img/pic_user_current.png")
    output.close()


def update_image():
    """
    This method tries to get profile picture of user from server for rendering.
    :return: It is for declaring that user has profile picture.
    """

    try:
        if database_api.getProfilePic(Cache.get("info", "token"), Cache.get("info", "nick")) == "Done":
            render_image()

            return True
        else:
            return False
    except:
        return False
