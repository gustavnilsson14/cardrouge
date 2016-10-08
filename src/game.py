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
from npc import *
from ui import UI

class Game(JoinableObject):

    def __init__(self,queues,defaults):
        Camera.initialize()
        JoinableObject.__init__(self,queues)
        self.player = None
        self.ui = UI()
        self.ui.x = 1337
        self.mapgen_process = self.start_child_process(WorldGen)
        self.run(WorldGen.generate, {})
        self.wait_join()

    def update(self):
        self.join()
        self.run(WindowHandler.move_camera, Camera.get_object())
        if self.player.has_update:
            self.npc.update()
            self.run(WindowHandler.add_sprites, self.player.fov)
            self.player.has_update = 0

    def start(self,package):
        test_map = package.get('map')
        start_pos = package.get('start_pos')
        player_unit = TestUnit(start_pos[1],test_map[start_pos[0]])
        self.player = Player(player_unit, test_map)
        self.player.fov = self.player.controllable_entities[0].get_fov(test_map)
        self.npc = Npc(test_map)
        self.map_sprite_list = test_map
        self.player.set_camera()
        self.player.has_update = 1

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
