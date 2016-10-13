import arcade
from state import State
from scene import Camera
from unit import Crosshair

class PlayerState(State):

    def __init__(self,owner):
        State.__init__(self,owner)

    def handle_key_press(self,key):
        print("NOT IMPLEMENTED")
        return (0,0)

class Move:

    def handle_key_press(key):
        if key == arcade.key.UP:
            return (1,0)
        if key == arcade.key.DOWN:
            return (-1,0)
        if key == arcade.key.LEFT:
            return (0,1)
        if key == arcade.key.RIGHT:
            return (0,-1)
        return (0,0)

class StateMove(PlayerState):

    def __init__(self,owner):
        PlayerState.__init__(self,owner)

    def handle_key_press(self,key):
        move_vector = Move.handle_key_press(key)
        if move_vector != (0,0):
            self.owner.move_entity(move_vector)
            return (1,1)
        if key == arcade.key.X:
            Camera.clip_y += 1
            return (1,1)
        if key == arcade.key.Z:
            Camera.clip_y -= 1
            return (1,1)
        if key == arcade.key.D:
            self.owner.draw_card()
            return (1,1)
        return (0,0)

class StateTarget(PlayerState):

    def __init__(self,owner):
        PlayerState.__init__(self,owner)
        self.crosshair = owner.add_unit(self.get_crosshair())

    def handle_key_press(self,key):
        move_vector = Move.handle_key_press(key)
        if move_vector != (0,0):
            self.owner.controllable_entities[1].move(self.owner.game_map,move_vector)
            return (1,0)
        if key == arcade.key.X:
            self.owner.controllable_entities[1].y += 1
            Camera.clip_y += 1
            return (1,0)
        if key == arcade.key.Z:
            self.owner.controllable_entities[1].y -= 1
            Camera.clip_y -= 1
            return (1,0)
        if key == arcade.key.BACKSPACE:
            self.change_state(StateMove(self.owner))
            return (1,0)
        if key == arcade.key.SPACE:
            self.change_state(StateAnimation(self.owner))
        return (0,0)

    def change_state(self,state):
        self.remove_crosshair()
        State.change_state(self.state)

    def remove_crosshair(self):
        self.owner.remove_unit(self.crosshair)
        Camera.clip_y = 0

    def get_crosshair(self):
        unit = self.owner.controllable_entities[0]
        return Crosshair(unit.y,unit.tile)

class StateAnimation(PlayerState):

    def __init__(self,owner):
        PlayerState.__init__(self,owner)

class StateMenu(PlayerState):

    def __init__(self,owner):
        PlayerState.__init__(self,owner)
