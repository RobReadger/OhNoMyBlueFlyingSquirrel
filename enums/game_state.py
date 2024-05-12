from enum import Enum


class GameState(Enum):
    MAIN_MENU = 1
    IN_GAME = 2
    GAME_OVER = 3
    WIN = 4
