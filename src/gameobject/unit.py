from entity import Unit

class GroundUnit(Unit):

    def __init__(self,y,tile):
        Unit.__init__(self,y,tile)
        self.fall_speed = 0

    def move(self,vector):
        if not self.has_footing():
            self.y -= 1
            return 0
        self.fall_speed = 0
        Unit.move(self,vector)
        return 1

    def has_footing(self):
        ground_tile = self.tile.get_entity_below(self)
        if ground_tile.y +1 < self.y:
            return 0
        return 1

class AirUnit(Unit):

    def __init__(self,y,tile):
        Unit.__init__(self,y,tile)

    def move(self,vector):
        Unit.move(self,vector)

class TestUnit(GroundUnit):

    def __init__(self,y,tile):
        GroundUnit.__init__(self,y,tile)
