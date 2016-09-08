import arcade

class Player:

    def __init__(self):
        self.keys_pressed = []
        self.controllable_entity = None

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

    def handle_pressed_keys(key = None):
        for key in self.keys_pressed:
            if key == arcade.key.UP:
                self.controllable_entity.move(1,0)
            elif key == arcade.key.DOWN:
                self.controllable_entity.move(-1,0)
            elif key == arcade.key.RIGHT:
                self.controllable_entity.move(0,1)
            elif key == arcade.key.LEFT:
                self.controllable_entity.move(0,-1)
