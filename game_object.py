from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

import pygame as pg

pg.init()

from abc import ABC, abstractmethod

from constants import GAME_OBJECT_HEIGHT, GAME_OBJECT_WIDTH


class Game_Object(ABC):
    
    def __init__(self, master: Game, offset_x: int = 0, offset_y: int = 0, x: int = 0, y: int = 0) -> None:
        """
        master : Game
        offset_x : int = 0
        offset_y : int = 0
        x : int = 0
        y : int = 0
        """
        
        self.master: Game  = master
        self.offset_x: int = offset_x
        self.offset_y: int = offset_y
        
        self.width: int  = GAME_OBJECT_WIDTH
        self.height: int = GAME_OBJECT_HEIGHT
        
        self.coordinate: pg.Vector2  = pg.Vector2()
        self.rect: pg.Rect = pg.Rect(self.coordinate.x, self.coordinate.y, self.width, self.height)
        self.hit_box: pg.Rect = pg.Rect(self.coordinate.x, self.coordinate.y, self.width - self.offset_x, self.height - self.offset_y)
        
        self.setcoordinate(x, y)
        
    @abstractmethod
    def update(self) -> None: ...
    @abstractmethod
    def draw(self) -> None: ...

    def setcoordinate(self, x: int | None = None, y: int | None = None):
        self.coordinate.x = x or self.coordinate.x
        self.coordinate.y = y or self.coordinate.y
        
        self.rect.topleft    = (self.coordinate.x, self.coordinate.y) # type: ignore
        self.hit_box.topleft = (self.coordinate.x + self.offset_x/2, self.coordinate.y + self.offset_y/2) # type: ignore