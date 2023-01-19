import sys, pygame as pg

from game_object.pacman import PacMan
from maze import Maze
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
        # self.pacman.update()
        self.maze._create_random_maze()
    
    def draw(self):
        self.window.fill("#0000ff")
        # self.pacman.draw()
        self.draw_maze()
        
        pg.display.flip()
     
    #! should be removed     
    def draw_maze(self):
        
        for r in range(10):
            for c in range(10):
                if self.maze.maze[r][c].visited:
                    color = "#e98a36"
                    if (1, 0) in self.maze.maze[r][c].connected:
                        pg.draw.rect(self.window, color, (c*(20+10),r*(20 + 10) - 10, 20, 10))
                    if (-1, 0) in self.maze.maze[r][c].connected:
                        pg.draw.rect(self.window, color, (c*(20+10),r*(20 + 10), 20, 30))
                    if (0, -1) in self.maze.maze[r][c].connected:
                        pg.draw.rect(self.window, color, (c*(20+10) - 10,r*(20 + 10), 10, 20))
                    if (0, 1) in self.maze.maze[r][c].connected:
                        pg.draw.rect(self.window, color, (c*(20+10),r*(20 + 10), 30, 20))
                    
                else:
                    color = "#ffffff"
                    
                if self.maze.maze[r][c] == self.maze.current_node:
                    color = "#00ff00"
                    
                pg.draw.rect(self.window, color, (c*(20+10),r*(20+10), 20, 20))
                
    def run(self) -> None:
        self.maze = Maze(10, 10)
        
        while True:
            self.delta_time = self.clock.get_time()/1000
            
            event: pg.event.Event
            
            for event in pg.event.get():
                self.terminate(event)
              
            self.update()
            self.draw()
            self.clock.tick(10)