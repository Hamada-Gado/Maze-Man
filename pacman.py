from typing import Any
import pygame as pg
pg.init()

from game_object import Game_Object 

class PacMan(Game_Object):
    
    SPEED: int = 100
    COLOR: str = "yellow"
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        f"""{super().__doc__}"""
        
        super().__init__(*args, **kwargs)
        
    def update(self) -> None:
        return super().update()
    
    def draw(self) -> None:
        return super().draw()