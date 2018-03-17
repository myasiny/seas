'''
    This method imports profile picture from server and rounds it in order to show on top menu and PgProfile
'''

from kivy.logger import Logger

from SEAS.func import database_api
from PIL import Image, ImageOps, ImageDraw

def round_image():
    try:
        temp_login = open("data/temp_login.seas", "r")
        data_login = temp_login.readlines()

        if database_api.getProfilePic(data_login[7].replace("\n", ""), data_login[0].replace("\n", "")) == "Done":
            size = (512, 512)
            mask = Image.new('L', size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + size, fill=255)
            img = Image.open("img/pic_current_user.png")
            output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
            output.putalpha(mask)
            output.save("img/pic_current_user.png")

            Logger.info("round_image: Profile picture successfully imported from server and rounded on local")
        else:
            size = (512, 512)
            mask = Image.new('L', size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + size, fill=255)
            img = Image.open("img/pic_user.png")
            output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
            output.putalpha(mask)
            output.save("img/pic_user.png")

            Logger.warning("round_image: Profile picture couldn't get imported from server, default one rounded in case")
    except:
        Logger.error("round_image: Profile picture neither imported from server nor rounded on local")