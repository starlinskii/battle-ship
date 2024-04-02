from headers import *
from utils import player_fire, watch_field

class player_interface:
    
    def fire(board, history):
        return player_fire(board, history)
    
    def watch(orientation, x, y, ship, ships):
        return watch_field(orientation, x, y, ship, ships)
