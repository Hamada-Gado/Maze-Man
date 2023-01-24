from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

import pygame as pg

pg.init()

from abc import ABC, abstractmethod

from constants import Direction, CELL_WIDTH, CELL_HEIGHT

class Game_Object(ABC):
    
    def __init__(self, master: Game, width: int = CELL_WIDTH, height: int = CELL_HEIGHT, speed: int = 0, x: int = 0, y: int = 0) -> None:
        
        self.master: Game  = master
        self.width: int  = width
        self.height: int = height
        self.speed: int = speed
        
        self.coordinate: pg.Vector2  = pg.Vector2()
        self.rect: pg.Rect = pg.Rect(self.coordinate.x, self.coordinate.y, self.width, self.height)
        
        self.direction: Direction = Direction.NONE

        self.set_coordinate(x, y)

    @property
    def get_coordinate(self) -> tuple[float, float]:
        return (self.coordinate.x, self.coordinate.y)

    def set_coordinate(self, x: float | int | None = None, y: float | int | None = None):
        self.coordinate.x = x if x is not None else self.coordinate.x
        self.coordinate.y = y if y is not None else self.coordinate.y
        
        self.rect.topleft    = self.get_coordinate # type: ignore
        
    def add_coordinate(self, x: float | int = 0, y: float | int = 0):
        self.coordinate.x += x
        self.coordinate.y += y
        self.set_coordinate()
        
    @abstractmethod
    def update(self) -> None: ...
  
    @abstractmethod
    def draw(self) -> None: ...

    @abstractmethod
    def load_frames(self) -> None: ...