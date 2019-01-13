import pythoncom
import pyHook





def OnKeyboardEvent(event):
    print "key: " + event.Key
    return True


hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()

try:
    pythoncom.PumpMessages()
except KeyboardInterrupt():
    pass
