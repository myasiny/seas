def on_pre_enter(self):
    temp_lects = open("data/temp_lects.seas", "r")
    data_lects = self.ids["list_lects"].adapter.data

    for lect in temp_lects.readlines():
        data_lects.append(lect.replace("\n", "").title())

    #open("data/temp_lects.seas", "w+").close()