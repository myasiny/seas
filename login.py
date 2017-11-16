from kivy.lang import Builder

def loadString():
    with open("design/login.txt", "r") as pgLogin:
        Builder.load_string(pgLogin.read())