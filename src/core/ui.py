import arcade

class Keys:
    NUM_0 = 48
    NUM_1 = 49
    NUM_2 = 50
    NUM_3 = 51
    NUM_4 = 52
    NUM_5 = 53
    NUM_6 = 54
    NUM_7 = 55
    NUM_8 = 56
    NUM_9 = 57

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
        self.listeners = []
        self.has_update = 1


    def handle_key_press(self,key=None):
        self.has_update = 1
        for listener in self.listeners.get(key):
            obj = listener[0]
            method = listener[1]
            getattr(obj,method)()

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

    def add_listener(self,key,obj,method):
        listener = (obj,method)
        if self.listeners.get(key) == None:
            self.listeners[key] = [listener]
            return 1
        if listener in self.listeners.get(key):
            return 0
        self.listeners[key] += [listener]
        return 1

    def remove_listeners(self,key):
        if self.listeners.get(key) == None:
            return 0
        del self.listeners[key]

    def remove_listener(self,key,obj,method):
        listener = (obj,method)
        if self.listeners.get(key) == None:
            return 0
        if listener not in self.listeners.get(key):
            return 0
        self.listeners[key].remove(listener)
        return 1

class Element:

    def __init__(self,pos,image):
        self.pos = pos
        self.image = image
        self.text = None

    def add_text(self,text,pos,color=arcade.color.BLACK,font_size=14):
        self.text = Text(text,pos,color,font_size)

class Text:

    def __init__(self,text,pos,color,font_size):
        self.text = text
        self.pos = pos
        self.color = color
        self.font_size = font_size
