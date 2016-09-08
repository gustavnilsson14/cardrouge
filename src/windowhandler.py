import arcade, time
from message import JoinableObject
import game

class WindowHandler(arcade.Window,JoinableObject):
    """ Main application class. """

    def __init__(self, queues, defaults,game_process):
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

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.join()

        #self.all_sprites_list = arcade.SpriteList()

        #self.all_sprites_list.append(self.player_sprite)

        arcade.set_background_color((255,0,0))

    def add_sprites(self,data):
        self.all_sprites_list = arcade.SpriteList()
        for tile in data:
            (x, z) = tile.to_iso()
            x = (x * (self.defaults.get('tile_size')*self.defaults.get('scaling')))+300;
            raw_z = (z * (self.defaults.get('tile_size')*self.defaults.get('scaling')))+100;

            for y, entity in enumerate(tile.entities):
                z = raw_z + self.defaults.get('scaling')*(entity.height*y);

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
        self.join()

        self.all_sprites_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.game_process.terminate()
            exit(0)
        self.run(game.Game.key_press,key)

    def on_key_release(self, key, modifiers):
        self.run(game.Game.key_release,key)

    def animate(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        pass
