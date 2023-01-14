
from __future__ import annotations
import random
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from constants import BLOCK_HEIGHT, BLOCK_WIDTH

from coordinate import Coordinate
if TYPE_CHECKING:
    from game import Game

class Ghost(ABC):
    WIDTH: int = 20
    HEIGHT: int = 20
    SPEED: int = 120
    SCARED_COLOR: str = "#0000FF"
    EYE_OUT_COLOR: str = "white"
    EYE_IN_COLOR: str = "black"
    DIRECTION: list[str] = ["right", "left", "up", "down"]

    def __init__(self, master: Game) -> None:
        self.master: Game = master
        self.coordinate: Coordinate = Coordinate(0, 0, Ghost.WIDTH, Ghost.HEIGHT)
        while self.master.maze.check_collision(self.coordinate.position):
            self.coordinate.set_random_position()
        self.color: str = Ghost.SCARED_COLOR
        self.direction: str = "right"

    def update(self, dt: float) -> None:
        # move
        self.move(dt)

        # draw
        self.draw()

    @abstractmethod
    def move(self, dt: float) -> None:
        pass

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
        self.master.canvas.create_oval(x0 + 9, y0, x1 + 9, y1, fill= Ghost.EYE_OUT_COLOR, outline= Ghost.EYE_OUT_COLOR)

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
        self.master.canvas.create_oval(x0 + 9 +dx, y0 + dy, x1 + 9 + dx, y1 + dy, fill= Ghost.EYE_IN_COLOR, outline= Ghost.EYE_IN_COLOR)

class Red_Ghost(Ghost):
    COLOR: str = "red"

    def __init__(self, master: Game) -> None:
        super().__init__(master)
        self.color = Red_Ghost.COLOR

    def move(self, dt: float) -> None:
        from ai import A_Star
        
        x, y, _, _ = self.master.player.coordinate.position
        col_p, row_p = x//BLOCK_WIDTH, y//BLOCK_HEIGHT
        
        x, y, _, _ = self.coordinate.position
        col_g, row_g = x//BLOCK_WIDTH, y//BLOCK_HEIGHT
        
        self.ai = A_Star(self.master.maze, (int(col_p), int(row_p)), (int(col_g), int(row_g)))
        
        self.direction = self.ai.solve()
        print(self.direction)
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

    # Override
    def __move(self, dt: float) -> None:
        distanceX: float = self.master.player.coordinate.position[0] - self.coordinate.position[0]
        distanceY: float = self.master.player.coordinate.position[1] - self.coordinate.position[1]

        if distanceX > 10:
            dx = 1
        elif distanceX < -10:
            dx = -1
        else:
            dx = 0

        if distanceY > 10:
            dy = 1
        elif distanceY < -10:
            dy = -1
        else:
            dy = 0
        
        predict_position = self.coordinate.predict_move(dx * Ghost.SPEED * dt, 0)
        if not self.master.maze.check_collision(predict_position):
            self.coordinate.move(dx * Ghost.SPEED * dt, 0)

        predict_position = self.coordinate.predict_move(0, dy * Ghost.SPEED * dt)
        if not self.master.maze.check_collision(predict_position):
            self.coordinate.move(0, dy * Ghost.SPEED * dt)


class Orange_Ghost(Ghost):
    COLOR: str = "orange"

    def __init__(self, master: Game) -> None:
        super().__init__(master)
        self.color = Orange_Ghost.COLOR

    # Override
    def move(self, dt: float) -> None:
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

class Blue_Ghost(Ghost):
    COLOR: str = "cyan"

    def __init__(self, master: Game) -> None:
        super().__init__(master)
        self.color = Blue_Ghost.COLOR

    # Override
    def move(self, dt: float) -> None:
        distanceX: float = self.master.player.coordinate.position[0] - self.coordinate.position[0]
        distanceY: float = self.master.player.coordinate.position[1] - self.coordinate.position[1]

        if distanceX > 10:
            dx = 1
        elif distanceX < -10:
            dx = -1
        else:
            dx = 0

        if distanceY > 10:
            dy = 1
        elif distanceY < -10:
            dy = -1
        else:
            dy = 0
        
        predict_position = self.coordinate.predict_move(dx * Ghost.SPEED * dt, 0)
        if not self.master.maze.check_collision(predict_position) and dx != 0:
            self.coordinate.move(dx * Ghost.SPEED * dt, 0)
        else:
            predict_position = self.coordinate.predict_move(0, dy * Ghost.SPEED * dt)
            if not self.master.maze.check_collision(predict_position):
                self.coordinate.move(0, dy * Ghost.SPEED * dt)

class Pink_Ghost(Blue_Ghost):
    COLOR: str = "pink"

    def __init__(self, master: Game) -> None:
        super().__init__(master)
        self.color = Pink_Ghost.COLOR


