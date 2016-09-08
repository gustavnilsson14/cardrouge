from message import JoinableObject
from windowhandler import WindowHandler
from player import *
import time, arcade

class Game(JoinableObject):

    def __init__(self,queues,defaults):
        JoinableObject.__init__(self,queues)
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

class Test:

    def __init__(self):
        self.x = 10
        self.y = 50
