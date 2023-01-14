import random

from constants import HEIGHT, WIDTH


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
        if self._x0 > WIDTH:
            self._x0 = 0
            self._x1 = self._x0 + self._width
        
        elif self._x0 < -self._width:
            self._x0 = WIDTH
            self._x1 = self._x0 + self._width

        elif self._y0 > HEIGHT:
            self._y0 = 0
            self._y1 = self._y0 + self._height

        elif self._y0 < -self._height:
            self._y0 = HEIGHT
            self._y1 = self._y0 + self._height

    def set_random_position(self) -> None:
        self._x0 = random.randint(0, WIDTH - self._width)
        self._y0 = random.randint(0, HEIGHT - self._height)
        self._x1 = self._x0 + self._width
        self._y1 = self._y0 + self._height

    @property
    def position(self) -> tuple[float, float, float, float]:
        return (self._x0, self._y0, self._x1, self._y1)

