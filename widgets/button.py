from typing import Callable
from pyglet import window, shapes, text


class Button:
    def __init__(
        self,
        label: str,
        x: int,
        y: int,
        width: int,
        height: int,
        font_size: int,
        on_press: Callable,
        color: tuple[int, int, int],
    ) -> None:
        self.back = shapes.Rectangle(
            x - width // 2, y - height // 2, width, height, color
        )
        self.label = text.Label(
            label,
            font_name="Corbel",
            font_size=font_size,
            x=x,
            y=y + 5,
            color=(255, 255, 255, 255),
            anchor_x="center",
            anchor_y="center",
        )

    def draw(self):
        self.back.draw()
        self.label.draw()
