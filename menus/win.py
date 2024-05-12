from pyglet import text, window


class Win:
    def __init__(self, win: window.Window, game_context) -> None:

        self.title = text.Label(
            "You Won!",
            font_name="Corbel",
            font_size=76,
            x=win.width // 2,
            y=win.height - 50,
            anchor_x="center",
            anchor_y="top",
        )

        self.game_context = game_context

    def draw(self) -> None:
        self.title.draw()
