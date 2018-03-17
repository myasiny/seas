import sys, os, time, threading
sys.path.append("../..")

class Security(threading.Thread):
    def run(self):
        os.system("python ../Security/onTop.py")

class GUI(threading.Thread):
    def run(self):
        os.system("python ./app.py")

guiThread = GUI()
guiThread.start()

time.sleep(5)

securityThread = Security()
securityThread.start()