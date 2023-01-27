from __future__ import annotations

from typing import TYPE_CHECKING

from constants import CELL_HEIGHT, CELL_WIDTH, WALLS_OFFSET

if TYPE_CHECKING:
    from states.play_state import Play_State
    
import pygame as pg

from .game_object import Game_Object

pg.init()

class Pellet(Game_Object):
    pellets: list[Pellet] = list()
    master: Play_State
    
    def __init__(self, row: int, col: int, width: int = 16, height: int = 16) -> None:       
        self.rect: pg.Rect = pg.Rect(0, 0, width, height)
        self.rect.center = col * CELL_WIDTH + WALLS_OFFSET + CELL_WIDTH // 2, row * CELL_HEIGHT + WALLS_OFFSET + CELL_HEIGHT // 2
        self.load_frames()
        
    def load_frames(self) -> None:
        self.frame: pg.surface.Surface = pg.transform.scale(pg.image.load("../res/images/pellet.png"), size= (5, 5)).convert_alpha()
    
    @classmethod  
    def update(cls) -> None:
        for i, pellet in enumerate(cls.pellets[:]):
            if pellet.rect.colliderect(cls.master.pacman.rect):
                cls.pellets.remove(pellet)
    
    @classmethod
    def draw(cls) -> None:
        for pellet in cls.pellets:
            cls.master.game.window.blit(pellet.frame, pellet.rect)
        
    @classmethod
    def create_pellets(cls, master: Play_State) -> None:
        cls.master = master
        
        for r in range(cls.master.maze.rows):
            for c in range(cls.master.maze.cols):
                cls.pellets.append(Pellet(row= r, col= c))