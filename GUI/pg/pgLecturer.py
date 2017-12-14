from GUI.func.round_image import round_image

def on_logout(pages, screen):
    screen.current = pages[1].name
    #del pages[2]

def on_pre_enter(self):
    round_image()
    self.ids["pic_user"].reload()

    temp_login = open("data/temp_login.seas", "r")
    data_login = temp_login.readlines()

    self.ids["txt_username"].text = ((data_login[1].replace("\n", " ")).replace("_", " ")).title() + ((data_login[2].replace("\n", " ")).replace("_", " ")).title()