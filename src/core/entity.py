class Entity:

     def __init__(self,vector):
         self.x = vector[0]
         self.y = vector[1]
         self.z = vector[2]

    def move(self,vector):
        self.x += vector[0]
        self.y += vector[1]
        self.z += vector[2]

class Block(Entity):

    def __init__(self):
        Entity.__init__(self)

class Unit(Entity):

    def __init__(self):
        Entity.__init__(self)

    def move(self, vector):
        self.can_move_to(vector)

    def can_move_to(self,vector):
        return 0

class Prop(Entity):

    def __init__(self):
        Entity.__init__(self)

class Item(Entity):

    def __init__(self):
        Entity.__init__(self)
