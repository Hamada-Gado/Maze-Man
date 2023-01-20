from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from constants import Direction

if TYPE_CHECKING:
    from game import Game

import pygame as pg

from ai import Ai

from .game_object import Game_Object

pg.init()

class Ghost(Game_Object, ABC):
    
    def __init__(self, master: Game, width: int = 25, height: int = 25, speed: int = 0, offset_x: int = 0, offset_y: int = 0, x: int = 0, y: int = 0) -> None:
        super().__init__(master, width, height, speed, offset_x, offset_y, x, y)
        
        self.ai: Ai = Ai(self.master)
         
        self.current_frame: float = 0
        self.frame_rate: float = 20
        
    def load_frames(self, path: str):
        self.sprite_sheet: pg.surface.Surface = pg.image.load(path).convert_alpha()
        self.frames: dict[Direction, list[pg.surface.Surface]] = dict()
        
        # sprite sheet is 2 x 5 and each frame is 25 x 25
        for i, direction in zip(range(5), Direction.ALL.value):
            self.frames[direction] = list()            
            for j in range(2):
                self.frames[direction].append(pg.Surface((self.width, self.height), pg.SRCALPHA)) 
                self.frames[direction][-1].blit(self.sprite_sheet, (0, 0), (j*self.width, i*self.height, self.width, self.height))
      
    def update(self) -> None:
        return super().update()
                
    def draw(self) -> None:
        self.master.window.blit(self.frames[self.direction][int(self.current_frame)], self.rect)