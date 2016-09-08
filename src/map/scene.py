from utilities import *
import arcade
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
        self.wall_list = arcade.SpriteList()

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



        wall = arcade.Sprite("res/sprites/blocks/grass.png", Map.SPRITE_SCALING)
        y += 4*Map.SPRITE_SCALING*(4*(tile_in_height));

        wall.center_x = x
        wall.center_y = y
        self.wall_list.append(wall)
