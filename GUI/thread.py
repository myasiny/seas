import sys
sys.path.append("../..")

import os
import time
import threading

class Security(threading.Thread):
    def run(self):
        os.system("python ../Security/onTop.py")

class GUI(threading.Thread):
    def run(self):
        os.system("python ./gui.py")

guiThread = GUI()
guiThread.start()

time.sleep(5)

securityThread = Security()
securityThread.start()