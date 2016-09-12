from entity import Unit

class GroundUnit(Unit):

    def __init__(self,tile):
        Unit.__init__(self,tile)

    def move(self,vector):
        current_y = self.tile.entities.index(self)
        target = self.tile.get_neighbor(vector)
        if not target:
            return 0
        if len(target.entities) > current_y:
            return 0
        self.tile.entities.remove(self)
        target.entities += [self]
        self.tile = target
        return 1

class AirUnit(Unit):
    pass

class TestUnit(GroundUnit):

    def __init__(self,tile):
        GroundUnit.__init__(self,tile)
