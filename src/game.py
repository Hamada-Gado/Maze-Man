import sys

import pygame as pg

from constants import State
from state_machine import State_Machine
from states.base_state import Base_State
from states.play_state import Play_State
from states.start_state import Start_State

pg.init()

from constants import (CELL_HEIGHT, CELL_WIDTH, FPS, SCREEN_HEIGHT,
                       SCREEN_WIDTH, WALLS_OFFSET)


class Game:
    
    def __init__(self) -> None:
        self.window: pg.surface.Surface = pg.display.set_mode((SCREEN_WIDTH + WALLS_OFFSET, SCREEN_HEIGHT + WALLS_OFFSET), flags= pg.HWSURFACE | pg.DOUBLEBUF) # + walls offset so that the lower and most right walls can appear
        pg.display.set_caption("Pac-Man")
        
        self.clock: pg.time.Clock = pg.time.Clock()
        self.fps: int = FPS
        self.delta_time: float = 0
        
        self.states: dict[State, type[Base_State]] = {
            State.PLAY_STATE: Play_State,
            State.START_STATE: Start_State
        }
        self.state_machine: State_Machine = State_Machine(self, self.states)
        self.state_machine.change(State.START_STATE)
        
    
    def terminate(self) -> None:
        pg.quit()
        sys.exit()
        
    def update(self) -> None:
        self.state_machine.update()
       
    def draw(self) -> None:
        self.window.fill("#000000")
        self.state_machine.draw()        
        pg.display.flip()
     
    def run(self) -> None:
        
        while True:
            
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.terminate()
                    
                self.state_machine.event_handler(event)
              
            self.update()
            self.draw()
            self.delta_time = self.clock.tick(self.fps)/1000
