from enum import Enum, auto

FPS: int                = 60
SCREEN_WIDTH: int       = 600
SCREEN_HEIGHT: int      = 600
CELL_WIDTH: int         = 40
CELL_HEIGHT: int        = 40
COLUMNS: int            = SCREEN_WIDTH // CELL_WIDTH #* 15
ROWS: int               = SCREEN_HEIGHT // CELL_HEIGHT #* 15

class Direction(Enum):
    
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    NONE = auto()