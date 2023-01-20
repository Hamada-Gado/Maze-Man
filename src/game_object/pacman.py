from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

import pygame as pg

pg.init()

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, Direction

from .game_object import Game_Object


class PacMan(Game_Object):
    
    def __init__(self, master: Game, width: int = 25, height: int = 25, speed: int = 100, offset_x: int = 0, offset_y: int = 0, x: int = 0, y: int = 0) -> None:
        super().__init__(master, width, height, speed, offset_x, offset_y, x, y)
 
        self.current_frame: float = 0
        self.frame_rate: float = 20
        self.load_frames()

    def load_frames(self):
        self.sprite_sheet: pg.surface.Surface = pg.image.load("../res/pacman.png").convert_alpha()
        self.frames: list[pg.surface.Surface] = []
        
        # sprite sheet is 3 x 3 each frame is 25 x 25
        for i in range(3): 
            for j in range(3):
                self.frames.append(pg.Surface((self.width, self.height), pg.SRCALPHA))
                self.frames[-1].blit(self.sprite_sheet, (0, 0), (j*self.width, i*self.height, self.width, self.height))


    def update(self) -> None:
        keys = pg.key.get_pressed()
        
        # move
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.direction = Direction.UP
            self.add_coordinate(y= -self.speed*self.master.delta_time)
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.direction = Direction.DOWN
            self.add_coordinate(y= self.speed*self.master.delta_time)
        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            self.direction = Direction.LEFT
            self.add_coordinate(x= -self.speed*self.master.delta_time)
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.direction = Direction.RIGHT
            self.add_coordinate(x= self.speed*self.master.delta_time)
     
        # check to wrap to around
        if self.coordinate.y < -self.height:
            self.set_coordinate(y= SCREEN_HEIGHT)
        if self.coordinate.y > SCREEN_HEIGHT:
            self.set_coordinate(y= -self.height)
        if self.coordinate.x < -self.width:
            self.set_coordinate(x= SCREEN_WIDTH)
        if self.coordinate.x > SCREEN_WIDTH:
            self.set_coordinate(x= -self.width)        

        # check for collision
        self.check_collision()

        # update frames
        self.current_frame += (self.frame_rate * self.master.delta_time) 
        self.current_frame = self.current_frame if self.current_frame < len(self.frames) else 0
    
    def draw(self) -> None:
        image = self.frames[int(self.current_frame)]
        if self.direction == Direction.UP:
            image = pg.transform.rotate(surface= image, angle= 90)
        elif self.direction == Direction.DOWN:
            image = pg.transform.rotate(surface= image, angle= -90)
        elif self.direction == Direction.LEFT:
            image = pg.transform.rotate(surface= image, angle= 180)
        elif self.direction == Direction.RIGHT:
            image = image
        
        self.master.window.blit(image, self.rect)