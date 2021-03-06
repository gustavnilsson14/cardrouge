import arcade, time, arcade.window_commands
from message import JoinableObject
import game
from utilities import *

class WindowHandler(arcade.Window,JoinableObject):
    """ Main application class. """

    def __init__(self, queues, defaults,game_process):
        self.offset = (0,0)
        self.zoom = 1
        self.defaults = defaults
        self.game_process = game_process
        self.tiles = []
        self.tile_ids = []
        super().__init__(self.defaults.get('width'), self.defaults.get('height'))
        JoinableObject.__init__(self,queues)

        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.all_ui_list = arcade.SpriteList()
        self.all_text_list = []

        self.setup()

    def move_camera(self,data):
        self.zoom = data.get('zoom')
        self.offset = data.get('offset')
        self.offset_y = data.get('offset_y')
        self.clip_y = data.get('clip_y')

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.join()

        #self.all_sprites_list = arcade.SpriteList()

        #self.all_sprites_list.append(self.player_sprite)

        arcade.set_background_color((0,0,0))

    def get_tile_index(self,tile):
        #TODO: CHANGE TO B SEARCH
        if tile.id in self.tile_ids:
            return self.tile_ids.index(tile.id)
        return None

    def add_to_tiles(self,tile):
        self.tile_ids += [tile.id]
        self.tiles += [tile]
        return 0

    def tile_changed(self,tile,fov):
        if tile.changed:
            #print(tile.changed)
            return 1
        return 0

    def add_ui(self,elements):
        self.remove_ui()
        self.all_text_list = []
        for element in elements:
            element_sprite = arcade.Sprite(element.image, self.defaults.get('ui_scaling'))
            element_sprite.center_x = element.pos[0]
            element_sprite.center_y = element.pos[1]
            self.all_ui_list.append(element_sprite)
            if element.text == None:
                continue
            self.all_text_list += [element]

    def add_sprites(self,data):
        self.remove_sprites()
        data = reversed(data)
        for tile in data:
            scaling = self.defaults.get('tile_size')*self.defaults.get('scaling')
            (x, z) = tile.to_iso()
            x = (x * scaling) - (scaling*self.offset[0]) + (self.defaults.get('width')/2)
            raw_z = (z * scaling) - (scaling*self.offset[1]) + (self.defaults.get('height')/2)
            offset_next_height = 0
            for entity in tile.entities:
                y = entity.y - self.offset_y
                z = raw_z + self.defaults.get('scaling')*(entity.height*y) + entity.offset_height + offset_next_height;
                offset_next_height = entity.offset_next_height
                if self.clip_y + self.offset_y < entity.y:
                    continue
                if self.clip_y + self.offset_y == entity.y and entity.image == 'res/sprites/blocks/cliffgrass.png':
                    entity.image = 'res/sprites/blocks/cliffwall.png'
                entity_sprite = arcade.Sprite(entity.image, self.defaults.get('scaling'))
                entity_sprite.center_x = x
                entity_sprite.center_y = z
                self.all_sprites_list.append(entity_sprite)

    def remove_sprites(self):
        while len(self.all_sprites_list) != 0:
            self.all_sprites_list.remove(self.all_sprites_list[0])

    def remove_ui(self):
        while len(self.all_ui_list) != 0:
            self.all_ui_list.remove(self.all_ui_list[0])

    def add_text(self,data):
        pass
        #arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_draw(self):
        arcade.start_render()
        self.join()
        self.all_sprites_list.draw()
        self.all_ui_list.draw()
        for element in self.all_text_list:
            text_pos = TupleHelper.add_t(element.pos,element.text.pos)
            arcade.draw_text(element.text.text, text_pos[0], text_pos[1], element.text.color, element.text.font_size)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.terminate()
        self.run(game.Game.key_press,key)

    def on_key_release(self, key, modifiers):
        self.run(game.Game.key_release,key)

    def on_mouse_motion(self, x, y, dx, dy):
        print(x,y)

    def on_mouse_press(self, x, y, button, modifiers):
        print(x,y)

    def animate(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        pass
