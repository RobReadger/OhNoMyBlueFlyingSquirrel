from enum import Enum
from pyglet import window

from core.level_context import LevelContext
from enums.game_state import GameState
from menus.game_over import GameOver
from menus.main_menu import MainMenu
from pyglet.math import Mat4

from menus.win import Win


class GameContext:
    def __init__(self, win: window.Window, levels: list[str]) -> None:
        self.game_state = GameState.MAIN_MENU
        self.current_level: LevelContext = None
        self.main_menu = MainMenu(win, self)
        self.game_over = GameOver(win, self)
        self.win_menu = Win(win, self)
        self.win = win
        self.levels = levels
        self.level_counter = -1

    def load_level(self, level_name: str) -> None:
        self.current_level = LevelContext.load_level(level_name, self.win, self)
        self.game_state = GameState.IN_GAME

    def next_level(self):
        self.level_counter += 1

        if self.level_counter == len(self.levels):
            self.game_state = GameState.WIN
            return

        self.load_level(self.levels[self.level_counter])

    def draw(self, win: window.Window, keys) -> None:
        match self.game_state:
            case GameState.MAIN_MENU:
                self.main_menu.draw()
                return
            case GameState.IN_GAME:
                if self.current_level is not None:
                    self.current_level.draw(win, keys)
                return
            case GameState.GAME_OVER:
                self.current_level = None
                win.view = Mat4().translate((0, 0, 0))
                self.game_over.draw()
                return
            case GameState.WIN:
                self.current_level = None
                win.view = Mat4().translate((0, 0, 0))
                self.win_menu.draw()
