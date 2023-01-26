from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

from abc import ABC, abstractmethod
import pygame as pg


class Base_State(ABC):
    
    def __init__(self, game: Game) -> None:
        self.game: Game = game
    
    @abstractmethod
    def update(self) -> None: pass
    @abstractmethod
    def draw(self) -> None: pass
    @abstractmethod
    def event_handler(self, event: pg.event.Event) -> None: pass
    @abstractmethod
    def enter(self) -> None: pass
    @abstractmethod
    def exit(self) -> None: pass