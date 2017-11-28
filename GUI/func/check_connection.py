import socket

def check_connection(img, dt):
    connected = False
    try:
        socket.create_connection((socket.gethostbyname("www.google.com"), 80), 2)
        connected = True
    except:
        pass
    finally:
        if connected:
            img.source = "img/ico_connection_success.png"
        else:
            img.source = "img/ico_connection_fail.png"
        img.reload()