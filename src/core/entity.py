class Entity:

    def __init__(self,y):
        self.height = 30
        self.y = y
        self.offset_height = 0
        self.offset_next_height = 0
        self.stop_draw = 0
        self.solid = 0
        self.draw_priority = 0
        self.image = "link-perfect-small.png"

    def destroy(self):
        pass

    def move_into(self,target):
        return 1

class Block(Entity):

    def __init__(self,y):
        Entity.__init__(self,y)
        self.transparent = 1

    def move_into(self,target):
        return 0

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
        if entity.y == self.y:
            return entity.move_into(self)
        return 0

    def get_fov(self,view_range = 5,tile = None):
        fov = []
        if tile == None:
            tile = self.tile
        view_range -= 1
        if view_range <= 0:
            return fov
        for neighbor in tile.neighbors:
            if neighbor in fov:
                continue
            fov += self.get_fov(view_range,neighbor)
        fov += tile.neighbors
        return fov


class Prop(Entity):

    def __init__(self,y):
        Entity.__init__(self,y)

class Item(Entity):

    def __init__(self,y):
        Entity.__init__(self,y)
        self.draw_priority = -1
        self.image = "res/sprites/items/default.png"
