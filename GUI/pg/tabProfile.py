def on_pre_enter(self):
    self.ids["pic_user"].reload()

    temp_data = open("data/temp_data.txt", "r")
    user_data = temp_data.readlines()

    self.ids["txt_username"].text = user_data[1].replace("\n", " ") + user_data[2].replace("\n", "")