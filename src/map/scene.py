import arcade, random, math,time,noise
from utilities import *
from block import *
from item import *
import world
from bisect import bisect_left
import uuid

class Map:

    # Options for hidding blocks that are between unit and camera
    fade_option = {
        'alpha': 0.25,            # Alpha of start block
        'alpha_to_distance': 0.2, # Fade out speed
        'fade_distance': 10,      # Number of tile (towards camera)
        'fade_angle': 0.1,       # 2 = ~45 degrees or two block step.
        'fade_from_block': 1      # Start fade 1 block from player tile-height
    }

    def __init__(self,area):
        self.sub_area_size = int(world.Area.AREA_SIDE / 40)
        self.overworld = self.create_overworld(area)

    def pad_debug_char(self,char,padding):
        new_char = char
        for i in range(len(char),padding):
            new_char = new_char + '.'
        return new_char

    def create_tile_grid(self):
        neighbors = [(1,0),(-1,0),(0,1),(0,-1),
                     (1,1),(1,-1),(-1,1),(-1,-1)]
        grid = []
        for x in range(0,world.Area.AREA_SIDE):
            z_list = []
            grid += [z_list]
            for z in range(0,world.Area.AREA_SIDE):
                new_tile = Tile((x,z))
                new_tile_index = (x * world.Area.AREA_SIDE) + z
                for pos in neighbors:
                    n_pos = (x+pos[0],z+pos[1])
                    neighbor_index = (n_pos[0] * world.Area.AREA_SIDE) + n_pos[1]
                    if neighbor_index < 0:
                        continue
                    try:
                        grid[n_pos[0]][n_pos[1]].neighbors += [new_tile_index]
                        new_tile.neighbors += [neighbor_index]
                    except Exception as e:
                        continue
                z_list += [new_tile]
        return grid

    def create_ramps(self,game_map):
        for index, tile in enumerate(game_map):
            block = tile.entities[-1]
            for n_pos in tile.neighbors:
                neighbor = game_map[n_pos]
                relative_vector = tile.relative_vector(neighbor)
                if relative_vector[0] != 0 and relative_vector[1] != 0:
                    continue
                n_block = neighbor.entities[-1]
                if n_block.y -1 == block.y and block.__class__ != RampBlock and n_block.__class__ != RampBlock:
                    game_map[index].add_entity(RampBlock(n_block.y,relative_vector))
                    break

        return game_map

    def create_overworld(self,area):
        grid = self.create_tile_grid()
        area_height = int(area.height()/10)
        area_height = 3
        overworld = []
        for x in range(0,world.Area.AREA_SIDE):
            for z in range(0,world.Area.AREA_SIDE):
                y = random.random()
                height = (float(noise.pnoise3(x,z,y,octaves=1,persistence=0.9))*area_height*12)+5
                grid[x][z].noise = height

        for pa in range(0,int(abs(area_height-16)/2)):
            if pa == 6:
                break
            for x in range(0,world.Area.AREA_SIDE):
                for z in range(0,world.Area.AREA_SIDE):
                    ns = 1
                    height = grid[x][z].noise
                    for n_pos in [(1,0),(0,1),(-1,0),(0,-1),  (1,1),(-1,1),(-1,-1),(1,-1)]:
                        try:
                            ns +=1
                            height += grid[x+n_pos[0]][z+n_pos[1]].noise
                        except IndexError as e:
                            pass
                    grid[x][z].noise = int(height / ns)
        for z_list in grid:
            for tile in z_list:
                for y in range(tile.noise-4,tile.noise):
                    tile.add_entity(DirtGrassBlock(y))
                overworld += [tile]
        overworld = self.create_ramps(overworld)

        return overworld

class Tile:

    def __init__(self,pos):
        self.id = str(uuid.uuid4())
        self.pos = pos
        self.entities = []
        self.neighbors = []
        self.sprites = []
        self.changed = 1

    def add_entity(self,entity):
        if entity in self.entities:
            return 0
        self.entities += [entity]
        self.entities.sort(key = lambda new_entity: (new_entity.y,new_entity.draw_priority))
        self.changed = 1
        return 1

    def remove_entity(self,entity):
        if entity not in self.entities:
            return 0
        self.entities.remove(entity)
        self.changed = 1
        return 1

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

    def get_neighbor(self,game_map,vector):
        for n_pos in self.neighbors:
            neighbor = game_map[n_pos]
            if neighbor.pos == (self.pos[0] + vector[0],self.pos[1] + vector[1],):
                return neighbor
        return None

    def to_iso(self):
        x = self.pos[0] - self.pos[1]
        z = (self.pos[0] + self.pos[1]) / 2
        return (x,z)

    def relative_vector(self,tile):
        return (self.pos[0] - tile.pos[0], self.pos[1] - tile.pos[1])

    def raycast(self, game_map, y1, target_tile, y2):

        if self.pos == target_tile.pos:
            print("Can't raycast on same tile")
            return

        result = Raycast.cast(self, target_tile)

        y_factor = (y2-y1)/len(result)
        next_tile = self
        for i, pos in enumerate(result):
            for neighbor in next_tile.neighbors:
                if game_map[neighbor].pos == pos:
                    next_tile = game_map[neighbor]
                    break
            if next_tile.get_entity_at(int(y1+(i * y_factor))) and i != 0:
                return next_tile

        return 0

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
