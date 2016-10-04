import arcade
from scene import Camera, Map
from controllable import *

class Player(Controllable):

    def __init__(self, controllable_entity = None, game_map = None):
        Controllable.__init__(self, game_map)
        self.addUnit(controllable_entity)
        self.keys_pressed = []
        #self.controllable_entity = controllable_entity
        self.has_update = 1
        self.fov = []

    def key_press(self,data):
        if self.controllable_entities[0] == None:
            return
        if data in self.keys_pressed:
            return
        self.keys_pressed += [data]
        self.handle_pressed_keys(data)

    def key_release(self,data):
        if self.controllable_entities[0] == None:
            return
        if data in self.keys_pressed:
            self.keys_pressed.remove(data)

    def handle_pressed_keys(self,key = None):
        self.has_update = 1
        for key in self.keys_pressed:
            if key == arcade.key.UP:
                self.move_entity((1,0))
            elif key == arcade.key.DOWN:
                self.move_entity((-1,0))
            elif key == arcade.key.LEFT:
                self.move_entity((0,1))
            elif key == arcade.key.RIGHT:
                self.move_entity((0,-1))
            elif key == arcade.key.X:
                Camera.clip_y += 1
            elif key == arcade.key.Z:
                Camera.clip_y -= 1

    def move_entity(self,vector):
        self.controllable_entities[0].move(self.game_map,vector)
        tile = self.controllable_entities[0].tile
        self.fov = self.controllable_entities[0].get_fov(self.game_map)

        self.fov.sort(key = lambda tile: (tile.pos[0],tile.pos[1]))
        #print(len(self.controllable_entity.tile.entities))
        self.set_camera()
        print(self.controllable_entities[0].y, self.controllable_entities[0].tile.pos )

        tile.raycast(self.game_map, self.controllable_entities[0].y, self.game_map[0], 1,)

        return 1

    def set_camera(self):
        Camera.move_to(self.controllable_entities[0].tile.pos)
        Camera.offset_y = self.controllable_entities[0].y
        #self.game_map.set_transparent(self.controllable_entity)
