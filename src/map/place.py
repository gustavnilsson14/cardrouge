import arcade, random, math,time,noise
from utilities import *
from block import *
from item import *
from scene import *
import world
from bisect import bisect_left
import uuid

class OverWorld(Map):

    def __init__(self,area):
        Map.__init__(self,area)
        self.map = self.create_overworld()

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

    def create_overworld(self):
        grid = self.create_tile_grid()
        area_height = int(self.area.height()/10)
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

class Dungeon(Map):

    def __init__(self,area):
        Map.__init__(self,area)
        self.max_y = 5
        self.map = self.create_dungeon_level()

    def create_empty_grid(self):
        grid = []
        for x in range(0,world.Area.AREA_SIDE):
            z_list = []
            for z in range(0,world.Area.AREA_SIDE):
                z_list += [None]
            grid += [z_list]
        return grid

    def create_dungeon_level(self):
        grid = self.create_empty_grid()
        dungeon = []
        room_count = 5
        junction_count = 5
        start_room = Room(grid)
        return dungeon

class Space:

    def __init__(self,pos,max_exits,size):
        self.pos = pos
        self.max_exits = max_exits
        self.size = size

class Room(Space):

    def __init__(self,pos=(0,0,0),max_exits=1,size=5):
        Space.__init__(self,pos,max_exits,size)

class Junction(Space):

    def __init__(self,pos=(0,0,0),max_exits=3,size=2):
        Space.__init__(self,pos,max_exits,size)

class Exit:

    def __init__(self,pos,space):
        self.pos = pos
        self.space = space

class Corridoor:

    def __init__(self,exit1,exit2,width=1):
        self.exit1 = exit1
        self.exit2 = exit2
        self.width = width
