import arcade, random
from utilities import *
from block import *

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
        for x in range(0,10):
            for z in range(0,10):
                new_tile = Tile((x,z))
                #for y in range(0,int(random.randint(0,34)/34)+1):
                #    new_tile.add_entity(GroundBlock())

                #Custom map for testing fade
                new_tile.add_entity(GroundBlock())
                if int(random.randint(0,100)) < 20:
                    for i in range(0,4):
                        new_tile.add_entity(GroundBlock())
                grid += [new_tile]
        neighbors = [(-1,-1),(-1,0),(0,-1),(-1,1),(1,-1),(1,0),(1,1),(0,1)]
        for tile in grid:
            tile_neighbors = []
            for n in neighbors:
                #TODO: This is not correct! only works for index 10-99
                index = (tile.pos[1] + n[1])+((tile.pos[0] + n[0]) * 10)
                if index > 0 and index < len(grid)-1:
                    tile_neighbors += [grid[index]]
            tile.neighbors = tile_neighbors

        ramptiles = []
        '''for tile in grid:
            if len(tile.entities) == 1:
                continue
            ramptile = random.choice(tile.neighbors)
            if len(ramptile.entities) != 1:
                continue
            ramptiles +=[ramptile]

        for tile in ramptiles:
            tile.add_entity(RampBlock())'''
        return grid

    def set_transparent(self, entity):
        #TODO: Don't do this loop!
        #      Create list of all previous transparent block and set them to non transparent?
        for tile in self.grid:
            for block in tile.entities:
                block.transparent = 1

        height = entity.tile.entities.index(entity)
        tile = entity.tile

        # Get options
        alpha = self.fade_option.get('alpha')
        alpha_to_distance = self.fade_option.get('alpha_to_distance')
        fade_distance = self.fade_option.get('fade_distance')
        fade_angle = self.fade_option.get('fade_angle')
        fade_from_block = self.fade_option.get('fade_from_block')

        #Do da thing!
        for tile_distance in range(0, fade_distance):
            # Make block transparent in an angle to camera.
            height_to_distance = height + int( tile_distance * fade_angle ) + fade_from_block
            # Make closes neighbors transparent.
            for neighbor_index in range(0, 3):
                # Get get number of enities (height) of neighbor tile.
                entities_on_neighbor = len( tile.neighbors[neighbor_index].entities )
                if height_to_distance < entities_on_neighbor:
                    for block_index in range( height_to_distance, entities_on_neighbor ):
                        # Calculate new alpha depending on height between player and block.
                        new_alpha = alpha + (alpha_to_distance * ( height_to_distance - block_index ))
                        tile.neighbors[neighbor_index].entities[block_index].transparent = new_alpha

                        #TODO: Remove line and do something better!
                        tile.neighbors[neighbor_index].entities[block_index-1].image="res/sprites/blocks/cliffwall.png"

            tile = tile.neighbors[0]

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
