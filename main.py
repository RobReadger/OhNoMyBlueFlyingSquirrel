import os
from pyglet import app, window
from core.game_context import GameContext
from pyglet.window import key


width = 1280
height = 720


win = window.Window(
    width=width, height=height, caption="Oh No My Blue Flying Squirrel", resizable=True
)
keys = key.KeyStateHandler()
win.push_handlers(keys)

# level_context = LevelContext.load_level("level_4.json", win)

game_context = GameContext(win, os.listdir("./levels"))
game_context.next_level()
# game_context.game_state = GameState.GAME_OVER


# @win.event
# def on_resize(width, height):
#     level_context.player_y_offset = height // 4


@win.event
def on_draw():
    win.clear()
    game_context.draw(win, keys)


app.run()
