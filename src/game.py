import sys

import pygame as pg
from game_object.ghost import Red_Ghost

from game_object.pacman import PacMan
from maze import Maze

pg.init()

from constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH


class Game:
    
    def __init__(self) -> None:
        self.window: pg.surface.Surface = pg.display.set_mode((SCREEN_WIDTH+3, SCREEN_HEIGHT+3), flags= pg.HWSURFACE | pg.DOUBLEBUF) # + 2 so that the lower and most right walls can appear
        pg.display.set_caption("Pac-Man")
        self.clock: pg.time.Clock = pg.time.Clock()
        self.fps: int = FPS
        self.delta_time: float = 0
        
        self._init()
        
    def _init(self) -> None:
        self.maze = Maze(self)
        self.pacman: PacMan = PacMan(self, x= 4*40 + 3, y= 0*40 + 3)
        self.red_ghost: Red_Ghost = Red_Ghost(self, x= 50, y= 50)
        
        self.restart()
        
    def restart(self) -> None:
        pass
        
    def terminate(self, event: pg.event.Event) -> None:
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()
        
    def update(self) -> None:
        self.pacman.update()
        self.red_ghost.update()
        
    def draw(self) -> None:
        self.window.fill("#000000")
        self.maze.draw()
        self.pacman.draw()
        self.red_ghost.draw()
        
        pg.display.flip()
     
    def run(self) -> None:
        
        while True:
            self.delta_time = self.clock.get_time()/1000
            
            event: pg.event.Event
            
            for event in pg.event.get():
                self.terminate(event)
              
            self.update()
            self.draw()
            self.clock.tick(self.fps)