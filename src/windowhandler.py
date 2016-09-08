import arcade, time
from message import JoinableObject
import game

class WindowHandler(arcade.Window,JoinableObject):
    """ Main application class. """

    def __init__(self, queues, defaults):
        self.defaults = defaults
        super().__init__(self.defaults.get('width'), self.defaults.get('height'))
        JoinableObject.__init__(self,queues)

        # Sprite lists
        self.all_sprites_list = None

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
        #wall = arcade.Sprite("brick_wall_tiled_perfect.png", self.defaults.get('scaling'))
        #wall.center_x = 1500
        #wall.center_y = 50
        #self.all_sprites_list.append(wall)
        pass

    def remove_sprites(self,data):
        pass

    def add_text(self,data):
        pass
        #arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_draw(self):
        arcade.start_render()

        #self.all_sprites_list.draw()

    def on_key_press(self, key, modifiers):
        """
        Called whenever the mouse moves.
        """
        self.run(game.Game.key_press,key)

    def on_key_release(self, key, modifiers):
        self.run(game.Game.key_release,key)

    def animate(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        pass
