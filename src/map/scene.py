import arcade, random
from utilities import *
from block import *
'''
class Map:

    TILE_SIZE = 50
    SPRITE_SCALING = 1
    BLOCKS = [];
    MAP = [[0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0]]

    def __init__(self):
        self.wall_list = [];

    def create_map(self):
        world_map = Map.MAP
        world_y = len(world_map)-1

        for y, row in enumerate(reversed(world_map)):
            for x, r in enumerate(reversed(row)):
                world_x = len(row)-1
                tileType = world_map[world_x-x][world_y-y]
                self.add_tile(tileType, world_x-x, world_y-y)

        return self.wall_list;

    def add_tile(self, tile_type, x, y, tile_in_height = 0):
        x = (x * (Map.TILE_SIZE*Map.SPRITE_SCALING))+300;
        y = (y * (Map.TILE_SIZE*Map.SPRITE_SCALING))-100;
        (x, y) = IsoConverter.to_iso(Point(x, y)).as_tuple()

        y += 4*Map.SPRITE_SCALING*(4*(tile_in_height));

        self.wall_list += [["res/sprites/blocks/grass.png", x, y]]
'''
class Map:

    def __init__(self,width,depth):
        self.grid = self.create_map()

    def create_map(self):
        grid = []
        for x in range(0,10):
            for z in range(0,10):
                new_tile = Tile((x,z))
                for y in range(0,random.randint(1,4)):
                    new_tile.add_entity(GroundBlock())
                grid += [new_tile]
        return reversed(grid)

class Tile:

    def __init__(self,pos):
        self.pos = pos
        self.entities = []

    def add_entity(self,entity):
        if 1 == 0 : #CHECK IF REALLY ENTITY SUBCLASS
            return 0
        self.entities += [entity]

    def to_iso(self):
        x = self.pos[0] - self.pos[1]
        z = (self.pos[0] + self.pos[1]) / 2
        return (x,z)
