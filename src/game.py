from message import JoinableObject
from draw import WindowHandler
import time


class Game(JoinableObject):

    def __init__(self,queues,defaults):
        JoinableObject.__init__(self,queues)
        while 1:
            self.join()
            self.update()
            time.sleep(0.00001)

    def update(self):
        self.run(WindowHandler.add_sprites,Test())

    def some_game_method(self):
        print("HEJ")

class Test:

    def __init__(self):
        self.x = 10
        self.y = 50
