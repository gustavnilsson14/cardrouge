class Map:

    def __init__(self,width,depth):
        pass

class Tile:

    def __init__(self,pos):
        self.pos = pos
        self.entities = []

    def add_entity(self,entity):
        self.entities += [entity]
