import arcade, time
from message import JoinableObject
import game

class WindowHandler(arcade.Window,JoinableObject):
    """ Main application class. """

    def __init__(self, queues, defaults,game_process):
        self.offset = (0,0)
        self.zoom = 1
        self.defaults = defaults
        self.game_process = game_process
        super().__init__(self.defaults.get('width'), self.defaults.get('height'))
        JoinableObject.__init__(self,queues)

        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.player_sprite = None
        self.wall_list = None
        self.physics_engine = None
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

    def add_sprites(self,data):
        for sprite in self.all_sprites_list:
            self.all_sprites_list.remove(sprite)

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

    def remove_sprites(self,data):
        pass

    def add_text(self,data):
        pass
        #arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_draw(self):
        arcade.start_render()
        self.all_sprites_list.draw()
        self.join()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.terminate()
        self.run(game.Game.key_press,key)

    def on_key_release(self, key, modifiers):
        self.run(game.Game.key_release,key)

    def animate(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        pass
