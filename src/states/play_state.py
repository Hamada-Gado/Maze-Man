from __future__ import annotations

from typing import TYPE_CHECKING

from constants import State

if TYPE_CHECKING:
    from game import Game

import pygame as pg

from constants import COLUMNS, ROWS, CELL_HEIGHT, CELL_WIDTH, WALLS_OFFSET
from game_object.ghost import Red_Ghost
from game_object.maze_man import Maze_Man 
from game_object.pellet import Pellet
from maze import Maze

from .base_state import Base_State


class Play_State(Base_State):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.maze = Maze(self)
        self.maze_man: Maze_Man = Maze_Man(self, x= WALLS_OFFSET, y= WALLS_OFFSET)
        self.pellet: type[Pellet] = Pellet
        self.pellet.create_pellets(self)
        self.red_ghost: Red_Ghost = Red_Ghost(self, x= (COLUMNS-1) * CELL_WIDTH + WALLS_OFFSET, y= (ROWS-1) * CELL_HEIGHT + WALLS_OFFSET)

    def update(self) -> None:

        if self.maze_man.rect.colliderect(self.red_ghost.rect) or len(self.pellet.pellets) == 0:
            self.game.state_machine.change(State.SCORE_STATE, self.pellet.eaten)
        
        self.maze_man.update()
        self.red_ghost.update()
        self.pellet.update()
       
    def draw(self) -> None:
        self.game.window.fill("#000000")
        self.maze.draw()
        self.pellet.draw()
        self.maze_man.draw()
        self.red_ghost.draw()
        
    def enter(self) -> None:
        return super().enter()
    
    def exit(self) -> None:
        return super().exit()

    def event_handler(self, event: pg.event.Event) -> None:
        return super().event_handler(event)
