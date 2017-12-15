from kivy.animation import Animation

def on_pre_enter(self):
    self.ids["pic_user"].reload()

    temp_login = open("data/temp_login.seas", "r")
    data_login = temp_login.readlines()

    self.ids["txt_username"].text = (data_login[1].replace("\n", " ")).replace("_", " ").title() + (data_login[2].replace("\n", " ")).replace("_", " ").title()
    self.ids["txt_usermail"].text = data_login[5].replace("\n", " ")
    self.ids["txt_userdept"].text = (data_login[6].replace("\n", " ")).replace("_", " ").title()
    self.ids["txt_useruniv"].text = (data_login[7].replace("\n", " ")).replace("_", " ").title()
    self.ids["txt_userrole"].text = (data_login[4].replace("\n", " ")).replace("_", " ").title()

    self.ids["input_new_password"].disabled = True
    self.ids["input_new_mail"].disabled = True

def on_text(self, this):
    if this == "current_password":
        if not self.ids["input_current_password"].text == "":
            self.ids["input_new_password"].disabled = False
            self.ids["input_new_mail"].disabled = False
        else:
            self.ids["input_new_password"].disabled = True
            self.ids["input_new_mail"].disabled = True
    elif this == "new_password":
        if not self.ids["input_new_password"].text == "":
            self.ids["input_new_mail"].disabled = True
        else:
            self.ids["input_new_mail"].disabled = False
    elif this == "new_mail":
        if not self.ids["input_new_mail"].text == "":
            self.ids["input_new_password"].disabled = True
        else:
            self.ids["input_new_password"].disabled = False

def on_change(self): # TODO: Change personal settings
    img_fail = self.ids["img_fail"]
    img_fail.opacity = 0

    input_current_password = self.ids["input_current_password"]
    input_new_password = self.ids["input_new_password"]
    input_new_mail = self.ids["input_new_mail"]

    if input_current_password.text == "":
        anim_appear = Animation(opacity=1, duration=1)
        anim_appear.start(img_fail)
    elif input_new_password.text == "":
        pass
    elif input_new_mail.text == "":
        pass
    else:
        pass