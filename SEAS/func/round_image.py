'''
    This method imports profile picture from server and rounds it in order to show on top menu and PgProfile
'''

from kivy.logger import Logger

from SEAS.func import database_api
from PIL import Image, ImageOps, ImageDraw

def round_render():
    def render(filename):
        try:
            size = (512, 512)
            mask = Image.new("L", size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + size, fill=255)
            img = Image.open("img/pic_%s.png" % filename)
            output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
            output.putalpha(mask)
            output.save("img/pic_%s.png" % filename)
            output.close()

            Logger.info("round_image: Profile picture successfully rounded on local")
        except:
            Logger.error("round_image: Profile picture couldn't rounded on local")

    try:
        temp_login = open("data/temp_login.seas", "r")
        data_login = temp_login.readlines()

        if database_api.getProfilePic(data_login[8].replace("\n", ""), data_login[0].replace("\n", "")) == "Done":
            Logger.info("round_image: Profile picture successfully imported from server")

            render("current_user")
        else:
            Logger.info("round_image: Profile picture couldn't get imported from server, default one used in case")

            render("user")
    except:
        Logger.error("round_image: Profile picture neither imported from server nor rounded on local")