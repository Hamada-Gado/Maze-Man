import random
import time
import tkinter as tk
from typing import Callable

#* Classes

class Game:
    DELAY = 30
    WIDTH = 600
    HEIGHT = 600
    
    def __init__(self) -> None:
        self.root: tk.Tk = tk.Tk()
        self.canvas: tk.Canvas = tk.Canvas(self.root, width= Game.WIDTH, height= Game.HEIGHT)
        
        self.keys: dict[str, bool] = dict()
        self.root.bind('<Key>', self.key_listener)

        # setup
        self.maze: Maze = Maze(self)

        self.player: PacMan = PacMan(self)
        self.pellet: Pellet = Pellet(self)

        self.ghosts: list[Ghost] = []
        self.ghosts.append(Ghost(self, "red"))

        self.delta_time: float = 0
         
    def restart(self) -> None:
        self.maze = Maze(self)

        self.player = PacMan(self)
        self.pellet = Pellet(self)

        self.ghosts = []
        self.ghosts.append(Ghost(self, "red"))

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
        print(self.delta_time*1000) #! should be removed

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

        self.root.after(Game.DELAY, self._run)
        self.delta_time = time.time()

    def key_listener(self, event: tk.Event) -> None:
        self.keys[event.keysym] = True

    def check_game_over(self) -> bool:
        position = self.player.coordinate.position

        for ghost in self.ghosts:
            if aabb_collision(ghost.coordinate.position, position):
                print("lol again")
                return True

        return False

class Coordinate:
    def __init__(self, x: float, y: float, width: int, height: int) -> None:
        self._width: int = width
        self._height: int = height
        self._x0: float = x
        self._y0: float = y
        self._x1: float = self._x0 + self._width
        self._y1: float = self._y0 + self._height

    def predict_move(self, dx: float, dy: float) -> tuple[float, float, float, float]:
        return (self._x0 + dx, self._y0 + dy, self._x1 + dx, self._y1 + dy)

    def move(self, dx: float, dy: float) -> None:
        self._x0 += dx
        self._y0 += dy
        self._x1 = self._x0 + self._width
        self._y1 = self._y0 + self._height

        # to wrap-around the boundaries
        if self._x0 > Game.WIDTH:
            self._x0 = 0
            self._x1 = self._x0 + self._width
        
        elif self._x0 < -self._width:
            self._x0 = Game.WIDTH
            self._x1 = self._x0 + self._width

        elif self._y0 > Game.HEIGHT:
            self._y0 = 0
            self._y1 = self._y0 + self._height

        elif self._y0 < -self._height:
            self._y0 = Game.HEIGHT
            self._y1 = self._y0 + self._height

    def set_random_position(self) -> None:
        self._x0 = random.randint(0, Game.WIDTH - self._width)
        self._y0 = random.randint(0, Game.HEIGHT - self._height)
        self._x1 = self._x0 + self._width
        self._y1 = self._y0 + self._height

    @property
    def position(self) -> tuple[float, float, float, float]:
        return (self._x0, self._y0, self._x1, self._y1)

class Maze:
    BLOCK_WIDTH: int = 15 
    BLOCK_HEIGHT: int = 15
    COLS: int = Game.WIDTH//BLOCK_WIDTH # 20
    ROWS: int = Game.HEIGHT//BLOCK_HEIGHT # 20
    BG_COLOR: str = "black"
    BLOCK_COLOR: str = "blue"

    def __init__(self, master: Game) -> None:
        self.master: Game = master
        self.maze: list[list[int]] = [[0 for y in range(Maze.ROWS)] for x in range(Maze.COLS)]
        self.make_maze()

    def make_maze(self) -> None:
        for x in range(0, -2, -1):
            for y in range(Maze.ROWS):
                self.maze[x][y] = 1
        
        for x in range(Maze.COLS):
            for y in range(0, -2, -1):
                self.maze[x][y] = 1

        self.maze[5][-1] = 0
        self.maze[6][-1] = 0
        self.maze[5][0] = 0
        self.maze[6][0] = 0
    
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

class PacMan:
    WIDTH: int = 20
    HEIGHT: int = 20
    SPEED: int = 100
    COLOR: str = "yellow"

    def __init__(self, master: Game) -> None:
        self.master: Game = master
        self.coordinate: Coordinate = Coordinate(0, 0, PacMan.WIDTH, PacMan.HEIGHT)
        while self.master.maze.check_collision(self.coordinate.position):
            self.coordinate.set_random_position()
        self.angle: int = 0
        self.frames_timer: float = 0
        self.current_frame: int = 0
        self.frames: list[Callable] = [self._frame1, self._frame2, self._frame3]

    def update(self, dt: float) -> None:
        # move
        if self.master.keys.get("Right", False):
            predicted_position = self.coordinate.predict_move(PacMan.SPEED * dt, 0)
            if not self.master.maze.check_collision(predicted_position):
                self.coordinate.move(PacMan.SPEED * dt, 0)
            self.angle = 0

        elif self.master.keys.get("Left", False):
            predict_position = self.coordinate.predict_move(-PacMan.SPEED * dt, 0)
            if not self.master.maze.check_collision(predict_position):
                self.coordinate.move(-PacMan.SPEED * dt, 0)
            self.angle = 180

        elif self.master.keys.get("Down", False):
            predict_position = self.coordinate.predict_move(0, PacMan.SPEED * dt)
            if not self.master.maze.check_collision(predict_position):
                self.coordinate.move(0, PacMan.SPEED * dt)
            self.angle = 270

        elif self.master.keys.get("Up", False):
            predict_position = self.coordinate.predict_move(0, -PacMan.SPEED * dt)
            if not self.master.maze.check_collision(predict_position):
                self.coordinate.move(0, -PacMan.SPEED * dt)
            self.angle = 90

        self.frames_timer += dt

        # draw
        self.draw()

    def draw(self) -> None:
        if self.frames_timer > 0.1:
            self.current_frame += 1
            if self.current_frame == len(self.frames):
                self.current_frame = 0
            self.frames_timer = 0
        self.frames[self.current_frame]()

    def _frame1(self) -> None:
        self.master.canvas.create_oval(self.coordinate.position, fill= PacMan.COLOR, outline= PacMan.COLOR)
        
    def _frame2(self) -> None:
        self.master.canvas.create_arc(self.coordinate.position, start= 30 + self.angle, extent= 300, fill= PacMan.COLOR, outline= PacMan.COLOR)
                
    def _frame3(self) -> None:
        self.master.canvas.create_arc(self.coordinate.position, start= 60 + self.angle, extent= 240, fill= PacMan.COLOR, outline= PacMan.COLOR)

