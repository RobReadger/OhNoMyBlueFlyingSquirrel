from pyglet import shapes
from pyglet.graphics import Batch

from core.body import Body


class Block(Body):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: tuple[int, int, int],
    ) -> None:
        super().__init__(x, y, width, height)
        self.color = color
        self.rect = None

    def add_to_batch(self, batch: Batch) -> None:
        self.rect = shapes.Rectangle(
            x=self.pos[0],
            y=self.pos[1],
            width=self.hitbox[0],
            height=self.hitbox[1],
            color=self.color,
            batch=batch,
        )

    def __str__(self) -> str:
        return f"pos: {self.pos}, shape: {self.hitbox}"
