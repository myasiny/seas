from kivy.logger import Logger

import qrcode
from PIL import Image
# import barcode
# from shutil import move
# from barcode.writer import ImageWriter

'''
    This method takes ID as input and converts to barcode. Then, it exports barcode as png
'''

# def barcode_png(id):
#     try:
#         ean = barcode.get_barcode_class("ean13")
#         cod = ean(id, writer=ImageWriter())
#         cod.save("pic_barcode")
#         move("pic_barcode.png", "img/pic_barcode.png")
#         try:
#             pil = Image.open("img/pic_barcode.png")
#             rot = pil.rotate(90)
#             res = rot.resize((128, 512), Image.LANCZOS)
#             res.save("img/pic_barcode.png")
#
#             Logger.info("barcode_png: ID successfully saved as pic_barcode.png")
#         except:
#             Logger.error("barcode_png: Error occurred while rotating pic_barcode.png")
#     except:
#         Logger.error("barcode_png: Error occurred while converting ID to barcode")

'''
    This method takes ID as input and converts to QR code. Then, it exports QR code as png
'''

def barcode_png(id):
    try:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(str(id))
        qr.make(fit=True)
        img = qr.make_image(fill_color="white", back_color="black")
        img.save("img/pic_barcode.png")
        try:
            pil = Image.open("img/pic_barcode.png")
            rot = pil.rotate(90)
            res = rot.resize((128, 512), Image.LANCZOS)
            res.save("img/pic_barcode.png")

            Logger.info("barcode_png: ID successfully saved as pic_barcode.png")
        except:
            Logger.error("barcode_png: Error occurred while rotating pic_barcode.png")
    except:
        Logger.error("barcode_png: Error occurred while converting ID to QR code")