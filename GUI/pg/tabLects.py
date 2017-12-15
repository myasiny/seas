def on_pre_enter(self):
    temp_lects = open("data/temp_lects.seas", "r")
    data_lects = self.ids["list_lects"].adapter.data

    for lect in temp_lects.readlines():
        data_lects.append(lect.replace("\n", "").title())

def on_detail(self): # TODO: Show details when lecture selected
    txt_hint = self.ids["txt_hint"]
    txt_hint.size_hint_y = None
    txt_hint.height = "0dp"