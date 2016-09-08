from message import *
from unit import *
from block import *
from prop import *
from item import *
import game

class MapGen(JoinableObject):

    def __init__(self,queues):
        JoinableObject.__init__(self,queues)
        self.maps = []
        self.max_maps = 50
        while 1:
            if self.join():
                continue
            self.maps += [self.generate()]
            time.sleep(0.001)

    def generate(self):
        pass

    def send_map(self,data):
        pass

    def map_template(self):
        pass
