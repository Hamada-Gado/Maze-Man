from typing import Any
import pygame as pg
pg.init()

from .game_object import Game_Object 

class PacMan(Game_Object):
    
    # images
    images: list[pg.surface.Surface] = list()
    for i in range(3):
        images.append(pg.image.load(f"res/pacman/image{i}.svg"))
              
    _ = images.copy()
    _.reverse()
    images.extend(_)
    print(images)
        
    speed: int = 100
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        f"""{super().__doc__}"""
        super().__init__(*args, **kwargs)
        
        self.current_frame: float = 0
        self.frame_rate: float = 55.5

    def update(self) -> None:
        self.current_frame += (self.frame_rate * self.master.delta_time) 
        self.current_frame = self.current_frame if self.current_frame < 6 else 0
    
    def draw(self) -> None:
        self.master.window.blit(self.images[int(self.current_frame)], self.rect)