import arcade, random, math,time
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
        self.overworld = []
        self.sub_area_size = int(world.Area.AREA_SIDE / 40)
        self.create_overworld(area)

    def get_sub_area_side(self,area):
        return int(world.Area.AREA_SIDE/self.rect_base_size(area))

    def rect_base_size(self,area):
        return abs(area.stats[world.Area.INDEX_HEIGHT] - 95) / 20

    def get_random_size_rect(self,x,z,base_size):
        diff = base_size * 0.25
        diff_offset = base_size * 0.5
        max_x = int(x+base_size + (random.random() * diff) - diff_offset)
        max_z = int(x+base_size + (random.random() * diff) - diff_offset)
        x += int((random.random() * diff) - diff_offset)
        z += int((random.random() * diff) - diff_offset)
        return (x,z,max_x,max_z)

    def get_random_height(self,area):
        return int(random.random() * (area.stats[world.Area.INDEX_HEIGHT]/10))

    def create_overworld(self,area):
        self.overworld = []
        neighbors = [(1,0),(-1,0),(0,1),(0,-1),
                     (1,1),(1,-1),(-1,1),(-1,-1)]
        grid = []
        for x in range(0,world.Area.AREA_SIDE):
            z_list = []
            grid += [z_list]
            for z in range(0,world.Area.AREA_SIDE):
                new_tile = Tile((x,z))
                new_tile_index = (x * world.Area.AREA_SIDE) + z
                new_tile.add_entity(GroundBlock(15))
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
        sub_area_side = self.get_sub_area_side(area)
        rect_base_size = self.rect_base_size(area)
        print('height:',area.stats[world.Area.INDEX_HEIGHT],'sub_area_side:',sub_area_side,)
        print('-'*50)
        side_max = int(world.Area.AREA_SIDE/sub_area_side)
        for x in range(0,sub_area_side):
            for z in range(0,sub_area_side):
                rect = self.get_random_size_rect(x * side_max,z * side_max,rect_base_size)
                #print(rect)
                height = range(15,16+self.get_random_height(area))
                for tile_x in range(rect[0],rect[2]):
                    for tile_z in range(rect[1],rect[3]):
                        for y in height:
                            try:
                                grid[tile_x][tile_z].add_entity(GroundBlock(y))
                            except IndexError as e:
                                continue


        for z_list in grid:
            for tile in z_list:
                self.overworld += [tile]
        print("DONE, RETURN")

    def create_map(self):
        grid = {}
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
                grid[new_tile.id] = new_tile
        for y in range(0,10):
            grid[50].add_entity(GroundBlock(y))

        grid[49].add_entity(WaterBlock(1))
        grid[70].add_entity(RampBlock(1))
        #grid[75].add_entity(Card(1))
        grid[71].add_entity(GroundBlock(1))
        grid[72].add_entity(GroundBlock(1))
        grid[72].add_entity(RampBlock(2))
        grid[73].add_entity(GroundBlock(2))
        grid[73].add_entity(GroundBlock(1))

        return grid

    def raycast(self, start_tile, target_tile):
        result = Raycast.cast(start_tile, target_tile)
        print("doing raycast between point: ", start_tile.pos, " and ", target_tile.pos)

        next_tile = start_tile
        for pos in result:
            for neighbor in next_tile.neighbors:
                if neighbor.pos == pos:
                    next_tile = neighbor
                    print ("Found neighbor: ", neighbor.pos)
                    break

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
            print(vector,self.pos,neighbor.pos)
            if neighbor.pos == (self.pos[0] + vector[0],self.pos[1] + vector[1],):
                print("RETURN")
                return neighbor
        return None
        print(vector,self.pos,len(self.neighbors))
        for neighbor in self.neighbors:
            print(neighbor.pos)
        print('-'*10)
        for neighbor in self.neighbors:
            if neighbor.pos[0] == self.pos[0] + vector[0] and neighbor.pos[1] == self.pos[1] + vector[1]:
                print(neighbor.pos)
                print('-'*30)
                return neighbor
        return None

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
