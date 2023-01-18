import sys, pygame as pg

from game_object.pacman import PacMan
pg.init()

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class Game:
    
    def __init__(self) -> None:
        self.window: pg.surface.Surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags= pg.DOUBLEBUF)
        pg.display.set_caption("Pac-Man")
        self.clock: pg.time.Clock = pg.time.Clock()
        self.fps: int = FPS
        self.delta_time: float = 0
        
        self._init()
        
    def _init(self) -> None:
        self.pacman: PacMan = PacMan(self, x= 10, y= 20)
        
    def restart(self) -> None:
        self._init()
        
    def terminate(self, event: pg.event.Event) -> None:
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()
        
    def update(self):
        self.pacman.update()
    
    def draw(self):
        self.window.fill("#0000ff")
        self.pacman.draw()
        
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