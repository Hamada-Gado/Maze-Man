import time
import tkinter as tk

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

