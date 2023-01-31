from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

import pygame as pg
import pygame_gui as pgg

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, State
from states.base_state import Base_State

class Score_State(Base_State):
    
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        
        self.manager: pgg.UIManager = pgg.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "../res/themes/theme.json", enable_live_theme_updates= True)
        
        
    def init(self, score: int) -> None:
        
        score_text: str = f"Score: {score*11}"
        
        # score
        pgg.elements.UILabel(
            relative_rect= pg.Rect((0, 10), (-1, -1)),
            text= score_text, manager= self.manager,
            object_id= "title_label",
            anchors= {
                'centerx': 'centerx',
                'top': 'top',
            } 
        )
        
        self.main_menu_button: pgg.elements.UIButton = pgg.elements.UIButton(
            relative_rect= pg.Rect((0, 0), (-1, -1)),
            text= "MAIN MENU", manager= self.manager,
            object_id= "button",
            anchors= {
                'center': 'center'
            }
        )
        
        self.quit_button : pgg.elements.UIButton = pgg.elements.UIButton(
            relative_rect= pg.Rect((0, self.main_menu_button.relative_rect.height + 10), (-1, -1)),
            text= "QUIT", manager= self.manager,
            object_id= "button",
            anchors= {
                'center': 'center',
                'top_target': self.main_menu_button
            }
        )
        
    
    def enter(self, score: int) -> None:
        self.init(score)
        
    def exit(self) -> None:
        return super().exit()
    
    def update(self) -> None:
        self.manager.update(self.game.delta_time)
        
    def draw(self) -> None:
        self.game.window.fill("#12c4ff")
        self.manager.draw_ui(self.game.window)
                
    def event_handler(self, event: pg.event.Event) -> None:
        self.manager.process_events(event)
        if event.type == pgg.UI_BUTTON_PRESSED:
            if event.ui_element == self.main_menu_button:
                self.game.state_machine.change(State.START_STATE)
            elif event.ui_element == self.quit_button:
                self.game.terminate()