class Pellet:
    WIDTH: int = 7
    HEIGHT: int = 7
    COLOR: str = "blue"

    def __init__(self, master: Game) -> None:
        self.master: Game = master
        self.coordinate: Coordinate = Coordinate(0, 0, Pellet.WIDTH, Pellet.HEIGHT)
        while self.master.maze.check_collision(self.coordinate.position):
            self.coordinate.set_random_position()
 

    def update(self) -> None:
        # draw
        self.draw()

    def draw(self) -> None:
        self.master.canvas.create_oval(self.coordinate.position, fill= Pellet.COLOR, outline= Pellet.COLOR)

class Ghost:
    WIDTH: int = 20
    HEIGHT: int = 20
    SPEED: int = 150
    EYE_OUT_COLOR: str = "white"
    EYE_IN_COLOR: str = "black"
    DIRECTION: list[str] = ["right", "left", "up", "down"]

    def __init__(self, master: Game, color) -> None:
        self.master: Game = master
        self.coordinate: Coordinate = Coordinate(0, 0, Ghost.WIDTH, Ghost.HEIGHT)
        while self.master.maze.check_collision(self.coordinate.position):
            self.coordinate.set_random_position()
        self.color: str = color
        self.direction: str = "right"

    def update(self, dt: float) -> None:
        # move
        random.shuffle(Ghost.DIRECTION)
        if self.direction == "right":
            predict_position = self.coordinate.predict_move(Ghost.SPEED * dt, 0)
            if self.master.maze.check_collision(predict_position):
                self.direction = Ghost.DIRECTION[0]
            else:
                self.coordinate.move(Ghost.SPEED*dt, 0)
        
        elif self.direction == "left":
            predict_position = self.coordinate.predict_move(-Ghost.SPEED * dt, 0)
            if self.master.maze.check_collision(predict_position):
                self.direction = Ghost.DIRECTION[0]
            else:
                self.coordinate.move(-Ghost.SPEED*dt, 0)
        
        elif self.direction == "down":
            predict_position = self.coordinate.predict_move(0, Ghost.SPEED * dt)
            if self.master.maze.check_collision(predict_position):
                self.direction = Ghost.DIRECTION[0]
            else:
                self.coordinate.move(0, Ghost.SPEED*dt)

        elif self.direction == "up":
            predict_position = self.coordinate.predict_move(0, -Ghost.SPEED * dt)
            if self.master.maze.check_collision(predict_position):
                self.direction = Ghost.DIRECTION[0]
            else:
                self.coordinate.move(0, -Ghost.SPEED*dt)   

        # draw
        self.draw()

    def draw(self) -> None:
        self._draw_head()
        self._draw_body()
        self._draw_eyes()

    def _draw_head(self) -> None:
        self.master.canvas.create_arc(self.coordinate.position, start= 0, extent= 180, fill= self.color, outline= self.color)


    def _draw_body(self) -> None:
        x0, y0, x1, y1 = self.coordinate.position
        self.master.canvas.create_rectangle(x0, y0 + 10, x1, y1, fill= self.color, outline= self.color)

    def _draw_eyes(self) -> None:
        x0, y0, x1, y1 = self.coordinate.position
        x0 += 3
        y0 += 3
        x1 = x0 + 5
        y1 = y0 + 5
        self.master.canvas.create_oval(x0, y0, x1, y1, fill= Ghost.EYE_OUT_COLOR, outline= Ghost.EYE_OUT_COLOR)
        self.master.canvas.create_oval(x0 + 8, y0, x1 + 8, y1, fill= Ghost.EYE_OUT_COLOR, outline= Ghost.EYE_OUT_COLOR)

        if self.direction == "right":
            dx = 1
            dy = 0
        elif self.direction == "left":
            dx = -1
            dy = 0
        elif self.direction == "down":
            dx = 0
            dy = 1
        else:
           dx = 0
           dy = -1

        self.master.canvas.create_oval(x0 + dx, y0 + dy, x1 + dx, y1 + dy, fill= Ghost.EYE_IN_COLOR, outline= Ghost.EYE_IN_COLOR)
        self.master.canvas.create_oval(x0 + 8 +dx, y0 + dy, x1 + 8 + dx, y1 + dy, fill= Ghost.EYE_IN_COLOR, outline= Ghost.EYE_IN_COLOR)

#* Utilities functions
def aabb_collision(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
        aX0, aY0, aX1, aY1 = a
        bX0, bY0, bX1, bY1 = b
        if  (aX0 < bX1) and  (aX1 > bX0) and  (aY0 < bY1) and  (aY1 > bY0):
            return True
        return False

if __name__ == '__main__':
    game = Game()
    game.run() 