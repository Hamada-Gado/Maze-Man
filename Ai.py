from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from maze import Maze
from queue import PriorityQueue
from constants import WIDTH, HEIGHT

class Node:
    target: tuple[int, int]
    
    def __init__(self, state: tuple[int, int], parent: Node | None, action) -> None:
        self.state = state
        self.parent = parent
        self.steps = 0 if parent is None else (parent.steps + 1)
        self.action = action

    def cost(self) -> int: # cost function
        return self.steps
        
    def heuristic(self) -> int: # heuristic function
        return abs(self.state[0] - self.target[0]) + abs(self.state[1] - self.target[1])
    
    def evaluation(self) -> int: # evaluation function
        return self.cost() + self.heuristic()

    def __lt__(self, other: Node) -> bool:
        return self.evaluation() < other.evaluation()

class A_Star:
    
    def __init__(self, maze: Maze, target: tuple[int, int], agent: tuple[int, int]) -> None:
        self.maze = maze
        Node.target = target
        self.target = target
        self.agent = agent
    
    def neighbors(self, state: tuple[int, int]):
        col, row = state
        candidates = [
            ("up", (col, row-1)),
            ("down", (col, row+1)),
            ("left", (col-1, row)),
            ("right", (col+1, row))
        ]

        result = []
        for action, (c, r) in candidates:
            if 0 <= r < HEIGHT and 0 <= c < WIDTH and not self.maze.maze[c][r]:
                result.append((action, (c, r)))
        return result
    
    def solve(self) -> str: # tuple[str, tuple[int, int]]:
        self.num_explored: int = 0
        
        start: Node = Node(state= self.agent, parent= None, action= None)
        frontier: PriorityQueue = PriorityQueue(0)
        frontier.put(start, block= False)
        
        self.explored: set = set()
        
        while True:
            
            if frontier.empty():
                raise Exception("No solution")
            
            node: Node = frontier.get(block= False)
            self.num_explored += 1
            
            if node.state == self.target:
                actions: list[str] = []
                cells: list[tuple[int, int]] = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                
                return actions[-1]
            
            self.explored.add(node.state)
        
            for action, state in self.neighbors(node.state):
                if state not in self.explored:
                    child = Node(state= state, parent= node, action= action)
                    frontier.put(child)
                    