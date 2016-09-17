import time, arcade
from message import JoinableObject
from windowhandler import WindowHandler
from mapgen import SceneGen, WorldGen
from player import *
from unit import *
from scene import *
from world import *
import time
from utilities import *

class Game(JoinableObject):

    def __init__(self,queues,defaults):
        Camera.initialize()
        JoinableObject.__init__(self,queues)
        self.mapgen_process = self.start_child_process(WorldGen)
        self.run(WorldGen.generate, {})
        self.wait_join()

    def update(self):
        self.join()
        self.run(WindowHandler.move_camera, Camera.get_object())
        self.run(WindowHandler.add_sprites, self.player.fov)

    def start(self,area):
        test_map = Map(10,10)
        player_unit = TestUnit(10,test_map.grid[-1])
        test_map.grid[-1].add_entity(GroundBlock(9))
        self.player = Player(player_unit, test_map)
        self.player.fov = self.player.controllable_entity.get_fov()
        self.map_sprite_list = test_map.grid
        self.player.set_camera()

        test_map.raycast(test_map.grid[50], test_map.grid[87])
        while 1:
            for tile in self.player.fov:
                tile.changed = 0
            self.update()
            time.sleep(1/40)

    def key_press(self,data):
        self.player.key_press(data)

    def key_release(self,data):
        self.player.key_release(data)

class Test:

    def __init__(self):
        self.x = 10
        self.y = 50
