import time
import tkinter as tk
from constants import *
from maze import Maze
from pacman import PacMan
from pellet import Pellet
from ghost import *

class Game:
    
    def __init__(self) -> None:
        self.root: tk.Tk = tk.Tk()
        self.canvas: tk.Canvas = tk.Canvas(self.root, width= WIDTH, height= HEIGHT)
        
        self.keys: dict[str, bool] = dict()
        self.root.bind('<Key>', self.key_listener)

        # setup
        self.maze: Maze = Maze(self)

        self.player: PacMan = PacMan(self)
        self.pellet: Pellet = Pellet(self)

        self.ghosts: list[Ghost] = []
        self.ghosts.append(Orange_Ghost(self))
        self.ghosts.append(Red_Ghost(self))
        self.ghosts.append(Blue_Ghost(self))
        self.ghosts.append(Pink_Ghost(self))

        self.delta_time: float = 0
         
    def restart(self) -> None:
        self.maze = Maze(self)

        self.player = PacMan(self)
        self.pellet = Pellet(self)

        self.ghosts = []
        self.ghosts.append(Orange_Ghost(self))
        self.ghosts.append(Red_Ghost(self))
        self.ghosts.append(Blue_Ghost(self))
        self.ghosts.append(Pink_Ghost(self))

        self.root.after(0, self._run)
        self.delta_time = time.time()

    def run(self) -> None:
        self.canvas.pack()
        
        self.root.title("Pac-Man")

        self.root.after(0, self._run)
        self.delta_time = time.time()

        self.root.mainloop()

    def _run(self) -> None:
        self.delta_time = time.time() - self.delta_time
        # print(self.delta_time*1000) #! should be removed

        self.canvas.delete("all")

        self.maze.update()
        self.pellet.update()
        self.player.update(self.delta_time)

        for ghost in self.ghosts:
            ghost.update(self.delta_time)

        self.keys = dict()

        if self.check_game_over():
            self.restart()
            return

        self.root.after(DELAY, self._run)
        self.delta_time = time.time()

    def key_listener(self, event: tk.Event) -> None:
        self.keys[event.keysym] = True

    def check_game_over(self) -> bool:
        position = self.player.coordinate.position

        for ghost in self.ghosts:
            if Maze.aabb_collision(ghost.coordinate.position, position):
                return True

        return False

