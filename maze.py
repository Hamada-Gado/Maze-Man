class Maze:
    BLOCK_WIDTH: int = 15 
    BLOCK_HEIGHT: int = 15
    COLS: int = Game.WIDTH//BLOCK_WIDTH # 40
    ROWS: int = Game.HEIGHT//BLOCK_HEIGHT # 40
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
        self.master.canvas.create_rectangle(0, 0, Game.WIDTH, Game.HEIGHT, fill= Maze.BG_COLOR)
        for x in range(Maze.COLS):
            for y in range(Maze.ROWS):
                if self.maze[x][y] == 1:
                    self.master.canvas.create_rectangle(x*Maze.BLOCK_WIDTH, y*Maze.BLOCK_HEIGHT, x*Maze.BLOCK_WIDTH + Maze.BLOCK_WIDTH, y*Maze.BLOCK_HEIGHT + Maze.BLOCK_HEIGHT, fill= Maze.BLOCK_COLOR, outline= Maze.BLOCK_COLOR) 

    def check_collision(self, player_coords: tuple[float, float, float, float]) -> bool:
     
        for x in range(Maze.COLS):
            for y in range(Maze.ROWS):
                if self.maze[x][y] == 1:
                    block_coords = x*Maze.BLOCK_WIDTH, y*Maze.BLOCK_HEIGHT, x*Maze.BLOCK_WIDTH + Maze.BLOCK_WIDTH, y*Maze.BLOCK_HEIGHT + Maze.BLOCK_HEIGHT
                    if aabb_collision(block_coords, player_coords):
                        return True
        return False

def aabb_collision(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
        aX0, aY0, aX1, aY1 = a
        bX0, bY0, bX1, bY1 = b
        if  (aX0 < bX1) and  (aX1 > bX0) and  (aY0 < bY1) and  (aY1 > bY0):
            return True
        return False