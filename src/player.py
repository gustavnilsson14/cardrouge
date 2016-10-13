import arcade
from scene import Camera, Map
from controllable import *
from player_state import *
import ui

class Player(Controllable):

    def __init__(self, controllable_entity = None, game_map = None):
        Controllable.__init__(self, game_map, StateMove(self))
        self.add_unit(controllable_entity)
        self.keys_pressed = []
        #self.controllable_entity = controllable_entity
        self.has_update = 1
        self.end_turn = 0
        self.fov = []
        self.ui = ui.UI()

    def key_press(self,data):
        if self.controllable_entities[0] == None:
            return
        self.handle_key_press(data)

    def handle_key_press(self,key=None):
        (self.has_update,self.end_turn) = self.state.handle_key_press(key)
        self.ui.handle_key_press(key)

    def draw_card(self):
        if self.controllable_entities[0].hand.is_full():
            return
        self.controllable_entities[0].draw_card()
        self.redraw_ui()

    def redraw_ui(self):
        self.ui.has_update = 1
        for index, card in enumerate(self.controllable_entities[0].hand.list):
            self.ui.remove_elements_by_entity(card)
            ui_x = index*80
            card_index = (index+1) % 10
            new_element = ui.Element((40+ui_x,40),'res/ui/cards/base.png',card)
            new_element.add_text(str(card_index),(20,20))
            self.ui.add_element(new_element)
            self.ui.add_listener(ui.Keys.NUM.get(card_index),self,'play_card',new_element)

    def play_card(self,element):
        card = element.entity
        if not self.controllable_entities[0].hand.in_list(card):
            return 0
        for index, other_card in enumerate(self.controllable_entities[0].hand.list):
            card_index = index+1 % 10
            self.ui.remove_listeners(ui.Keys.NUM.get(card_index))
            self.ui.remove_elements_by_entity(other_card)
        if self.controllable_entities[0].play_card(card):
            self.state = StateTarget(self)
            self.has_update = 1
            self.redraw_ui()
            return 1
        return 0

    def move_entity(self,vector):
        self.controllable_entities[0].move(self.game_map,vector)
        tile = self.controllable_entities[0].tile
        self.fov = self.controllable_entities[0].get_fov(self.game_map)

        self.sort_fov()
        self.set_camera()

        tile.raycast(self.game_map, self.controllable_entities[0].y, self.game_map[0], 1,)

        return 1

    def sort_fov(self):
        self.fov.sort(key = lambda tile: (tile.pos[0],tile.pos[1]))

    def set_camera(self):
        Camera.move_to(self.controllable_entities[0].tile.pos)
        Camera.offset_y = self.controllable_entities[0].y
        #self.game_map.set_transparent(self.controllable_entity)
