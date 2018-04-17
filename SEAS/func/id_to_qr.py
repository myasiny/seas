"""
id_to_qr
========

`id_to_qr` creates qr code image from given integer.
"""

import qrcode
from PIL import Image

__author__ = "Muhammed Yasin Yildirim"


def generate_qr(i):
    """
    This method generates qr code from given integer and saves it as png file.
    :param i: It is integer to generate qr code from.
    :return:
    """

    try:
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=10,
                           border=4
                           )
        qr.add_data(str(i))
        qr.make(fit=True)

        img = qr.make_image(fill_color="white",
                            back_color="black"
                            )
        img.save("data/img/img_qr.png")

        try:
            pil = Image.open("data/img/img_qr.png")
            rot = pil.rotate(90)
            res = rot.resize((128, 512),
                             Image.LANCZOS
                             )
            res.save("data/img/img_qr.png")
            res.close()
        except:
            pass
    except:
        pass
