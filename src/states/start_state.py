from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

import pygame as pg
import pygame_gui as pgg

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, State
from states.base_state import Base_State


class Start_State(Base_State):
    # TODO: add themes for label (title) and buttons (play, quit)
    
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        
        self.manager: pgg.UIManager = pgg.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), enable_live_theme_updates= False)

        # title label
        pgg.elements.UILabel(
            relative_rect= pg.Rect((0, 10), (100, 54)),
            text= "PAC-MAN", manager= self.manager,
            anchors= {
                'centerx': 'centerx',
            }
        )

        self.play_button: pgg.elements.UIButton = pgg.elements.UIButton(
            relative_rect= pg.Rect((0, 0), (100, 54)),
            text= "PLAY", manager= self.manager,
            anchors= {
                'center': 'center'
            }
        )
        
        self.quit_button : pgg.elements.UIButton = pgg.elements.UIButton(
            relative_rect= pg.Rect((0, 54), (100, 54)),
            text= "QUIT", manager= self.manager,
            anchors= {
                'center': 'center',
                'top_target': self.play_button
            }
        )
        
    def update(self) -> None:
        self.manager.update(self.game.delta_time)
        
    def draw(self) -> None:
        self.manager.draw_ui(self.game.window)
                
    def event_handler(self, event: pg.event.Event) -> None:
        self.manager.process_events(event)
        if event.type == pgg.UI_BUTTON_PRESSED:
            if event.ui_element == self.play_button:
                self.game.state_machine.change(State.PLAY_STATE)
            elif event.ui_element == self.quit_button:
                self.game.terminate()
        
    def exit(self) -> None:
        return super().exit()
    def enter(self) -> None:
        return super().enter()