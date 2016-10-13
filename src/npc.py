from scene import Camera, Map
from unit import *
from controllable import *
from ai_state import *
import random

class Npc(Controllable):
    def __init__(self, game_map):
        Controllable.__init__(self, game_map, StateAI(self))
        self.active = 1
        for i in range(0,10):
            self.add_unit(TestUnit(30,game_map[0]))

    def update(self):
        for entity in self.controllable_entities:
            x = random.randint(-1, 1)
            z = random.randint(-1, 1)
            entity.move(self.game_map, (x,z))
