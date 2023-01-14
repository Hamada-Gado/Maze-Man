from __future__ import annotations
from typing import TYPE_CHECKING

from coordinate import Coordinate
if TYPE_CHECKING:
    from game import Game

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
