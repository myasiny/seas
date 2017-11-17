from kivy.lang import Builder

def design():
    with open("design/login.txt", "r") as pgLogin:
        Builder.load_string(pgLogin.read())

def login():
    # TODO: Add Login Stuff
    pass