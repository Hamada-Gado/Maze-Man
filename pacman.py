from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Callable

from coordinate import Coordinate
if TYPE_CHECKING:
    from game import Game

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
        self.move(dt)

        # draw
        self.draw()

    def move(self, dt: float) -> None:
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

