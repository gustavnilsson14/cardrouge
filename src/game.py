import time, arcade
from message import JoinableObject
from windowhandler import WindowHandler
from mapgen import SceneGen, WorldGen
from player import *
from unit import *
from scene import *
import time

class Game(JoinableObject):

    def __init__(self,queues,defaults):
        JoinableObject.__init__(self,queues)

        self.mapgen_process = self.start_child_process(WorldGen)
        #player_unit = TestUnit((3,3,3))
        self.player = Player()

        test_map = Map(10,10)

        self.map_sprite_list = test_map.grid
        while 1:
            self.update()
            time.sleep(0.01)

    def update(self):
        self.join()
        self.run(WindowHandler.add_sprites, self.map_sprite_list)

    def key_press(self,data):
        self.player.key_press(data)

    def key_release(self,data):
        self.player.key_release(data)

class Test:

    def __init__(self):
        self.x = 10
        self.y = 50
