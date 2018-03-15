'''
    This method takes ID as input and converts to barcode. Then, it exports barcode as png
'''

from kivy.logger import Logger

import barcode
from PIL import Image
from shutil import move
from barcode.writer import ImageWriter

def barcode_png(id):
    try:
        ean = barcode.get_barcode_class("ean13")
        cod = ean(str(id), writer=ImageWriter())
        cod.save("pic_barcode")
        move("pic_barcode.png", "img/pic_barcode.png")
        try:
            pil = Image.open("img/pic_barcode.png")
            rot = pil.rotate(90)
            res = rot.resize((128, 512), Image.LANCZOS)
            res.save("img/pic_barcode.png")

            Logger.info("barcode_png: ID successfully saved as pic_barcode.png")
        except:
            Logger.error("barcode_png: Error occurred while rotating pic_barcode.png")
    except:
        Logger.error("barcode_png: Error occurred while converting ID to barcode")