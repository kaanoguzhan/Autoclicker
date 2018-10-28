class Enumeration(object):

    def __init__(self, names):  # or *names, with no .split()
        for number, name in enumerate(names.split()):
            setattr(self, name, number)


fs = Enumeration("Big Small")
gtd = Enumeration("Between Before")

mouse_click = Enumeration("Mouse Click")
keyboard_click = Enumeration("Keyboard Click")
