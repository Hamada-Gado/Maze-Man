from enum import Enum, auto

FPS: int                = 60
SCREEN_WIDTH: int       = 600
SCREEN_HEIGHT: int      = 600
CELL_WIDTH: int         = 40
CELL_HEIGHT: int        = 40
COLUMNS: int            = SCREEN_WIDTH // CELL_WIDTH #* 15
ROWS: int               = SCREEN_HEIGHT // CELL_HEIGHT #* 15
WALLS_OFFSET: int       = 3     #* width or height of walls. used to not collide with walls when placing the game objects and cause random behaviors

class Direction(Enum):
    
    NONE = auto()
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()