class Entity:

    def __init__(self):
        pass

    def destroy(self):
        pass

class Block(Entity):

    def __init__(self):
        Entity.__init__(self)
        self.height = 15

class Unit(Entity):

    def __init__(self):
        Entity.__init__(self)

class Prop(Entity):

    def __init__(self):
        Entity.__init__(self)

class Item(Entity):

    def __init__(self):
        Entity.__init__(self)
