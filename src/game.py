import time, arcade
from multiprocessing import Process, Queue
from message import JoinableObject
from windowhandler import WindowHandler
from mapgen import MapGen
from player import *
from unit import *

class Game(JoinableObject):

    def __init__(self,queues,defaults):
        JoinableObject.__init__(self,queues)
        self.mapgen_process = self.start_mapgen_process()
        player_unit = TestUnit((3,3,3))
        self.player = Player()
        while 1:
            self.join()
            self.update()
            time.sleep(0.00001)

    def update(self):
        self.join()
        pass
        #self.run(WindowHandler.add_sprites,Test())

    def key_press(self,data):
        self.player.key_press(data)

    def key_release(self,data):
        self.player.key_release(data)

    def start_mapgen_process(self):
        mapgen_queues = {
            'Game': self.queues.get('input'),
            'input': self.queues.get('MapGen')
        }
        print("-"*50)
        mapgen_process = Process(target=MapGen,args=(mapgen_queues))
        print("-"*50)
        mapgen_process.start()
        return mapgen_process

class Test:

    def __init__(self):
        self.x = 10
        self.y = 50
