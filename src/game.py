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
        self.npc_groups = []
        self.ui = None
        self.mapgen_process = self.start_child_process(WorldGen)
        self.run(WorldGen.generate, {})
        self.wait_join()

    def update(self):
        self.join()
        self.run(WindowHandler.move_camera, Camera.get_object())
        if self.player.has_update:
            self.run(WindowHandler.add_sprites, self.player.fov)
            self.player.has_update = 0
        if self.player.end_turn == 1:
            for npc in self.npc_groups:
                npc.update()
            self.animate()
            self.player.end_turn = 0
        if self.ui.has_update:
            self.run(WindowHandler.add_ui, self.ui.elements)
            self.ui.has_update = 0

    def animate(self):
        animations = []
        for controllable in self.npc_groups + [self.player]:
            animations += controllable.spawn_animations()
        self.entities.sort(key = lambda new_entity: (new_entity.y,new_entity.draw_priority))

    def start(self,package):
        test_map = package.get('map')
        start_pos = package.get('start_pos')
        player_unit = TestUnit(start_pos[1],test_map[start_pos[0]])
        self.player = Player(player_unit, test_map)
        self.player.fov = self.player.controllable_entities[0].get_fov(test_map)
        self.player.sort_fov()
        self.npc_groups += [Npc(test_map)]
        self.map_sprite_list = test_map
        self.player.set_camera()
        self.player.has_update = 1
        self.ui = UI()

        while 1:
            self.update()
            time.sleep(1/60)

    def key_press(self,data):
        if self.player:
            self.player.key_press(data)

    def key_release(self,data):
        return
        if self.player:
            self.player.key_release(data)
