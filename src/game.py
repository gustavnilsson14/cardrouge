import time, arcade
from multiprocessing import Process, Queue
from message import JoinableObject
from windowhandler import WindowHandler
from mapgen import MapGen
from player import *
from unit import *
from scene import *
import time

class Game(JoinableObject):

    def __init__(self,queues,defaults):
        JoinableObject.__init__(self,queues)

        self.mapgen_process = self.start_mapgen_process()
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

    def start_mapgen_process(self):
        return
        mapgen_queues = {
            'Game': self.queues.get('input'),
            'input': self.queues.get('MapGen')
        }
        mapgen_process = Process(target=MapGen,args=(mapgen_queues))
        mapgen_process.start()
        return mapgen_process

class Test:

    def __init__(self):
        self.x = 10
        self.y = 50
