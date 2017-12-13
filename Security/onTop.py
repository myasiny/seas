import pyHook
import win32gui
import win32con

def OnKeyboardEvent(event):
    if event.Key.lower() in ["lwin", "escape", "f4", "lmenu", "rmenu"]:
        return False
    else:
        return True

def on():
    try:
        while True:
            hook_manager = pyHook.HookManager()
            hook_manager.KeyDown = OnKeyboardEvent
            hook_manager.HookKeyboard()
            window = win32gui.FindWindow(None, "Seas")
            win32gui.ShowWindow(window, win32con.SW_MAXIMIZE)
            win32gui.SetWindowPos(window, win32con.HWND_TOPMOST, 0, 0, 0, 0, (win32con.SWP_NOMOVE | win32con.SWP_NOSIZE))
    except:
        print ("SEAS [INFO]: onTop > Except > Program Closed")

on()