import arcade

class Keys:
    NUM = {
        1:49,
        2:50,
        3:51,
        4:52,
        5:53,
        6:54,
        7:55,
        8:56,
        9:57,
        0:48,
    }

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
        self.listeners = {}
        self.has_update = 1

    def handle_key_press(self,key=None):
        self.has_update = 1
        if self.listeners.get(key) == None:
            return 0
        for listener in self.listeners.get(key):
            obj = listener[0]
            method = listener[1]
            element = listener[2]
            getattr(obj,method)(element)
        return 1

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

    def remove_elements(self):
        while len(self.elements) != 0:
            self.elements.pop()

    def remove_elements_by_entity(self,entity):
        i = 0
        while i < len(self.elements):
            element = self.elements[i]
            if element.entity == entity:
                self.elements.pop(i)
                continue
            i+=1

    def add_listener(self,key,obj,method,element):
        listener = (obj,method,element)
        if self.listeners.get(key) == None:
            self.listeners[key] = [listener]
            return 1
        if listener in self.listeners.get(key):
            return 0
        self.listeners[key] += [listener]
        return 1

    def remove_listeners(self,key):
        print(key)
        if self.listeners.get(key) == None:
            return 0
        del self.listeners[key]
        return 1

    def remove_listener(self,key,obj,method,element=None):
        listener = (obj,method,element)
        if self.listeners.get(key) == None:
            return 0
        if listener not in self.listeners.get(key):
            return 0
        self.listeners[key].remove(listener)
        if len(self.listeners[key]) == 0:
            del self.listeners[key]
        return 1

class Element:

    def __init__(self,pos,image,entity=None):
        self.pos = pos
        self.image = image
        self.text = None
        self.entity = entity

    def add_text(self,text,pos,color=arcade.color.BLACK,font_size=14):
        self.text = Text(text,pos,color,font_size)

class Text:

    def __init__(self,text,pos,color,font_size):
        self.text = text
        self.pos = pos
        self.color = color
        self.font_size = font_size
