def on_pre_enter(self):
    self.ids["pic_user"].reload()

    temp_login = open("data/temp_login.txt", "r")
    data_login = temp_login.readlines()

    self.ids["txt_username"].text = ((data_login[1].replace("\n", " ")).replace("_", " ")).title() + ((data_login[2].replace("\n", " ")).replace("_", " ")).title()
    self.ids["txt_usermail"].text = data_login[5].replace("\n", " ")
    self.ids["txt_userdept"].text = ((data_login[6].replace("\n", " ")).replace("_", " ")).title()
    self.ids["txt_useruniv"].text = ((data_login[7].replace("\n", " ")).replace("_", " ")).title()
    self.ids["txt_userrole"].text = ((data_login[4].replace("\n", " ")).replace("_", " ")).title()

def on_change(self):
    pass # TODO: Personal Settings