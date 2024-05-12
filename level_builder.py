from dataclasses import dataclass
from enum import Enum
import json
import os
import time
import numpy as np
from pyglet import app, shapes, text
from pyglet.math import Mat4
from pyglet.window import key, Window, mouse
from pyglet.graphics import Batch

from core.level import Level, LevelDecoder, LevelEncoder


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BG_COLOR = (89, 89, 89)
GRID_COLOR = (140, 140, 140)
PURPLE = (204, 0, 255)
BLUE = (0, 153, 204)
BLACK = (51, 51, 51)

win = Window(
    resizable=True,
    caption="Oh No My Blue Flying Squirrel - Level Builder",
)
keys = key.KeyStateHandler()
win.push_handlers(keys)

bg = shapes.Rectangle(0, 0, win.width, win.height, BG_COLOR)
origin = shapes.Circle(0, 0, 5, color=WHITE)
camera_pos = [0, 0]

# Generate grid
grid = []
grid_batch = Batch()
GRID_GAP = 30
NUM_OF_LINES = 1000

block_batch = Batch()
enemy_batch = Batch()
ammo_batch = Batch()

for i in range(-NUM_OF_LINES // 2, NUM_OF_LINES // 2):
    grid.append(
        shapes.Line(
            -NUM_OF_LINES // 2 * GRID_GAP,
            i * GRID_GAP,
            NUM_OF_LINES // 2 * GRID_GAP,
            i * GRID_GAP,
            color=GRID_COLOR,
            batch=grid_batch,
        )
    )

    grid.append(
        shapes.Line(
            i * GRID_GAP,
            -NUM_OF_LINES // 2 * GRID_GAP,
            i * GRID_GAP,
            NUM_OF_LINES // 2 * GRID_GAP,
            color=GRID_COLOR,
            batch=grid_batch,
        )
    )


class Placable(Enum):
    BLOCK = 1
    ENEMY = 2
    PLAYER_SPAWN = 3
    AMMO = 4
    LEVEL_END = 5

    def get_shape(self) -> shapes.ShapeBase:
        match self.value:
            case Placable.BLOCK.value:
                return shapes.Rectangle(
                    x=0, y=0, width=GRID_GAP, height=GRID_GAP, color=WHITE
                )
            case Placable.ENEMY.value:
                return shapes.Rectangle(
                    x=0, y=0, width=GRID_GAP, height=2 * GRID_GAP, color=PURPLE
                )
            case Placable.PLAYER_SPAWN.value:
                return shapes.Circle(x=0, y=0, radius=10, color=RED)
            case Placable.AMMO.value:
                return shapes.Rectangle(
                    x=0, y=0, width=GRID_GAP, height=GRID_GAP, color=BLUE
                )
            case Placable.LEVEL_END.value:
                return shapes.Rectangle(
                    x=0, y=0, width=2 * GRID_GAP, height=2 * GRID_GAP, color=BLACK
                )


@dataclass
class LevelBuild:
    blocks: dict[np.array : Placable.BLOCK]
    enemies: dict[np.array : Placable.ENEMY]
    player_spawn: np.array
    ammo: dict[np.array : Placable.AMMO]
    level_end: np.array

    def save(self) -> None:
        levels = os.listdir("levels")

        if len(levels) == 0:
            filename = "level_1.json"
        else:
            filename = f"level_{max([int(x.split('.')[0].split('_')[1]) for x in levels]) + 1}.json"

        level = Level()

        if self.blocks is not None:
            level.blocks = [(key[0], key[1]) for key in self.blocks.keys()]

        if self.enemies is not None:
            level.enemies = [(key[0], key[1]) for key in self.enemies.keys()]

        if self.player_spawn is not None:
            level.player_spawn = (self.player_spawn[0], self.player_spawn[1])

        if self.ammo is not None:
            level.ammo = [(key[0], key[1]) for key in self.ammo.keys()]

        if self.level_end is not None:
            level.level_end = (self.level_end[0], self.level_end[1])

        with open(os.path.join("levels", filename), "w") as out:
            out.write(json.dumps(level, cls=LevelEncoder, indent=4))

    def load(self, level_name: str) -> None:
        with open(os.path.join("levels", level_name), "r") as f:
            loaded_level: Level = json.load(f, cls=LevelDecoder)

            for block_pos in loaded_level.blocks:
                block = Placable.BLOCK.get_shape()
                block.batch = block_batch
                block.x = block_pos[0]
                block.y = block_pos[1]

                self.blocks[block_pos] = block

            for enemy_pos in loaded_level.enemies:
                enemy = Placable.ENEMY.get_shape()
                enemy.batch = enemy_batch
                enemy.x = enemy_pos[0]
                enemy.y = enemy_pos[1]

                self.enemies[enemy_pos] = enemy

            for ammo_pos in loaded_level.ammo:
                ammo = Placable.AMMO.get_shape()
                ammo.batch = ammo_batch
                ammo.x = ammo_pos[0]
                ammo.y = ammo_pos[1]

                self.ammo[ammo_pos] = ammo

            self.player_spawn = loaded_level.player_spawn
            self.level_end = loaded_level.level_end


selected_item: Placable = Placable.BLOCK
label = text.Label(
    f"Selected: {selected_item.name}",
    font_name="Cairo",
    font_size=36,
    anchor_x="left",
    anchor_y="baseline",
)

mouse_grid_pos = [0, 0]


# 1: individual
# 2: rect
mode = 1


level = LevelBuild({}, {}, None, {}, None)


@win.event
def on_resize(width, height):
    bg.width = width
    bg.height = height


def update_mouse_pos(x, y):
    global mouse_grid_pos

    mouse_grid_pos = (
        x - x % GRID_GAP + camera_pos[0] - camera_pos[0] % GRID_GAP,
        y - y % GRID_GAP + camera_pos[1] - camera_pos[1] % GRID_GAP,
    )


@win.event
def on_mouse_motion(x, y, dx, dy):
    update_mouse_pos(x, y)


def place_item(item: Placable):
    """Places selected item"""
    match item:
        case Placable.BLOCK:
            if mouse_grid_pos in level.blocks:
                return

            block = Placable.BLOCK.get_shape()
            block.batch = block_batch
            block.x = mouse_grid_pos[0]
            block.y = mouse_grid_pos[1]

            level.blocks[mouse_grid_pos] = block

        case Placable.PLAYER_SPAWN:
            if mouse_grid_pos == level.player_spawn:
                return

            level.player_spawn = mouse_grid_pos

        case Placable.ENEMY:
            if mouse_grid_pos in level.enemies:
                return

            enemy = Placable.ENEMY.get_shape()
            enemy.batch = enemy_batch
            enemy.x = mouse_grid_pos[0]
            enemy.y = mouse_grid_pos[1]

            level.enemies[mouse_grid_pos] = enemy

        case Placable.AMMO:
            if mouse_grid_pos in level.ammo:
                return

            ammo = Placable.AMMO.get_shape()
            ammo.batch = enemy_batch
            ammo.x = mouse_grid_pos[0]
            ammo.y = mouse_grid_pos[1]

            level.ammo[mouse_grid_pos] = ammo

        case Placable.LEVEL_END:
            if mouse_grid_pos == level.level_end:
                return

            level.level_end = mouse_grid_pos


def remove_item(item: Placable):
    """Removes selected item"""
    match item:
        case Placable.BLOCK:

            if mouse_grid_pos not in level.blocks:
                return

            del level.blocks[mouse_grid_pos]

        case Placable.PLAYER_SPAWN:
            if mouse_grid_pos != level.player_spawn:
                return

            level.player_spawn = None

        case Placable.ENEMY:
            if mouse_grid_pos not in level.enemies:
                return

            del level.enemies[mouse_grid_pos]

        case Placable.AMMO:
            if mouse_grid_pos not in level.ammo:
                return

            del level.ammo[mouse_grid_pos]

        case Placable.LEVEL_END:
            if mouse_grid_pos != level.level_end:
                return

            level.level_end = None


@win.event
def on_mouse_press(x, y, button, modifiers):
    update_mouse_pos(x, y)

    if button == 1:
        place_item(selected_item)

    elif button == 4:
        remove_item(selected_item)


@win.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    update_mouse_pos(x, y)

    if buttons & mouse.LEFT:
        place_item(selected_item)
    elif buttons & mouse.RIGHT:
        remove_item(selected_item)


spawn_sprite = Placable.PLAYER_SPAWN.get_shape()
level_end_sprite = Placable.LEVEL_END.get_shape()


@win.event
def on_draw():
    global selected_item, spawn_sprite

    win.clear()
    bg.x = camera_pos[0]
    bg.y = camera_pos[1]
    label.x = camera_pos[0]
    label.y = camera_pos[1] + win.height - 50
    label.text = f"Selected: {selected_item.name}"

    bg.draw()
    grid_batch.draw()
    origin.draw()
    label.draw()
    block_batch.draw()
    enemy_batch.draw()
    ammo_batch.draw()

    mouse_sprite = selected_item.get_shape()
    mouse_sprite.x = mouse_grid_pos[0]
    mouse_sprite.y = mouse_grid_pos[1]
    mouse_sprite.opacity = 128

    mouse_sprite.draw()

    if level.player_spawn is not None:
        spawn_sprite.x = level.player_spawn[0]
        spawn_sprite.y = level.player_spawn[1]
        spawn_sprite.draw()

    if level.level_end is not None:
        level_end_sprite.x = level.level_end[0]
        level_end_sprite.y = level.level_end[1]
        level_end_sprite.draw()

    cam_speed = 30

    if keys[key.LSHIFT]:
        cam_speed = 60

    if keys[key.D]:
        camera_pos[0] += cam_speed
    if keys[key.A]:
        camera_pos[0] -= cam_speed
    if keys[key.W]:
        camera_pos[1] += cam_speed
    if keys[key.S]:
        camera_pos[1] -= cam_speed

    if keys[key.L]:
        level.save()
        time.sleep(2)

    if keys[key._1]:
        selected_item = Placable.BLOCK
    if keys[key._2]:
        selected_item = Placable.ENEMY
    if keys[key._3]:
        selected_item = Placable.PLAYER_SPAWN
    if keys[key._4]:
        selected_item = Placable.AMMO
    if keys[key._5]:
        selected_item = Placable.LEVEL_END

    win.view = Mat4().translate((-(camera_pos[0]), -(camera_pos[1]), 0))


app.run()
