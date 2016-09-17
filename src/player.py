import arcade
from scene import Camera, Map

class Player:

    def __init__(self, controllable_entity = None, game_map = None):
        self.keys_pressed = []
        self.controllable_entity = controllable_entity
        self.game_map = game_map
        self.has_update = 1
        self.fov = []

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
            elif key == arcade.key.X:
                Camera.clip_y += 1
            elif key == arcade.key.Z:
                Camera.clip_y -= 1

    def move_entity(self,vector):
        self.has_update = 1
        self.controllable_entity.move(self.game_map,vector)
        self.fov = self.controllable_entity.get_fov(self.game_map)

        self.fov.sort(key = lambda tile: (tile.pos[0],tile.pos[1]))
        #print(len(self.controllable_entity.tile.entities))
        self.set_camera()
        print(self.controllable_entity.y, self.controllable_entity.tile.pos )
        self.game_map.raycast(self.game_map.grid[0], 1, self.controllable_entity.tile, self.controllable_entity.y )

        return 1

    def set_camera(self):
        Camera.move_to(self.controllable_entity.tile.pos)
        Camera.offset_y = self.controllable_entity.y
        #self.game_map.set_transparent(self.controllable_entity)
