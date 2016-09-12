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
                for y in range(0,int(random.randint(0,6)/6)+1):
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
