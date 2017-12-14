from GUI.func.round_image import round_image

def on_logout(pages, screen):
    screen.current = pages[1].name

def on_pre_enter(self):
    round_image()
    self.ids["pic_user"].reload()

    temp_login = open("data/temp_login.txt", "r")
    user_data = temp_login.readlines()

    self.ids["txt_username"].text = user_data[1].replace("\n", " ") + user_data[2].replace("\n", "")