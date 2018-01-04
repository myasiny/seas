import barcode

from PIL import Image
from shutil import move
from barcode.writer import ImageWriter

def barcode_png(id):
    try:
        ean = barcode.get_barcode_class("ean13")
        cod = ean(id, writer=ImageWriter())
        png = cod.save("pic_barcode")
        move("pic_barcode.png", "img/pic_barcode.png")
        try:
            pil = Image.open("img/pic_barcode.png")
            rot = pil.rotate(90)
            res = rot.resize((128, 512), Image.LANCZOS)
            res.save("img/pic_barcode.png")
        except:
            print ("SEAS [ERROR]: barcode_png > Try > Except > Barcode Rotating Failed")
    except:
        print ("SEAS [ERROR]: barcode_png > Except > Barcode Creating Failed")