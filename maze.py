from __future__ import annotations
import sys
from typing import TYPE_CHECKING

from constants import WIDTH, HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT

if TYPE_CHECKING:
    from game import Game    

class Maze:

    COLS: int = WIDTH//BLOCK_WIDTH # 40
    ROWS: int = HEIGHT//BLOCK_HEIGHT # 40
    BG_COLOR: str = "black"
    BLOCK_COLOR: str = "blue"
    MAZE_FILE_PATH: str = sys.path[0] + "\\maze.txt"

    def __init__(self, master: Game) -> None:
        self.master: Game = master
        self.maze: list[list[int]] = [[0 for y in range(Maze.ROWS)] for x in range(Maze.COLS)]
        self.make_maze()

    def make_maze(self) -> None:

        with open(Maze.MAZE_FILE_PATH, "r") as f:
            data = f.read()

        data = data.split("\n")

        for x in range(Maze.COLS):
            line = data[x].split(" ")
            for y in range(Maze.ROWS):
                self.maze[x][y] = int(line[y])
    
    def update(self) -> None:
        # draw
        self.draw()

    def draw(self) -> None:
        self.master.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill= Maze.BG_COLOR)
        for x in range(Maze.COLS):
            for y in range(Maze.ROWS):
                if self.maze[x][y] == 1:
                    self.master.canvas.create_rectangle(x*BLOCK_WIDTH, y*BLOCK_HEIGHT, x*BLOCK_WIDTH + BLOCK_WIDTH, y*BLOCK_HEIGHT + BLOCK_HEIGHT, fill= Maze.BLOCK_COLOR, outline= Maze.BLOCK_COLOR) 

    def check_collision(self, player_coords: tuple[float, float, float, float]) -> bool:
     
        for x in range(Maze.COLS):
            for y in range(Maze.ROWS):
                if self.maze[x][y] == 1:
                    block_coords = x*BLOCK_WIDTH, y*BLOCK_HEIGHT, x*BLOCK_WIDTH + BLOCK_WIDTH, y*BLOCK_HEIGHT + BLOCK_HEIGHT
                    if Maze.aabb_collision(block_coords, player_coords):
                        return True
        return False

    @staticmethod
    def aabb_collision(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
            aX0, aY0, aX1, aY1 = a
            bX0, bY0, bX1, bY1 = b
            if  (aX0 < bX1) and  (aX1 > bX0) and  (aY0 < bY1) and  (aY1 > bY0):
                return True
            return False