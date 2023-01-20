from enum import Enum, auto

FPS: int                = 60
SCREEN_WIDTH: int       = 600
SCREEN_HEIGHT: int      = 600
GAME_OBJECT_WIDTH: int  = 40
GAME_OBJECT_HEIGHT: int = 40
COLUMNS: int            = SCREEN_WIDTH//GAME_OBJECT_WIDTH #* 15
ROWS: int               = SCREEN_HEIGHT//GAME_OBJECT_HEIGHT #* 15

class Direction(Enum):
    
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    NONE = auto()