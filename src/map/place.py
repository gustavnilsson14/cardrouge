import arcade, random, math,time,opensimplex
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
        self.noise = opensimplex.OpenSimplex(area.seed)
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
        area_height = 4
        overworld = []
        for x in range(0,world.Area.AREA_SIDE):
            for z in range(0,world.Area.AREA_SIDE):
                y = random.random()
                height = (float(self.noise.noise2d(x,z))*area_height*12)+5
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
        self.grid = self.create_empty_grid()
        self.rooms = []
        self.junctions = []
        self.corridoors = []
        self.map = self.create_dungeon_level()

    def create_empty_grid(self):
        grid = []
        for x in range(0,world.Area.AREA_SIDE):
            z_list = []
            for z in range(0,world.Area.AREA_SIDE):
                y_list = []
                for y in range(0,world.Area.AREA_SIDE):
                    y_list += [0]
                z_list += [y_list]
            grid += [z_list]
        return grid

    def create_dungeon_level(self):
        print("-"*50)
        print("GEN START")
        print("-"*50)
        while len(self.rooms) < 3:
            self.rooms += [Room(self)]

        for x in range(0,world.Area.AREA_SIDE):
            for z in range(0,world.Area.AREA_SIDE):
                d_s = ''
                for y in range(0,world.Area.AREA_SIDE):
                    d_s += str(self.grid[x][z][y])
                print(d_s)

        print("-"*50)
        print("GEN STOP")
        print("-"*50)
        dungeon = self.grid_to_list([],-1,self.get_start_pos())
        return dungeon

    def get_start_pos(self):
        for x in range(0,world.Area.AREA_SIDE):
            for z in range(0,world.Area.AREA_SIDE):
                for y in range(0,world.Area.AREA_SIDE):
                    if self.grid[x][z][y] != 0:
                        return (x,z)
        return (0,0)

    def grid_to_list(self,dungeon=[],previous_tile=-1,pos=(0,0)):
        print("-"*50)
        print(pos)
        print("-"*50)
        x = pos[0]
        z = pos[1]
        if Space.pos_within_grid((x,z,0)) != 1:
            return dungeon
        is_tile = 0
        if type(self.grid[x][z]) != list:
            self.grid[x][z].neighbors += [dungeon.index(previous_tile)]
            previous_tile.neighbors += [dungeon.index(self.grid[x][z])]
            return dungeon
        for entity in self.grid[x][z]:
            if entity != 0:
                is_tile = 1
                break
        if is_tile == 0:
            return dungeon
        new_tile = Tile((x,z))
        for y, entity in enumerate(self.grid[x][z]):
            if entity != 0:
                new_tile.add_entity(DirtGrassBlock(y))
        dungeon += [new_tile]
        self.grid[x][z] = new_tile
        if previous_tile != -1:
            new_tile.neighbors += [dungeon.index(previous_tile)]
            previous_tile.neighbors += [dungeon.index(new_tile)]

        neighbors = [(1,0),(-1,0),(0,1),(0,-1)]
        for n_pos in neighbors:
            new_pos = (x+n_pos[0],z+n_pos[1])
            self.grid_to_list(dungeon,new_tile,new_pos)
        return dungeon

    def set_neighbors(self,pos):

        pass


class Space:

    def __init__(self,place,size):
        self.size = size
        self.pos = Space.get_random_position()
        self.insert_into_grid(place)

    def insert_into_grid(self,place):
        max_pos = (self.pos[0]+self.size,self.pos[1]+self.size,self.pos[2]+self.size)
        if Space.pos_within_grid(max_pos) != 1:
            return
        for x in range(self.pos[0],self.pos[0]+self.size):
            for z in range(self.pos[1],self.pos[1]+self.size):
                for y in range(self.pos[2],self.pos[2]+self.size):
                    if self.pos3d_is_edge((x,z,y)):
                        place.grid[x][z][y] = 1

    def pos3d_is_edge(self,pos):
        if pos[0] == range(self.pos[0],self.pos[0]+self.size)[0] or pos[0] == range(self.pos[0],self.pos[0]+self.size)[-1] :
            return 1
        if pos[1] == range(self.pos[1],self.pos[1]+self.size)[0] or pos[1] == range(self.pos[1],self.pos[1]+self.size)[-1] :
            return 1
        if pos[2] == range(self.pos[2],self.pos[2]+self.size)[0] or pos[2] == range(self.pos[2],self.pos[2]+self.size)[-1] :
            return 1
        return 0

    @staticmethod
    def pos_within_grid(pos):
        if pos[0] > world.Area.AREA_SIDE-1:
            return 0
        if pos[1] > world.Area.AREA_SIDE-1:
            return 0
        if pos[2] > world.Area.AREA_SIDE-1:
            return 0
        return 1

    @staticmethod
    def get_random_position():
        return (
            int(random.random()*world.Area.AREA_SIDE),
            int(random.random()*world.Area.AREA_SIDE),
            int(random.random()*world.Area.AREA_SIDE)
        )

class Room(Space):

    def __init__(self,place,size=7):
        Space.__init__(self,place,size)

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
