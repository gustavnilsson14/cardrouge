"""
Sprite Move With Walls

Simple program to show basic sprite usage.

Artwork from http://kenney.nl
"""
import arcade,time,sys
from multiprocessing import Process, Queue
sys.path.append('src')
sys.path.append('src/core')
sys.path.append('src/gameobject')
sys.path.append('src/map')
from game import *
from windowhandler import WindowHandler
from message import *

if __name__ == '__main__':

    defaults = {
        'width': 800,
        'height': 600,
        'scaling': 1.5,
        'tile_size': 30
    }

    windowhandler_in_q = Queue()
    game_in_q = Queue()
    mapgen_in_q = Queue()

    windowhandler_queues = {
        'Game': game_in_q,
        'input': windowhandler_in_q
    }
    game_queues = {
        'MapGen': mapgen_in_q,
        'WindowHandler': windowhandler_in_q,
        'input': game_in_q
    }

    def start_game_process(queues,defaults):
        game_process = Process(target=Game,args=(queues,defaults))
        game_process.start()
        return game_process

    game_process = start_game_process(game_queues,defaults)

    window = WindowHandler(windowhandler_queues,defaults,game_process)
    arcade.run()
