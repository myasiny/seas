import sys
sys.path.append("..")

from PIL import Image, ImageOps, ImageDraw

def round_image():
    try:
        size = (128, 128)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        img = Image.open("img/pic_user.png")
        output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        output.save("img/pic_user.png")
    except:
        print ("SEAS [ERROR]: round_image > Except > Program Closed")