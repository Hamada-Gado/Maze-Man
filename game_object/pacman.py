from typing import Any
import pygame as pg
pg.init()

from .game_object import Game_Object 

class PacMan(Game_Object):
    
    UP: str = "up"
    DOWN: str = "down"
    LEFT: str = "left"
    RIGHT: str = "right"
    
    # images
    images: list[pg.surface.Surface] = list()
    for i in range(3):
        images.append(pg.image.load(f"res/pacman/image{i}.svg"))
              
    tmp = images.copy()
    tmp.reverse()
    images.extend(tmp)
    del tmp
        
    speed: int = 100
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        f"""{super().__doc__}"""
        super().__init__(*args, **kwargs)

        self.current_frame: float = 0
        self.frame_rate: float = 5.5
        self.direction: str = PacMan.RIGHT

    def update(self) -> None:
        keys = pg.key.get_pressed()
        
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
        
        self.current_frame += (self.frame_rate * self.master.delta_time) 
        self.current_frame = self.current_frame if self.current_frame < 6 else 0
    
    def draw(self) -> None:
        image = self.images[int(self.current_frame)]
        if self.direction == PacMan.UP:
            image = pg.transform.rotate(surface= image, angle= 90)
        elif self.direction == PacMan.DOWN:
            image = pg.transform.rotate(surface= image, angle= -90)
        elif self.direction == PacMan.LEFT:
            image = pg.transform.rotate(surface= image, angle= 180)
        elif self.direction == PacMan.RIGHT:
            image = image
        
        self.master.window.blit(image, self.rect)