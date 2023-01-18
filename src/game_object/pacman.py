from typing import Any
import pygame as pg

pg.init()

from .game_object import Game_Object 
from constants import GAME_OBJECT_WIDTH, GAME_OBJECT_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT

class PacMan(Game_Object):
    
    UP: str = "up"
    DOWN: str = "down"
    LEFT: str = "left"
    RIGHT: str = "right"
        
    speed: int = 100
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        f"""{super().__doc__}"""
        super().__init__(*args, **kwargs)

        self.current_frame: float = 0
        self.frame_rate: float = 20
        self.direction: str = PacMan.RIGHT
        self.load_frames()

    def load_frames(self):
        self.sprite_sheet: pg.surface.Surface = pg.image.load("../res/pacman.png").convert_alpha()
        self.frames: list[pg.surface.Surface] = []
        
        for i in range(3):
            for j in range(3):
                self.frames.append(pg.Surface((GAME_OBJECT_WIDTH, GAME_OBJECT_HEIGHT), pg.SRCALPHA))
                self.frames[-1].blit(self.sprite_sheet, (0, 0), (j*GAME_OBJECT_HEIGHT, i*GAME_OBJECT_WIDTH, GAME_OBJECT_WIDTH, GAME_OBJECT_HEIGHT))

    def update(self) -> None:
        keys = pg.key.get_pressed()
        
        # move
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.direction = PacMan.UP
            self.add_coordinate(y= -self.speed*self.master.delta_time)
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.direction = PacMan.DOWN
            self.add_coordinate(y= self.speed*self.master.delta_time)
        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            self.direction = PacMan.LEFT
            self.add_coordinate(x= -self.speed*self.master.delta_time)
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.direction = PacMan.RIGHT
            self.add_coordinate(x= self.speed*self.master.delta_time)

        # check to wrap to around
        if self.coordinate.y < -GAME_OBJECT_HEIGHT:
            self.set_coordinate(y= SCREEN_HEIGHT)
        if self.coordinate.y > SCREEN_HEIGHT:
            self.set_coordinate(y= -GAME_OBJECT_HEIGHT)
        if self.coordinate.x < -GAME_OBJECT_WIDTH:
            self.set_coordinate(x= SCREEN_WIDTH)
        if self.coordinate.x > SCREEN_WIDTH:
            self.set_coordinate(x= -GAME_OBJECT_WIDTH)
        
        # update frames
        self.current_frame += (self.frame_rate * self.master.delta_time) 
        self.current_frame = self.current_frame if self.current_frame < len(self.frames) else 0
    
    def draw(self) -> None:
        image = self.frames[int(self.current_frame)]
        if self.direction == PacMan.UP:
            image = pg.transform.rotate(surface= image, angle= 90)
        elif self.direction == PacMan.DOWN:
            image = pg.transform.rotate(surface= image, angle= -90)
        elif self.direction == PacMan.LEFT:
            image = pg.transform.rotate(surface= image, angle= 180)
        elif self.direction == PacMan.RIGHT:
            image = image
        
        self.master.window.blit(image, self.rect)