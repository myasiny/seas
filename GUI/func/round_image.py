from GUI.func import database_api
from PIL import Image, ImageOps, ImageDraw

def round_image():
    try:
        temp_login = open("data/temp_login.seas", "r")
        data_login = temp_login.readlines()

        database_api.getProfilePic(data_login[7].replace("\n", ""), data_login[0].replace("\n", ""))

        size = (512, 512)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        img = Image.open("img/pic_user.png")
        output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        output.save("img/pic_user.png")
    except:
        print ("SEAS [ERROR]: round_image > Except > Image Shaping Failed")