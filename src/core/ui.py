class UI:

    _instance = None
    def __new__(class_, *args, **kwargs):
        if UI._instance != None:
            return UI._instance
        UI._instance = object.__new__(class_, *args, **kwargs)
        UI._instance.init()
        return UI._instance

    def init(self):
        self.elements = []
        self.has_update = 1

    def add_element(self,element):
        if element in self.elements:
            return 0
        self.elements += [element]
        self.has_update = 1
        return 1

    def remove_element(self,element):
        if element not in self.elements:
            return 0
        self.elements.remove(element)
        self.has_update = 1
        return 1

class Element:

    def __init__(self,pos,image):
        self.pos = pos
        self.image = image
