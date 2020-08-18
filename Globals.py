from types import SimpleNamespace
from typing import NamedTuple

direction = SimpleNamespace(LEFT=0, RIGHT=1, UP=2, DOWN=3)
game_globals = SimpleNamespace(SPRITE_SCALE = 2.0, SCREEN_WIDTH = 640, SCREEN_HEIGHT = 480)

class Side:
    def __init__(self):
        self.NONE = 0
        self.TOP = 1
        self.BOTTOM = 2 
        self.LEFT = 3
        self.RIGHT = 4
    
    def getOppositeSide(self, side):
        if side == self.TOP:
            return self.BOTTOM
        elif side == self.BOTTOM:
            return self.TOP
        elif side == self.LEFT:
            return self.RIGHT
        elif side == self.RIGHT:
            return self.LEFT
        else:
            return self.NONE 



class Vector2(NamedTuple):
    x: int
    y: int 


sides = Side()