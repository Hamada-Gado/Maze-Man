from __future__ import annotations
from queue import PriorityQueue

from typing import TYPE_CHECKING

from constants import Direction

if TYPE_CHECKING:
    from game import Game
    from maze import Maze, Maze_Node

class Ai:
    
    def __init__(self, master: Game) -> None:
        self.master: Game = master
        self.path: list[tuple[str, tuple[int, int]]] = list()
        self.a_star: A_Star = A_Star(self.master.maze, tuple(), tuple())
        
class Ai_Node:
    
    def __init__(self, state: Maze_Node, target: tuple[int, int], parent: Ai_Node | None, action: Direction) -> None:
        self.state: Maze_Node = state
        self.target: tuple[int, int] = target
        self.parent: Ai_Node | None = parent
        self.steps: int = 0 if parent is None else (parent.steps + 1)
        self.action: Direction = action
    
    def cost(self) -> int:
        return self.steps
        
    def heuristic(self) -> int:
        return abs(self.state.row - self.target[0]) + abs(self.state.col - self.target[1])
    
    def evaluation(self) -> int: # evaluation function
        return self.cost() + self.heuristic()

    def __lt__(self, other: Ai_Node) -> bool:
        return self.evaluation() < other.evaluation()
        
class A_Star:
    
    def __init__(self, maze: Maze, target: tuple[int, int], agent: tuple[int, int]) -> None:
        self.maze: Maze = maze
        self.target: tuple[int, int] = target
        self.agent: tuple[int, int] = agent
    
    def neighbors(self, state: Maze_Node) -> list[tuple[Direction, Maze_Node]]:
        row, col = state.row, state.col
        candidates: list[tuple[Direction, tuple[int, int]]] = [
            (Direction.UP, (row-1, col)),
            (Direction.DOWN, (row+1, col)),
            (Direction.LEFT, (row, col-1)),
            (Direction.RIGHT, (row, col+1))
        ]

        result: list[tuple[Direction, Maze_Node]] = []
        for action, (r, c) in candidates:
            if 0 <= r < self.maze.rows and 0 <= c < self.maze.cols and action in self.maze.maze[r][c].connected:
                result.append((action, self.maze.maze[r][c]))
        return result
    
    def solve(self):
        self.num_explored: int = 0
        
        start: Ai_Node = Ai_Node(state= self.maze.maze[self.agent[0]][self.agent[1]], target= self.target, parent= None, action= Direction.NONE)
        frontier: PriorityQueue = PriorityQueue(0)
        frontier.put(start, block= False)
        
        self.explored: set = set()
        
        while True:
            
            if frontier.empty():
                raise Exception("No solution")
            
            node: Ai_Node = frontier.get(block= False)
            self.num_explored += 1
            
            if (node.state.row, node.state.col) == self.target:
                actions: list[Direction] = []
                cells: list[Maze_Node] = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                
                actions.reverse()
                cells.reverse()
                
                return actions, cells
            
            self.explored.add(node.state)
        
            for action, state in self.neighbors(node.state):
                if state not in self.explored:
                    child = Ai_Node(state= state, target= self.target, parent= node, action= action)
                    frontier.put(child)