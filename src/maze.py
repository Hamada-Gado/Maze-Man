from collections import deque
import random

class Node:

    UP: tuple[int, int] = (1, 0)
    DOWN: tuple[int, int] = (-1, 0)
    LEFT: tuple[int, int] = (0, -1)
    RIGHT: tuple[int, int] = (0, 1)
    
    def __init__(self, row: int, col: int) -> None:
        self.col: int = col
        self.row: int = row
        self.visited: bool = False
        self.connected: list[tuple[int, int]] = list()
        
    def __repr__(self) -> str:
        return f"|row, col: {(self.row, self.col)}, dir: {self.connected}|"

class Maze:
    
    def __init__(self, cols: int, rows: int) -> None:
        self.cols: int = cols
        self.rows: int = rows
        self.maze: list[list[Node]] = [[Node(row, col) for col in range(self.cols)] for row in range(self.rows)]
        
        #! should be removed
        self.current_node: Node = random.choice(random.choice(self.maze))
        
        self.visited: deque[Node] = deque()
        self.visited.append(self.current_node)
        
        self.num_visited = 1
        
    def get_neighbors(self, node: Node) -> dict[tuple[int, int], Node]:
        col, row = node.col, node.row
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
      
    #! should be removed
    def _create_random_maze(self):
        if self.num_visited >= self.cols * self.rows:
            return
        
        self.current_node.visited = True
        neighbors: dict[tuple[int, int], Node] = self.get_neighbors(self.current_node)
        
        if neighbors == {}:
            self.current_node = self.visited.pop()
            return
        
        direction: tuple[int, int] = random.choice(list(neighbors.keys()))
        self.current_node.connected.append(direction)
        self.current_node = neighbors[direction]
                    
        self.visited.append(self.current_node)
        self.num_visited += 1