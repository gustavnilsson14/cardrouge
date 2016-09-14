import arcade, random
from utilities import *
from block import *

class Map:

    def __init__(self,width,depth):
        self.grid = self.create_map()

    def create_map(self):
        grid = []
        for x in range(0,10):
            for z in range(0,10):
                new_tile = Tile((x,z))
                for y in range(0,int(random.randint(0,32)/32)+1):
                    new_tile.add_entity(GroundBlock())
                grid += [new_tile]
        neighbors = [(-1,-1),(-1,0),(-1,1),(1,-1),(1,0),(1,1),(0,-1),(0,1)]
        for tile in grid:
            tile_neighbors = []
            for n in neighbors:
                index = (tile.pos[1] + n[1])+((tile.pos[0] + n[0]) * 10)
                if index > 0 and index < len(grid)-1:
                    tile_neighbors += [grid[index]]
            tile.neighbors = tile_neighbors

        ramptiles = []
        for tile in grid:
            if len(tile.entities) == 1:
                continue
            ramptile = random.choice(tile.neighbors)
            if len(ramptile.entities) != 1:
                continue
            ramptiles +=[ramptile]

        for tile in ramptiles:
            tile.add_entity(RampBlock())
        return grid

class Tile:

    def __init__(self,pos):
        self.pos = pos
        self.entities = []
        self.neighbors = 0

    def add_entity(self,entity):
        if 1 == 0 : #CHECK IF REALLY ENTITY SUBCLASS
            return 0
        self.entities += [entity]

    def get_neighbor(self,vector):
        for neighbor in self.neighbors:
            if neighbor.pos[0] == self.pos[0] + vector[0] and neighbor.pos[1] == self.pos[1] + vector[1]:
                return neighbor

    def get_entity_at(self,height):
        if len(self.entities) > height:
            return self.entities[height]
        return None

    def to_iso(self):
        x = self.pos[0] - self.pos[1]
        z = (self.pos[0] + self.pos[1]) / 2
        return (x,z)

class Camera:

    @staticmethod
    def initialize(offset = (0,0)):
        Camera.zoom = 1
        Camera.offset = offset

    @staticmethod
    def move(vector = (0,0)):
        Camera.offset -= vector

    @staticmethod
    def move_to(vector = (0,0)):
        Camera.offset = vector

    @staticmethod
    def get_object():
        return {
            'zoom':Camera.zoom,
            'offset':Camera.to_iso(),
        }

    @staticmethod
    def to_iso():
        x = Camera.offset[0] - Camera.offset[1]
        z = (Camera.offset[0] + Camera.offset[1]) / 2
        return (x,z)
