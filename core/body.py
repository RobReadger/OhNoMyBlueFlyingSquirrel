from abc import ABC
import numpy as np
from pyglet import shapes


class Body(ABC):
    def __init__(self, x, y, width, height) -> None:
        self.pos = np.array([x, y])
        self.hitbox = np.array([width, height])
        self.center = self.pos + self.hitbox / 2

    def is_colliding(self, body: "Body", offset: np.array = np.array([0, 0])) -> bool:
        return (
            self.pos[0] + offset[0] <= body.pos[0] + body.hitbox[0]
            and self.pos[0] + self.hitbox[0] + offset[0] >= body.pos[0]
            and self.pos[1] + offset[1] <= body.pos[1] + body.hitbox[1]
            and self.pos[1] + self.hitbox[1] + offset[1] >= body.pos[1]
        )

    def is_bottom_colliding(self, body: "Body", y_offset: int = 0) -> bool:
        return (
            self.pos[0] < body.pos[0] + body.hitbox[0]
            and self.pos[0] + self.hitbox[0] > body.pos[0]
            and self.pos[1] + y_offset < body.pos[1] + body.hitbox[1]
            and self.pos[1] + y_offset > body.pos[1]
        )

    def are_sides_colliding(self, body: "Body", x_offset: int = 0) -> bool:
        return (
            self.pos[0] + x_offset > body.pos[0]
            and self.pos[0] + x_offset < body.pos[0] + body.hitbox[0]
            and self.pos[1] + self.hitbox[1] / 4 < body.pos[1] + body.hitbox[1]
            and self.pos[1] + self.hitbox[1] * 3 / 4 > body.pos[1]
        ) or (
            self.pos[0] + self.hitbox[0] + x_offset > body.pos[0]
            and self.pos[0] + self.hitbox[0] + x_offset < body.pos[0] + body.hitbox[0]
            and self.pos[1] + self.hitbox[1] / 4 < body.pos[1] + body.hitbox[1]
            and self.pos[1] + self.hitbox[1] * 3 / 4 > body.pos[1]
        )

    def wall_colliding(self, body: "Body", x_offset: int = 0) -> bool:
        return

    def show_hitbox(self):
        bbox = shapes.BorderedRectangle(
            x=self.pos[0],
            y=self.pos[1],
            width=self.hitbox[0],
            height=self.hitbox[1],
            color=(0, 204, 255),
            border_color=(0, 0, 0),
            border=3,
        )

        bbox.opacity = 0
        bbox.draw()
