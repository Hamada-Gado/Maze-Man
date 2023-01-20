from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

import pygame as pg

pg.init()

from abc import ABC, abstractmethod

from constants import Direction, CELL_WIDTH, CELL_HEIGHT

class Game_Object(ABC):
    
    def __init__(self, master: Game, width: int = CELL_WIDTH, height: int = CELL_HEIGHT, speed: int = 0, offset_x: int = 0, offset_y: int = 0, x: int = 0, y: int = 0) -> None:
        
        self.master: Game  = master
        self.width: int  = width
        self.height: int = height
        self.speed: int = speed
        
        self.offset_x: int = offset_x
        self.offset_y: int = offset_y
        
        self.coordinate: pg.Vector2  = pg.Vector2()
        self.rect: pg.Rect = pg.Rect(self.coordinate.x, self.coordinate.y, self.width, self.height)
        self.hit_box: pg.Rect = pg.Rect(self.coordinate.x, self.coordinate.y, self.width - self.offset_x, self.height - self.offset_y)
        
        self.direction: Direction = Direction.RIGHT

        self.set_coordinate(x, y)

    @property
    def get_coordinate(self) -> tuple[float, float]:
        return (self.coordinate.x, self.coordinate.y)

    def set_coordinate(self, x: float | int | None = None, y: float | int | None = None):
        self.coordinate.x = x if x is not None else self.coordinate.x
        self.coordinate.y = y if y is not None else self.coordinate.y
        
        self.rect.topleft    = self.get_coordinate # type: ignore
        self.hit_box.topleft = (self.coordinate.x + self.offset_x/2, self.coordinate.y + self.offset_y/2) # type: ignore
    
    def add_coordinate(self, x: float | int = 0, y: float | int = 0):
        self.coordinate.x += x
        self.coordinate.y += y
        self.set_coordinate()
        
    @abstractmethod
    def update(self) -> None: ...
  
    @abstractmethod
    def draw(self) -> None: ...
    
    def check_collision(self):
        
        for wall in self.master.maze.walls.values():
            if not self.hit_box.colliderect(wall):
                continue
            
            if self.direction == Direction.UP:
                self.set_coordinate(y= wall.bottom)
            elif self.direction == Direction.DOWN:
                self.set_coordinate(y= wall.top - self.height)
            elif self.direction == Direction.LEFT:
                self.set_coordinate(x= wall.right)
            elif self.direction == Direction.RIGHT:
                self.set_coordinate(x= wall.left - self.width)
                
            break