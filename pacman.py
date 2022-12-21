import time
import tkinter as tk
from typing import Callable

#* Classes
class Game():
    FPS = 60
    
    def __init__(self) -> None:
        self.root: tk.Tk = tk.Tk()
        self.canvas: tk.Canvas = tk.Canvas(self.root, width=600, height=600)
        self.player: PacMan = PacMan(self)
        self.keys: dict[str, bool] = dict()
        self.root.bind('<Key>', self.key_listener)
        self.time: float = 0 #? should be removed

    def run(self) -> None:
        self.canvas.pack()
        self.root.title("Pac-Man")
        self.root.after(0, self._run)
        self.time = time.time() #? should be removed

        self.root.mainloop()

    def _run(self) -> None:
        # print(time.time() - self.time) #? should be removed
        self.time = time.time() #? should be removed
        self.canvas.delete("all")
        self.player.update()
        self.keys = dict()
        self.root.after(Game.FPS, self._run)

    def key_listener(self, event: tk.Event) -> None:
        print(event.keysym) #? should be removed
        self.keys[event.keysym] = True

class PacMan():
    WIDTH: int = 25
    HEIGHT: int = 25
    SPEED: int = 5

    def __init__(self, master: Game) -> None:
        self.master: Game = master
        self.x0: int = 10
        self.y0: int = 10
        self.x1: int = self.x0 + PacMan.WIDTH
        self.y1: int = self.y0 + PacMan.HEIGHT
        self.color: str = "yellow"
        self.angle = 0
        self.draw: Callable = self._draw1

    def update(self) -> None:
        # move
        if self.master.keys.get("Right", False):
            self.x0 += PacMan.SPEED
            self.x1: int = self.x0 + PacMan.WIDTH
            self.angle = 0

        elif self.master.keys.get("Left", False):
            self.x0 -= PacMan.SPEED
            self.x1: int = self.x0 + PacMan.WIDTH
            self.angle = 180

        elif self.master.keys.get("Up", False):
            self.y0 -= PacMan.SPEED
            self.y1 = self.y0 + PacMan.HEIGHT
            self.angle = 90

        elif self.master.keys.get("Down", False):
            self.y0 += PacMan.SPEED
            self.y1 = self.y0 + PacMan.HEIGHT
            self.angle = 270

        # to wrap-around the boundaries
        if self.x0 > self.master.canvas.winfo_width():
            self.x0 = 0
            self.x1: int = self.x0 + PacMan.WIDTH
        
        elif self.x0 < -PacMan.WIDTH:
            self.x0 = self.master.canvas.winfo_width()
            self.x1: int = self.x0 + PacMan.WIDTH

        elif self.y0 > self.master.canvas.winfo_height():
            self.y0 = 0
            self.y1: int = self.y0 + PacMan.HEIGHT

        elif self.y0 < -PacMan.HEIGHT:
            self.y0 = self.master.canvas.winfo_height()
            self.y1: int = self.y0 + PacMan.HEIGHT

        # draw
        self.draw()

    def _draw1(self) -> None:
        self.master.canvas.create_oval(self.x0, self.y0, self.x1, self.y1, fill= self.color)
        self.draw = self._draw2
        
    def _draw2(self) -> None:
        self.master.canvas.create_arc((self.x0, self.y0, self.x1, self.y1), start= 30 + self.angle, extent= 300, fill= self.color)
        self.draw = self._draw3
        
    def _draw3(self) -> None:
        self.master.canvas.create_arc((self.x0, self.y0, self.x1, self.y1), start= 60 + self.angle, extent= 240, fill= self.color)
        self.draw = self._draw1

if __name__ == '__main__':
    game = Game()
    game.run() 