from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

import pygame as pg

from constants import State
from states.base_state import Base_State


class State_Machine:
    
    def __init__(self, game: Game, states: dict[State, type[Base_State]] | None = None) -> None:
        self.game: Game = game
        self.empty_state: type[Base_State] = type("Empty_State", (Base_State,), {'enter': lambda self : None, 'exit': lambda self : None, 'update': lambda self : None, 'draw': lambda self : None, 'event_handler': lambda self, event : None})
        self.states: dict[State, type[Base_State]] = states or {}
        self.current_state: Base_State = self.empty_state(self.game)
        
    def change(self, state: State, *enter_args, **enter_kwargs) -> None:
        assert(self.states[state])
        self.current_state.exit()
        self.current_state = self.states[state](self.game)
        self.current_state.enter(*enter_args, **enter_kwargs)
        
    def update(self) -> None:
        self.current_state.update()
        
    def draw(self) -> None:
        self.current_state.draw()
        
    def event_handler(self, event: pg.event.Event) -> None:
        self.current_state.event_handler(event)
