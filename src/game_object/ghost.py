from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from constants import CELL_HEIGHT, CELL_WIDTH, Direction

if TYPE_CHECKING:
    from states.play_state import Play_State

import pygame as pg

from ai import Ai

from .game_object import Game_Object

pg.init()

class Ghost(Game_Object, ABC):
    
    def __init__(self, master: Play_State, width: int = 25, height: int = 25, speed: int = 50, x: int = 0, y: int = 0) -> None:
        super().__init__(master, width, height, speed, x, y)
        self.ai: Ai = Ai(self.master)
        
        self.direction = Direction.NONE
        
        self.current_frame: float = 0
        self.frame_rate: float = 8
        
    def load_frames(self, path: str):
        self.sprite_sheet: pg.surface.Surface = pg.image.load(path).convert_alpha()
        self.frames: dict[Direction, list[pg.surface.Surface]] = dict()
        
        # sprite sheet is 2 x 5 and each frame is 25 x 25
        for i, direction in zip(range(5), Direction):
            self.frames[direction] = list()            
            for j in range(2):
                self.frames[direction].append(pg.Surface((self.width, self.height), pg.SRCALPHA)) 
                self.frames[direction][-1].blit(self.sprite_sheet, (0, 0), (j*self.width, i*self.height, self.width, self.height))

    @abstractmethod
    def update(self) -> None: ...
               
    def draw(self) -> None:
        self.master.game.window.blit(self.frames[self.direction][int(self.current_frame)], self.rect)

        
class Red_Ghost(Ghost):
    
    def __init__(self, master: Play_State, width: int = 25, height: int = 25, speed: int = 50, x: int = 0, y: int = 0) -> None:
        super().__init__(master, width, height, speed, x, y)
        self.load_frames("../res/red ghost.png")
        
    def update(self):
        # make a path to target if finished the last one
        if not self.ai.path:
            target = self.master.pacman.get_coordinate
            target = int(target[1] / CELL_HEIGHT), int(target[0] / CELL_WIDTH)
            
            agent  = self.get_coordinate
            agent  = int(agent[1] / CELL_HEIGHT), int(agent[0] / CELL_WIDTH)
            
            self.ai.solve(target, agent)
            
        self.direction, next_cell = self.ai.path[0]
        
        # move
        # change direction if reached next cell
        if self.direction == Direction.UP:
            self.add_coordinate(y= -self.speed*self.master.game.delta_time)
            if self.rect.centery < next_cell.row * CELL_HEIGHT + CELL_HEIGHT//2:
                self.ai.path.popleft()
        elif self.direction == Direction.DOWN:
            self.add_coordinate(y= self.speed*self.master.game.delta_time)
            if self.rect.centery > next_cell.row * CELL_HEIGHT + CELL_HEIGHT//2:
                self.ai.path.popleft()
        elif self.direction == Direction.LEFT:
            self.add_coordinate(x= -self.speed*self.master.game.delta_time)
            if self.rect.centerx < next_cell.col * CELL_WIDTH + CELL_WIDTH//2:
                self.ai.path.popleft()
        elif self.direction == Direction.RIGHT:
            self.add_coordinate(x= self.speed*self.master.game.delta_time)
            if self.rect.centerx > next_cell.col * CELL_WIDTH + CELL_WIDTH//2:
                self.ai.path.popleft()
        
        # check for collision     
        for wall in self.master.maze.walls.values():
            if not self.rect.colliderect(wall):
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
        
        # update frames
        self.current_frame += (self.frame_rate * self.master.game.delta_time) 
        self.current_frame = self.current_frame if self.current_frame < len(self.frames[self.direction]) else 0
    
    def draw(self) -> None:
        super().draw()
