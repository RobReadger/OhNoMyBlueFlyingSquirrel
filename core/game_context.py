from enum import Enum

from core.level_context import LevelContext


class GameState(Enum):
    MAIN_MENU = 1
    IN_GAME = 2
    GAME_OVER = 3


class GameContext:
    def __init__(self) -> None:
        self.game_state = GameState.MAIN_MENU
        self.current_level: LevelContext = None

    def load_level(self, level_name: str) -> None:
        self.current_level = LevelContext.load_level(level_name)
        self.game_state = GameState.IN_GAME
