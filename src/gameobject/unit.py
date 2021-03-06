from entity import Unit
from magiccards import *

class GroundUnit(Unit):

    def __init__(self,y,tile):
        Unit.__init__(self,y,tile)
        self.fall_speed = 0

    def move(self,game_map,vector):
        if not self.has_footing():
            self.y -= 1
            return 0
        self.fall_speed = 0
        Unit.move(self,game_map,vector)
        if not self.has_footing():
            self.y -= 1
            return 0
        return 1

    def has_footing(self):
        ground_tile = self.tile.get_entity_below(self)
        if ground_tile.y +1 < self.y:
            return 0
        return 1

class AirUnit(Unit):

    def __init__(self,y,tile):
        Unit.__init__(self,y,tile)

    def move(self,game_map,vector):
        Unit.move(self,game_map,vector)

    def has_footing(self):
        return 1

class TestUnit(GroundUnit):

    def __init__(self,y,tile):
        GroundUnit.__init__(self,y,tile)
        self.deck.add( Fireball(-1) )
        self.deck.add( SummonChair(-1) )
        self.deck.add( Fireball(-1) )
        self.deck.add( SummonChair(-1) )
        self.deck.add( Fireball(-1) )
        self.deck.add( SummonChair(-1) )
        self.deck.add( Fireball(-1) )
        self.deck.add( SummonChair(-1) )
        self.deck.add( Fireball(-1) )
        self.deck.add( SummonChair(-1) )
        self.deck.add( Fireball(-1) )

class Crosshair(AirUnit):

    def __init__(self,y,tile):
        AirUnit.__init__(self,y,tile)
        self.image = "res/sprites/entities/units/crosshair.png"

    def can_move_to(self,target):
        return 1
