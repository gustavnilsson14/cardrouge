import arcade, random, math
from utilities import *
from block import *
from item import *
from bisect import bisect_left

class Map:

    # Options for hidding blocks that are between unit and camera
    fade_option = {
        'alpha': 0.25,            # Alpha of start block
        'alpha_to_distance': 0.2, # Fade out speed
        'fade_distance': 10,      # Number of tile (towards camera)
        'fade_angle': 0.1,       # 2 = ~45 degrees or two block step.
        'fade_from_block': 1      # Start fade 1 block from player tile-height
    }

    def __init__(self,width,depth):
        self.grid = self.create_map()

    def create_map(self):
        grid = []
        for x in range(0,15):
            for z in range(0,15):
                new_tile = Tile((x,z))
                new_tile.add_entity(GroundBlock(0))
                for neighbor_prospect in grid :
                    x_diff = neighbor_prospect.pos[0] - new_tile.pos[0]
                    z_diff = neighbor_prospect.pos[1] - new_tile.pos[1]
                    if int(math.fabs(x_diff)) > 1 or int(math.fabs(z_diff)) > 1:
                        continue
                    neighbor_prospect.neighbors += [new_tile]
                    new_tile.neighbors += [neighbor_prospect]
                grid += [new_tile]
        for y in range(0,10):
            grid[50].add_entity(GroundBlock(y))

        grid[49].add_entity(WaterBlock(1))
        grid[70].add_entity(RampBlock(1))
        grid[75].add_entity(Card(1))
        grid[71].add_entity(GroundBlock(1))
        grid[72].add_entity(GroundBlock(1))
        grid[72].add_entity(RampBlock(2))
        grid[73].add_entity(GroundBlock(2))
        grid[73].add_entity(GroundBlock(1))

        return grid

    def set_transparent(self, entity):
        #TODO: Don't do this loop!
        #      Create list of all previous transparent block and set them to non transparent?
        for tile in self.grid:
            for block in tile.entities:
                block.transparent = 1

        height = entity.y
        tile = entity.tile

        # Get options
        alpha = self.fade_option.get('alpha')
        alpha_to_distance = self.fade_option.get('alpha_to_distance')
        fade_distance = self.fade_option.get('fade_distance')
        fade_angle = self.fade_option.get('fade_angle')
        fade_from_block = self.fade_option.get('fade_from_block')
'''
        #Do da thing!
        for tile_distance in range(0, fade_distance):
            # Make block transparent in an angle to camera.
            height_to_distance = height + int( tile_distance * fade_angle ) + fade_from_block
            # Make closes neighbors transparent.
            for neighbor in tile.neighbors:
                if neighbor
            for neighbor_index in range(0, 3):
                # Get get number of enities (height) of neighbor tile.
                entities_on_neighbor = len( tile.neighbors[neighbor_index].entities )
                tile.neighbors[neighbor_index].get_entity_at(height_to_distance)

                if height_to_distance < entities_on_neighbor:
                    for block_index in range( height_to_distance, entities_on_neighbor ):
                        # Calculate new alpha depending on height between player and block.
                        new_alpha = alpha + (alpha_to_distance * ( height_to_distance - block_index ))
                        tile.neighbors[neighbor_index].entities[block_index].transparent = new_alpha
            tile = tile.neighbors[0]'''

class Tile:

    def __init__(self,pos):
        self.pos = pos
        self.entities = []
        self.neighbors = []

    def add_entity(self,entity):
        self.entities += [entity]
        self.entities.sort(key = lambda new_entity: (new_entity.y,new_entity.draw_priority))

    def get_entity_below(self,entity):
        index = self.entities.index(entity) -1
        if index < 0:
            return 0
        return self.entities[index]

    def get_entity_at(self,y):
        pos = Search.binary_search(self.entities,y)
        if pos == None:
            return None
        return self.entities[pos]

    def get_neighbor(self,vector):
        for neighbor in self.neighbors:
            if neighbor.pos[0] == self.pos[0] + vector[0] and neighbor.pos[1] == self.pos[1] + vector[1]:
                return neighbor

    def to_iso(self):
        x = self.pos[0] - self.pos[1]
        z = (self.pos[0] + self.pos[1]) / 2
        return (x,z)

class Voxel:

    def __init__(self):
        self.block = 0
        self.entities = []

class Camera:

    @staticmethod
    def initialize(offset = (0,0)):
        Camera.zoom = 1
        Camera.offset = offset
        Camera.offset_y = 0
        Camera.clip_y = 0

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
            'offset_y':Camera.offset_y,
            'clip_y':Camera.clip_y
        }

    @staticmethod
    def to_iso():
        x = Camera.offset[0] - Camera.offset[1]
        z = (Camera.offset[0] + Camera.offset[1]) / 2
        return (x,z)
