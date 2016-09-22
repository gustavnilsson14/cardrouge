from scene import Camera, Map
from unit import *
from controllable import *
import random

class Npc(Controllable):
    def __init__(self, game_map):
        Controllable.__init__(self, game_map)
        for i in range(0,10):
            self.addUnit(TestUnit(30,game_map[i]))

    def update(self):
        for entity in self.controllable_entities:
            x = random.randint(-1, 1)
            z = random.randint(-1, 1)
            entity.move(self.game_map, (x,z))
