from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

from constants import CELL_HEIGHT, CELL_WIDTH, WALLS_OFFSET
from game_object.ghost import Red_Ghost
from game_object.pacman import PacMan
from game_object.pellet import Pellet
from maze import Maze

from .base_state import Base_State
import pygame as pg


class Play_State(Base_State):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.maze = Maze(self)
        self.pacman: PacMan = PacMan(self, x= 4*CELL_WIDTH + WALLS_OFFSET, y= WALLS_OFFSET)
        self.pellet: type[Pellet] = Pellet
        self.pellet.create_pellets(self)
        self.red_ghost: Red_Ghost = Red_Ghost(self, x= CELL_WIDTH + WALLS_OFFSET, y= CELL_HEIGHT + WALLS_OFFSET)

    def update(self) -> None:

        if self.pacman.rect.colliderect(self.red_ghost.rect) or len(self.pellet.pellets) == 0:
            self.game.terminate()
        
        self.pacman.update()
        self.red_ghost.update()
        self.pellet.update()
       
    def draw(self) -> None:
        self.game.window.fill("#000000")
        self.maze.draw()
        self.pellet.draw()
        self.pacman.draw()
        self.red_ghost.draw()
        
    def enter(self) -> None:
        return super().enter()
    
    def exit(self) -> None:
        return super().exit()

    def event_handler(self, event: pg.event.Event) -> None:
        return super().event_handler(event)
