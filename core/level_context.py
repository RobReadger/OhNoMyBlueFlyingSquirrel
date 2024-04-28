import json
import os
import time

import numpy as np
from core.entity import Entity
from core.level import Level, LevelDecoder
from pyglet.graphics import Batch
from pyglet import shapes, window, image, sprite
from pyglet.math import Mat4
from pyglet.window import key, FPSDisplay

from entities.bullet import Bullet
from entities.enemy import Enemy
from entities.player import Player
from objects.block import Block

BLOCK_WIDTH = 30
WHITE = (255, 255, 255)


class LevelContext:
    def __init__(self, win: window.Window) -> None:
        self.entities: list[Entity] = []
        self.blocks: list[Block] = []
        self.level: Level = None
        self.block_batch = Batch()
        self.entity_batch = Batch()

        self.player: Player = None
        self.bullets: list[Bullet] = []
        self.enemies: list[Enemy] = []
        self.player_health_bar_max = shapes.Rectangle(
            0,
            0,
            200,
            30,
            color=(255, 0, 0),
        )
        self.player_health_bar_actual = shapes.Rectangle(
            0,
            0,
            200,
            30,
            color=(0, 255, 0),
        )

        self.bg = sprite.Sprite(
            x=0,
            y=0,
            img=image.load(os.path.join("assets", "backgrounds", "bg.png")),
        )

        self.player_y_offset = win.height // 4
        self.fps_display = FPSDisplay(win)
        self.camera_pos = (0, 0)

    def draw(self, win: window.Window, keys):
        self.camera_pos = (
            self.player.pos[0] - win.width // 2,
            self.player.pos[1] - self.player_y_offset,
        )

        win.view = Mat4().translate(
            (
                -self.camera_pos[0],
                -self.camera_pos[1],
                0,
            )
        )

        self.bg.x = self.camera_pos[0] - 25
        self.bg.y = self.camera_pos[1] - 200
        self.bg.draw()

        self.update(keys)
        self.show(self.camera_pos, win)

        self.fps_display.label.x = self.camera_pos[0] + win.width - 100
        self.fps_display.label.y = self.camera_pos[1] + win.height - 50
        self.fps_display.draw()

    def show(self, camera_pos: np.array, win: window.Window):
        self.block_batch.draw()
        # self.entity_batch.draw()
        self.player.show()

        self.player_health_bar_max.x = camera_pos[0] + 20
        self.player_health_bar_max.y = camera_pos[1] + win.height - 50
        self.player_health_bar_max.draw()

        self.player_health_bar_actual.x = camera_pos[0] + 20
        self.player_health_bar_actual.y = camera_pos[1] + win.height - 50
        self.player_health_bar_actual.width = self.player.health * 2
        self.player_health_bar_actual.draw()

        for enemy in self.enemies:
            enemy.show()

    def update(self, keys):
        self.player.update(keys)
        for enemy in self.enemies:
            enemy.update()
        self.handle_bullets()

    def handle_bullets(self):
        bullets_to_render = []

        for bullet in self.bullets:
            if time.time() > bullet.lifetime:
                continue

            enemy_for_removal = None
            enemy_colliding = False
            for i, enemy in enumerate(self.enemies):
                if bullet.is_colliding(enemy):
                    enemy_colliding = True
                    enemy_for_removal = i
                    break

            if enemy_colliding:
                del self.enemies[enemy_for_removal]
                continue

            for block in self.blocks:
                if bullet.is_colliding(block):
                    break
            else:
                bullets_to_render.append(bullet)

        self.bullets = bullets_to_render
        for bullet in self.bullets:
            bullet.update()
            bullet.show()

    @staticmethod
    def load_level(level_name: str, win):
        context = LevelContext(win)

        with open(os.path.join("levels", level_name), "r") as f:
            level = json.load(f, cls=LevelDecoder)
            context.level = level

        for block_pos in context.level.blocks:
            block = Block(
                block_pos[0], block_pos[1], BLOCK_WIDTH, BLOCK_WIDTH, color=WHITE
            )
            block.add_to_batch(context.block_batch)

            context.blocks.append(block)

        for enemy_pos in context.level.enemies:
            enemy = Enemy(enemy_pos, context)
            context.enemies.append(enemy)

        context.player = Player(context.level.player_spawn, context)

        return context
