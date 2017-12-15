import sys
sys.path.append("../..")

from Server import DatabaseAPI

def check_connection(img, dt):
    try:
        if DatabaseAPI.testConnection("http://10.50.81.24:8888"):
            img.source = "img/ico_connection_success.png"
        else:
            img.source = "img/ico_connection_fail.png"
            print ("SEAS [ERROR]: check_connection > Try > Server Connection Failed")
    except:
        img.source = "img/ico_connection_fail.png"
        print ("SEAS [ERROR]: check_connection > Except > Server Connection Not Found")
    finally:
        img.reload()