class Entity:

    def __init__(self):
        self.height = 14
        self.offset_height = 0
        self.offset_next_height = 0
        self.image = "link-perfect-small.png"
        pass

    def destroy(self):
        pass

class Block(Entity):

    def __init__(self):
        Entity.__init__(self)
        self.transparent = 1
        self.walkable = 0


class Unit(Entity):

    def __init__(self,tile):
        Entity.__init__(self)
        self.offset_height = 16
        self.tile = tile
        self.tile.entities += [self]
        self.transparent = 1


class Prop(Entity):

    def __init__(self):
        Entity.__init__(self)

class Item(Entity):

    def __init__(self):
        Entity.__init__(self)
