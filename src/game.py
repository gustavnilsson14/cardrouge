from message import JoinableObject
from windowhandler import WindowHandler
from scene import *
import time

class Game(JoinableObject):

    def __init__(self,queues,defaults):
        JoinableObject.__init__(self,queues)

        test_map = Map()
        self.map_sprite_list = test_map.create_map()


        while 1:
            self.join()
            self.update()
            time.sleep(0.00001)

    def update(self):
        self.run(WindowHandler.add_sprites, self.map_sprite_list)
        self.join()


    def key_press(self,data):
        print(data)

    def key_release(self,data):
        print(data)

class Test:

    def __init__(self):
        self.x = 10
        self.y = 50
