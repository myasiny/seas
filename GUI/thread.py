import threading
import os
import time
import sys
sys.path.append("../..")
class Security(threading.Thread):
    def run(self):
        os.system("python ../Security/onTop.py")
    pass

class GUI(threading.Thread):
    def run(self):
        os.system("python ./gui.py")
    pass

guiThread = GUI()
guiThread.start()
time.sleep(5)
securityThread = Security()
securityThread.start()