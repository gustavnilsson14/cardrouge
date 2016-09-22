import random, math
from scene import *

class Region:

    def __init__(self):
        self.temp = 0

    def get_subregions(self):
        subregions = []
        seeds = [(0,0),(2,0),(0,2),(2,2)]
        random.shuffle(seeds)
        for x in range(0,2):
            y_list = []
            for y in range(0,2):
                y_list += [SubRegion(self.temp,seeds.pop())]
            subregions += [y_list]
        return subregions

class HotRegion(Region):

    def __init__(self):
        Region.__init__(self)
        self.temp = 80 + random.randint(0,20)
        self.subregions = self.get_subregions()

class TemperateRegion(Region):

    def __init__(self):
        Region.__init__(self)
        self.temp = 40 + random.randint(0,20)
        self.subregions = self.get_subregions()

class ColdRegion(Region):

    def __init__(self):
        Region.__init__(self)
        self.temp = random.randint(0,20)
        self.subregions = self.get_subregions()

class SubRegion:

    def __init__(self,temperature,seed):
        self.temp = temperature
        self.rain = 0
        self.height = 0
        self.rain = (seed[0]*40) + random.randint(0,20)
        self.height = (seed[1]*40) + random.randint(0,20)

class Area:

    OCEAN_LEVEL = 50
    INDEX_TEMP = 0
    INDEX_RAIN = 1
    INDEX_HEIGHT = 2
    INDEX_FEATURE = 3

    AREA_SIDE = 32

    def __init__(self,pos,region,subregion,region_center = 0,subregion_center = 0):
        self.pos = pos
        self.region = region
        self.subregion = subregion
        self.region_center = region_center
        self.subregion_center = subregion_center
        self.stats = (region.temp, subregion.rain,subregion.height)
        self.type = ''
        self.seed = random.random()
        self.entry_point = (0,0)

    def smooth(self,neighbors):
        avg_temp = 0
        avg_rain = 0
        avg_height = 0
        for neighbor in neighbors:
            avg_temp += neighbor.stats[Area.INDEX_TEMP]
            avg_rain += neighbor.stats[Area.INDEX_RAIN]
            avg_height += neighbor.stats[Area.INDEX_HEIGHT]
        avg_temp = avg_temp / len(neighbors)
        avg_rain = avg_rain / len(neighbors)
        avg_height = avg_height / len(neighbors)

        if not self.region_center:
            self.stats = (
                self.get_diff(self.stats[Area.INDEX_TEMP], avg_temp),
                self.stats[Area.INDEX_RAIN],
                self.stats[Area.INDEX_HEIGHT],
            )
        if not self.subregion_center:
            self.stats = (
                self.stats[Area.INDEX_TEMP],
                self.get_diff(self.stats[Area.INDEX_RAIN], avg_rain),
                self.get_diff(self.stats[Area.INDEX_HEIGHT], avg_height),
            )

    def populate(self):
        for feature in AreaFeatures.MAP:
            matches = 0
            for index, stat in enumerate(self.stats):
                if feature[index] == None:
                    matches += 1
                    continue
                if stat not in feature[index]:
                    break
                matches += 1
            if matches == 3:
                self.type = feature[Area.INDEX_FEATURE]
                break
            self.type = str(self.stats)

    def valid_for_settlement(self):
        if not self.region_center and not self.subregion_center:
            return 1
        return 0

    def init_entry_point(self):
        x = 0
        z = 0
        if self.pos[0] > 0:
            x = Area.AREA_SIDE
        if self.pos[1] > 0:
            z = Area.AREA_SIDE
        self.entry_point = (x,z)

    def generate_grid(self,data):
        grid = []
        for x in range(0, Area.AREA_SIDE):
            z_list = []
            for z in range(0, Area.AREA_SIDE):
                z_list += [Tile((x,z))]
            grid += [z_list]


    def get_diff(self,value,avg):
        if value < avg:
            diff = avg - value
            return int(value + (diff/2))
        diff = value - avg
        return int(value - (diff/2))

    def get_debug(self):
        char = self.pad_debug_char( self.type, 12)
        if self.region_center:
            return '.R.' + char
        if self.subregion_center:
            return '.S.' + char
        return '...' + char

    def pad_debug_char(self,char,padding):
        new_char = char
        for i in range(len(char),padding):
            new_char = new_char + '.'
        return new_char

class AreaFeatures:

    TYPE_DESERT = 'Desert'
    TYPE_OCEAN = 'Ocean'
    TYPE_JUNGLE = 'Jungle'
    TYPE_FOREST = 'Forest'
    TYPE_TAIGA = 'Taiga'
    TYPE_PLAINS = 'Grasslands'
    TYPE_SAVANNAH = 'Savannah'
    TYPE_MARSH = 'Marsh'
    TYPE_PEAK = 'Mountain'
    TYPE_GLACIER = 'Glacier'
    TYPE_WASTELAND = 'Moor'
    TYPE_STEPPE = 'Steppe'
    TYPE_TROPICS = 'Tropics'

    MAP = [
        (range(70,101),range(0,20),range(Area.OCEAN_LEVEL,90),TYPE_DESERT),
        (range(70,101),range(20,50),range(Area.OCEAN_LEVEL,90),TYPE_STEPPE),
        (range(70,101),range(50,80),range(Area.OCEAN_LEVEL,90),TYPE_JUNGLE),
        (range(70,101),range(80,101),range(Area.OCEAN_LEVEL,90),TYPE_TROPICS),
        (range(40,60),range(0,30),range(Area.OCEAN_LEVEL,90),TYPE_PLAINS),
        (range(60,80),range(0,30),range(Area.OCEAN_LEVEL,90),TYPE_SAVANNAH),
        (range(40,70),range(30,70),range(Area.OCEAN_LEVEL,90),TYPE_FOREST),
        (range(10,40),range(30,70),range(Area.OCEAN_LEVEL,90),TYPE_TAIGA),
        (range(10,40),range(0,30),range(Area.OCEAN_LEVEL,90),TYPE_WASTELAND),
        (range(10,70),range(70,101),range(Area.OCEAN_LEVEL,90),TYPE_MARSH),
        (range(0,10),None,range(Area.OCEAN_LEVEL-10,90),TYPE_GLACIER),
        (None,None,range(90,101),TYPE_PEAK),
        (None,None,range(0,Area.OCEAN_LEVEL),TYPE_OCEAN),
    ]

class Civ:

    INDEX_TEMPERAMENT = 0
    INDEX_HUMANITY = 0
    INDEX_SPIRITUALISM = 0
    INDEX_EXPLOITATION = 0
    INDEX_EXPLOITATION = 0

    def __init__(self,area):
        self.stats = []
