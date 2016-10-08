class UI:

    _instance = None
    def __new__(class_, *args, **kwargs):
        if UI._instance != None:
            return UI._instance
        UI._instance = object.__new__(class_, *args, **kwargs)
        return UI._instance

    def __init__(self):
        if self == UI._instance:
            return
        self.elements = []

    def add_element(self,element):
        if element in self.elements:
            return 0
        self.elements += [element]
        return 1

    def remove_element(self,element):
        if element in self.elements:
            self.elements.remove(element)
            return 1
        return 0
