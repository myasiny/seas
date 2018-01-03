def on_reset(self):
    pass
    #TODO: Reset Password

def on_back(pages, screen):
    try:
        screen.switch_to(pages[2])
    except:
        screen.current = pages[2].name
    del pages[1]