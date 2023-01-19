from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from constants import GAME_OBJECT_WIDTH, GAME_OBJECT_HEIGHT, COLUMNS, ROWS

pg.init()

if TYPE_CHECKING:
    from game import Game

import random
from collections import deque


class Node:

    UP: tuple[int, int] = (1, 0)
    DOWN: tuple[int, int] = (-1, 0)
    LEFT: tuple[int, int] = (0, -1)
    RIGHT: tuple[int, int] = (0, 1)
    
    def __init__(self, row: int, col: int) -> None:
        self.row: int = row
        self.col: int = col
        self.visited: bool = False
        self.connected: list[tuple[int, int]] = list()
        
    def __repr__(self) -> str:
        return f"|row, col: {(self.row, self.col)}, dir: {self.connected}|"

class Maze:
    
    def __init__(self, master: Game, cols: int = COLUMNS, rows: int = ROWS) -> None:
        self.master: Game = master
        self.cols: int = cols
        self.rows: int = rows
        self.maze: list[list[Node]] = [[Node(row, col) for col in range(self.cols)] for row in range(self.rows)]
        self.create_random_maze()
        self.load_walls()
        
    def load_walls(self):
        self.wallV: pg.surface.Surface = pg.image.load("../res/wall.png").convert_alpha()
        self.wallH: pg.surface.Surface = pg.transform.rotate(surface= self.wallV, angle= 90).convert_alpha()
       
        self.create_walls()
        
    def create_walls(self):
        self.walls: dict[tuple[int, int, int], tuple[str, pg.rect.Rect]] = dict()
        
        r, c = 0, 0
        num_walls = 0
        
        while num_walls < (self.rows + 1) * self.cols:
            rectH: pg.rect.Rect = self.wallH.get_rect()
            rectH.topleft = (c*GAME_OBJECT_WIDTH, r*GAME_OBJECT_HEIGHT)
            self.walls[r, c, 0] = (("H", rectH))
            
            num_walls += 1
            c += 1
        
            if c >= self.cols:
                c = 0
                r += 1
            
        r, c = 0, 0
        num_walls = 0
        while num_walls < (self.cols + 1) * self.rows:
            rectV: pg.rect.Rect = self.wallV.get_rect()
            rectV.topleft = (c*GAME_OBJECT_WIDTH, r*GAME_OBJECT_HEIGHT)
            self.walls[r, c, 1] = (("V" , rectV))           
            
            num_walls += 1
            r += 1
            
            if r >= self.cols:
                r = 0
                c += 1
            
        for r in range(self.rows):
            for c in range(self.cols):
                if (1, 0) in self.maze[r][c].connected:
                    self.walls.pop((r, c, 0))
                if (-1, 0) in self.maze[r][c].connected:
                    self.walls.pop((r+1, c, 0))
                if (0, -1) in self.maze[r][c].connected:
                    self.walls.pop((r, c, 1))
                if (0, 1) in self.maze[r][c].connected:
                    self.walls.pop((r, c+1, 1))

    def get_neighbors(self, node: Node) -> dict[tuple[int, int], Node]:
        row, col = node.row, node.col
        candidates = [
            (Node.UP, (row-1, col)),
            (Node.DOWN, (row+1, col)),
            (Node.LEFT, (row, col-1)),
            (Node.RIGHT, (row, col+1))
        ]
        
        result: dict[tuple[int, int], Node] = {}
        for direction, (r, c) in candidates:
            if 0 <= r < self.rows and 0 <= c < self.cols and not self.maze[r][c].visited :
                result[direction] = self.maze[r][c]
                
        return result
     
    def create_random_maze(self):
        
        current_node: Node = random.choice(random.choice(self.maze))
        
        visited: deque[Node] = deque()
        visited.append(current_node)
        
        num_visited = 1
        
        while num_visited < self.cols * self.rows: 
            current_node.visited = True
            neighbors: dict[tuple[int, int], Node] = self.get_neighbors(current_node)
            
            if neighbors == {}:
                current_node = visited.pop()
                continue
            
            direction: tuple[int, int] = random.choice(list(neighbors.keys()))
            current_node.connected.append(direction)
            current_node = neighbors[direction]

            visited.append(current_node)
            num_visited += 1
        
        current_node.visited = True
     
    def update(self):
        pass
    
    def draw(self):
       
        # draw walls
        for orientation, rect in self.walls.values():
            if orientation == "H":
                self.master.window.blit(self.wallH, rect)
            else:
                self.master.window.blit(self.wallV, rect)

    