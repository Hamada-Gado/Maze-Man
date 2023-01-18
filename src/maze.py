from collections import deque
import random
import time

class Node:

    UP: str = "up"
    DOWN: str = "down"
    LEFT: str = "left"
    RIGHT: str = "right"
    
    def __init__(self, col: int, row: int) -> None:
        self.col: int = col
        self.row: int = row
        self.connected: str = ""
        
    def __str__(self) -> str:
        return f"col, row: {(self.col, self.row)}, dir: {self.connected}"

class Maze:
    
    def __init__(self, width: int, height: int, cols: int, rows: int) -> None:
        self.width = width
        self.height = height
        self.cols = cols
        self.rows = rows
        self.maze: list[list[Node]] = [[Node(col, row) for row in range(self.rows)] for col in range(self.cols)]
        
    def get_neighbors(self, node: Node) -> dict[str, Node]:
        col, row = node.col, node.row
        candidates = [
            (Node.UP, (col, row-1)),
            (Node.DOWN, (col, row+1)),
            (Node.LEFT, (col-1, row)),
            (Node.RIGHT, (col+1, row))
        ]
        
        result: dict[str, Node] = {}
        for direction, (c, r) in candidates:
            if 0 <= r < self.rows and 0 <= c < self.cols and not self.maze[c][r].connected:
                result[direction] = self.maze[c][r]
                
        return result
        
    def create_random_maze(self):
        
        current_node: Node = random.choice(random.choice(self.maze))
        
        visited: deque[Node] = deque()
        visited.append(current_node)
        
        num_visited = 1
        
        while num_visited <= self.cols * self.rows:
            # self.print_maze()
            # print("\n\n")
            # time.sleep(1)
            current_node = visited[-1]
            neighbors: dict[str, Node] = self.get_neighbors(current_node)
            
            if neighbors == {}:
                print(current_node)
                print("poped")
                current_node = visited.pop()
                print(current_node)
                continue
            
            direction: str = random.choice(list(neighbors.keys()))
            current_node.connected = direction
            next_node: Node = neighbors[direction]
                        
            visited.append(next_node)
            num_visited += 1
            
    def print_maze(self):
        maze: list[list[str]] = [["" for _ in range(self.rows)] for _ in range(self.cols)]
        
        for c in range(self.cols):
            for r in range(self.rows):
                if self.maze[c][r].connected == Node.UP:
                    maze[c][r] = "^"
                elif self.maze[c][r].connected == Node.DOWN:
                    maze[c][r] = "|/"
                elif self.maze[c][r].connected == Node.LEFT:
                    maze[c][r] = "<-"
                elif self.maze[c][r].connected == Node.RIGHT:
                    maze[c][r] = "->"
                else:
                    maze[c][r] = "?"
                    
        for _ in range(len(maze)):
            print(maze[_])
        
        
m = Maze(600, 600, 15, 15)
m.create_random_maze()
m.print_maze()