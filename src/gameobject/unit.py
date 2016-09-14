from entity import Unit

class GroundUnit(Unit):

    def __init__(self,tile):
        Unit.__init__(self,tile)

    def move(self,vector):
        current_y = self.tile.entities.index(self)
        target = self.tile.get_neighbor(vector)
        if not target:
            return 0
        if not self.can_move_to(target,current_y):
            return 0
        self.tile.entities.remove(self)
        target.entities += [self]
        self.tile = target
        return 1

    def can_move_to(self,target,current_y):
        entity = target.get_entity_at(current_y)
        if entity == None:
            return 1
        if entity.walkable == 1:
            return 1
        return 0

class AirUnit(Unit):
    pass

class TestUnit(GroundUnit):

    def __init__(self,tile):
        GroundUnit.__init__(self,tile)
