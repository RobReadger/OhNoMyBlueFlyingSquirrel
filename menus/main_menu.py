from pyglet import text, window
from pyglet.shapes import Batch

from widgets.button import Button


class MainMenu:
    def __init__(self, win: window.Window, game_context) -> None:
        self.title_batch = Batch()
        self.title = text.Label(
            "Oh No...",
            font_name="Corbel",
            font_size=76,
            x=win.width // 2,
            y=win.height - 20,
            anchor_x="center",
            anchor_y="top",
            batch=self.title_batch,
        )
        self.title2 = text.Label(
            "My Blue Flying Squirrel",
            font_name="Corbel",
            font_size=76,
            x=win.width // 2,
            y=win.height - 120,
            anchor_x="center",
            anchor_y="top",
            batch=self.title_batch,
        )
        self.play_button = Button(
            label="Play",
            x=win.width // 2,
            y=win.height // 2,
            width=300,
            height=100,
            font_size=50,
            on_press=self.play,
            color=(100, 100, 100),
        )
        self.game_context = game_context

    def draw(self) -> None:
        self.title_batch.draw()
        self.play_button.draw()

    def play(self) -> None:
        self.game_context.load_level("level_4.json")
