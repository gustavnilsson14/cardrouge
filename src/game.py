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
        self.player = None
        self.mapgen_process = self.start_child_process(WorldGen)
        self.run(WorldGen.generate, {})
        self.wait_join()

    def update(self):
        self.join()
        self.run(WindowHandler.move_camera, Camera.get_object())
        if self.player.has_update:
            self.run(WindowHandler.add_sprites, self.player.fov)
            self.player.has_update = 0

    def start(self,package):
        test_map = package.get('map')
        d = 0
        start_tile_index = package.get('start_tile_index')
        print("-"*50)
        print(test_map[start_tile_index].entities)
        player_unit = TestUnit(30,test_map[start_tile_index-1])
        player_unit = TestUnit(30,test_map[start_tile_index])
        print(test_map[start_tile_index].entities)
        print("-"*50)
        self.player = Player(player_unit, test_map)
        self.player.fov = self.player.controllable_entity.get_fov(test_map)
        self.map_sprite_list = test_map
        self.player.set_camera()
        self.player.has_update = 1

        #test_map.raycast(test_map.tiles[50], test_map.tiles[87])
        while 1:
            self.update()
            time.sleep(1/60)

    def key_press(self,data):
        if self.player:
            self.player.key_press(data)

    def key_release(self,data):
        if self.player:
            self.player.key_release(data)

class Test:

    def __init__(self):
        self.x = 10
        self.y = 50
