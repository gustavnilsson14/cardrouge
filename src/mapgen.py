import time, math
from message import *
from unit import *
from block import *
from prop import *
from item import *
from world import *
import game

class MapGen(JoinableObject):

    def __init__(self,queues):
        JoinableObject.__init__(self,queues)
        self.generate()
        return
        while 1:
            if self.join():
                continue
            self.generate()
            time.sleep(0.001)

    def generate(self):
        pass

    def send_map(self,data):
        pass

    def map_template(self):
        pass

class WorldGen(MapGen):

    REGIONS_SIDE_LENGTH = 2
    SMOOTH_PASSES = 4

    def __init__(self,queues):
        self.regions = []
        self.subregions = []
        self.areas = []
        self.edge_areas = None
        self.world_outlined = 0
        MapGen.__init__(self,queues)

    def is_region_center(self,x,y,max_side):
        if x > 0 and x < max_side-1 and y > 0 and y < max_side-1:
            if x % 6 in range(2,4) and y % 6  in range(2,4):
                return 1
        return 0

    def is_subregion_center(self,x,y):
        if x % 3 == 1 and y % 3 == 1:
            return 1
        return 0

    def generate(self):
        max_side = WorldGen.REGIONS_SIDE_LENGTH * 6
        regions = self.get_regions()

        for y in range(0,max_side):
            x_list = []
            for x in range(0,max_side):
                region_x = math.floor(x/6)
                region_y = math.floor(y/6)
                region = regions[region_x][region_y]
                subregion_x = math.floor((x/3)%2)
                subregion_y = math.floor((y/3)%2)
                subregion = region.subregions[subregion_x][subregion_y]
                area = Area((x,y),region,subregion)
                area.subregion_center = self.is_subregion_center(x,y)
                area.region_center = self.is_region_center(x,y,max_side)
                x_list += [area]
            self.areas += [x_list]

        for i in range(0,WorldGen.SMOOTH_PASSES):
            self.smooth_areas()

        for y_list in self.areas:
            for area in y_list:
                area.populate()

        for y_list in self.areas:
            debug_string = ''
            for area in y_list:
                debug_string += area.get_debug()
            print(debug_string)
            print('')
        self.edge_areas = self.get_edge_areas(max_side)
        random.shuffle(self.edge_areas)
        start_area = self.edge_areas[0]
        start_area.init_entry_point()
        start_area.generate_overworld()
        start_area.generate_dungeon()
        self.update_game_map(start_area,start_area.entry_point)

    def update_game_map(self,area,entry_point):
        package = {
            'map': area.place.map,
            'start_tile_index': entry_point[0]*Area.AREA_SIDE+entry_point[1]
        }
        self.run(game.Game.start,package)

    def smooth_areas(self):
        neighbors = [(-1,-1),(-1,0),(-1,1),(1,-1),(1,0),(1,1),(0,-1),(0,1)]
        for x, y_list in enumerate(self.areas):
            for y, area in enumerate(y_list):
                area_neighbors = []
                for n in neighbors:
                    try:
                        area_neighbors += [self.areas[x+n[0]][y+n[1]]]
                    except IndexError:
                        continue
                area.smooth(area_neighbors)

    def get_regions(self):
        region_types = [HotRegion,TemperateRegion,ColdRegion]
        regions = []
        for x in range(0,WorldGen.REGIONS_SIDE_LENGTH):
            y_list = []
            for y in range(0,WorldGen.REGIONS_SIDE_LENGTH):
                region_n = x*y
                if region_n % len(region_types) == 0:
                    random.shuffle(region_types)
                y_list += [region_types[region_n % len(region_types)]()]
            regions += [y_list]
        return regions

    def get_area_at(self,pos):
        pass

    def get_edge_areas(self,max_side):
        edge_areas = []
        for x in [0,max_side-1]:
            for y in range(0,max_side):
                if self.areas[x][y] in edge_areas:
                    continue
                edge_areas += [self.areas[x][y]]
        for y in [0,max_side-1]:
            for x in range(0,max_side):
                if self.areas[x][y] in edge_areas:
                    continue
                edge_areas += [self.areas[x][y]]
        return edge_areas

class SceneGen(MapGen):

    def __init__(self,queues):
        MapGen.__init__(self,queues)
