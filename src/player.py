import arcade
from scene import Camera

class Player:

    def __init__(self, controllable_entity = None):
        self.keys_pressed = []
        self.controllable_entity = controllable_entity

    def key_press(self,data):
        if self.controllable_entity == None:
            return
        if data in self.keys_pressed:
            return
        self.keys_pressed += [data]
        self.handle_pressed_keys(data)

    def key_release(self,data):
        if self.controllable_entity == None:
            return
        if data in self.keys_pressed:
            self.keys_pressed.remove(data)

    def handle_pressed_keys(self,key = None):
        for key in self.keys_pressed:
            if key == arcade.key.UP:
                self.move_entity((1,0))
            elif key == arcade.key.DOWN:
                self.move_entity((-1,0))
            elif key == arcade.key.LEFT:
                self.move_entity((0,1))
            elif key == arcade.key.RIGHT:
                self.move_entity((0,-1))

    def move_entity(self,vector):
        self.controllable_entity.move(vector)
        Camera.move_to(self.controllable_entity.tile.pos)
