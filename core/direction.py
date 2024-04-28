from enum import Enum

import numpy as np


class Direction(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def get(self) -> np.array:
        return np.array(self.value)
