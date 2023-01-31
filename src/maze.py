from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from constants import Direction, CELL_WIDTH, CELL_HEIGHT, COLUMNS, ROWS

pg.init()

if TYPE_CHECKING:
    from states.play_state import Play_State

import random
from collections import deque


class Cell:
    def __init__(self, row: int, col: int) -> None:
        self.row: int = row
        self.col: int = col
        self.visited: bool = False
        self.connected: dict[Direction, Cell] = dict()
        
    def __repr__(self) -> str:
        return f"|row, col: {(self.row, self.col)} dir: {self.connected.keys()}|"

class Maze:
    
    def __init__(self, master: Play_State, cols: int = COLUMNS, rows: int = ROWS) -> None:
        self.master: Play_State = master
        self.cols: int = cols
        self.rows: int = rows
        self.maze: list[list[Cell]] = [[Cell(row, col) for col in range(self.cols)] for row in range(self.rows)]
        
        self.create_random_maze()
        self.load_walls()
        self.create_walls()
        
    def load_walls(self):
        self.wallV: pg.surface.Surface = pg.image.load("../res/images/wall.png").convert_alpha()
        self.wallH: pg.surface.Surface = pg.transform.rotate(surface= self.wallV, angle= 90).convert_alpha()
        
    def create_walls(self):
        self.walls: dict[tuple[int, int, str], pg.rect.Rect] = dict()
        
        r = c = num_walls = 0
        
        while num_walls < (self.rows + 1) * self.cols:
            rectH: pg.rect.Rect = self.wallH.get_rect()
            rectH.topleft = (c*CELL_WIDTH, r*CELL_HEIGHT)
            self.walls[r, c, "H"] = rectH
            
            num_walls += 1
            c += 1
        
            if c >= self.cols:
                c = 0
                r += 1
            
        r = c = num_walls = 0
        while num_walls < (self.cols + 1) * self.rows:
            rectV: pg.rect.Rect = self.wallV.get_rect()
            rectV.topleft = (c*CELL_WIDTH, r*CELL_HEIGHT)
            self.walls[r, c, "V"] = rectV
            
            num_walls += 1
            r += 1
            
            if r >= self.cols:
                r = 0
                c += 1
            
        for r in range(self.rows):
            for c in range(self.cols):
                if Direction.UP in self.maze[r][c].connected.keys():
                    self.walls.pop((r, c, "H"))
                if Direction.DOWN in self.maze[r][c].connected.keys():
                    self.walls.pop((r+1, c, "H"))
                if Direction.LEFT in self.maze[r][c].connected.keys():
                    self.walls.pop((r, c, "V"))
                if Direction.RIGHT in self.maze[r][c].connected.keys():
                    self.walls.pop((r, c+1, "V"))

    def get_neighbors(self, Cell: Cell) -> dict[Direction, Cell]:
        row, col = Cell.row, Cell.col
        candidates: list[tuple[Direction, tuple[int, int]]] = [
            (Direction.UP, (row-1, col)),
            (Direction.DOWN, (row+1, col)),
            (Direction.LEFT, (row, col-1)),
            (Direction.RIGHT, (row, col+1))
        ]
        
        result: dict[Direction, Cell] = {}
        for direction, (r, c) in candidates:
            if 0 <= r < self.rows and 0 <= c < self.cols and not self.maze[r][c].visited :
                result[direction] = self.maze[r][c]
                
        return result
     
    def create_random_maze(self):
        
        current_Maze_Node: Cell = random.choice(random.choice(self.maze))
        
        visited: deque[Cell] = deque()
        visited.append(current_Maze_Node)
        
        num_visited = 1
        
        while num_visited < self.cols * self.rows: 
            current_Maze_Node.visited = True
            neighbors: dict[Direction, Cell] = self.get_neighbors(current_Maze_Node)
            
            if neighbors == {}:
                current_Maze_Node = visited.pop()
                continue
            
            direction: Direction = random.choice(list(neighbors.keys()))
            current_Maze_Node.connected[direction] = neighbors[direction]
            current_Maze_Node = neighbors[direction]

            visited.append(current_Maze_Node)
            num_visited += 1
        
        current_Maze_Node.visited = True 
    
    def draw(self): 
        # draw walls
        for (_, _, orientation), rect in self.walls.items():
            if orientation == "H":
                self.master.game.window.blit(self.wallH, rect)
            else:
                self.master.game.window.blit(self.wallV, rect)

    