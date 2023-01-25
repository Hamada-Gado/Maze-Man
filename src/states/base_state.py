from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

from abc import ABC, abstractmethod


class Base_State(ABC):
    
    def __init__(self, game: Game) -> None:
        self.game: Game = game
    
    @abstractmethod
    def enter(self) -> None: pass
    @abstractmethod
    def exit(self) -> None: pass
    @abstractmethod
    def update(self) -> None: pass
    @abstractmethod
    def draw(self) -> None: pass