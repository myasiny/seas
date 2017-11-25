from kivy.lang import Builder

def load_string():
    with open("css/educator.seas", "r") as design:
        Builder.load_string(design.read())