from enum import Enum

class MD(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    NONE = 5

class Brushes(Enum):
    NONE = 0
    PENCIL = 1
    PAINT_BRUSH = 2
    PAINT_BUCKET = 3
    TILE_DRAG = 4
    EYE_DROPPER = 5
    ERASER = 6

class LayerKeys(Enum):
    ITEM_GROUP = 1
    ITEM_LIST = 2 
    ITEM_TMAP_POS_LIST = 3
    VISIBLE = 4
    REMOVABLE = 5
    LIST_ITEM = 6
    NAME = 7
    Z_LEVEL = 8
    CLOSE_BUTTON = 9
    TAB_COLOR = 10