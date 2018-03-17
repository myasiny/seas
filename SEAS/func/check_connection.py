'''
    This method checks whether communication with server is still alive or not
    Accordingly, it updates the image on pages where connection status is shown (e.g. PgLogin)
'''

from kivy.logger import Logger

from SEAS.func import database_api

def check_connection(img, dt):
    try:
        if database_api.testConnection():
            img.source = "img/ico_connection_success.png"

            Logger.info("check_connection: SEAS successfully connected to server")
        else:
            img.source = "img/ico_connection_fail.png"

            Logger.error("check_connection: SEAS couldn't connect to server")
    except:
        img.source = "img/ico_connection_fail.png"

        Logger.error("check_connection: Server is not reachable")
    finally:
        img.reload()