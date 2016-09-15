class Entity:

    def __init__(self,y):
        self.height = 30
        self.y = y
        self.offset_height = 0
        self.offset_next_height = 0
        self.stop_draw = 0
        self.solid = 0
        self.image = "link-perfect-small.png"
        pass

    def destroy(self):
        pass

class Block(Entity):

    def __init__(self,y):
        Entity.__init__(self,y)
        self.transparent = 1
        self.walkable = 0

class Unit(Entity):

    def __init__(self,y,tile):
        Entity.__init__(self,y)
        self.offset_height = 0
        self.tile = tile
        self.tile.entities += [self]
        self.transparent = 1

    def move(self,vector):
        target = self.tile.get_neighbor(vector)
        if not target:
            return 0
        if not self.can_move_to(target):
            return 0
        self.tile.entities.remove(self)
        target.add_entity(self)
        self.tile = target
        return 1

    def can_move_to(self,target):
        entity = target.get_entity_at(self.y)
        if entity == None:
            return 1
        if entity.y != self.y:
            return 1
        if entity.walkable == 1:
            return 1
        return 0

class Prop(Entity):

    def __init__(self,y):
        Entity.__init__(self,y)

class Item(Entity):

    def __init__(self):
        Entity.__init__(self,y)
