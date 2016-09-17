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
        start = self.tile
        open_list = [self.tile]
        closed_list = []
        while len(open_list) != 0:
            current = open_list[0]
            for neighbor in current.neighbors:
                if neighbor in open_list or neighbor in closed_list:
                    continue
                diff = abs(neighbor.pos[0]-start.pos[0])
                diff += abs(neighbor.pos[1]-start.pos[1])
                if diff > view_range:
                    continue
                open_list += [neighbor]
            closed_list += [current]
            open_list.remove(current)
        return closed_list

class Prop(Entity):

    def __init__(self,y):
        Entity.__init__(self,y)

class Item(Entity):

    def __init__(self,y):
        Entity.__init__(self,y)
        self.draw_priority = -1
        self.image = "res/sprites/blocks/grass.png"
