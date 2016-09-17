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
            st = time.time()
            self.run(WindowHandler.add_sprites, self.player.fov)
            print('game WindowHandler.add_sprites took: %s seconds'%(str(time.time()-st),))
            self.player.has_update = 0

    def start(self,package):
        test_map = package.get('map')
        start_tile_index = package.get('start_tile_index')
        player_unit = TestUnit(30,test_map[start_tile_index])
        test_map[-1].add_entity(GroundBlock(9))
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
            st = time.time()
            self.player.key_press(data)
            print('game key_press took: %s seconds'%(str(time.time()-st),))

    def key_release(self,data):
        if self.player:
            self.player.key_release(data)

class Test:

    def __init__(self):
        self.x = 10
        self.y = 50
