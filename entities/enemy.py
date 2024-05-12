import time
import numpy as np
from pyglet import shapes
from pyglet.graphics import Batch
from core.direction import Direction
from util.game_util import distance_between_points

from core.entity import JUMP_ACC, Entity, EntityMode, SpriteConfig

GRAVITY = np.array([0, -1])

ENEMY_WIDTH = 40
ENEMY_HEIGHT = 70
PURPLE = (204, 0, 255)

ATTACK_TIMEOUT = 1.8


class Enemy(Entity):
    def __init__(self, pos: tuple[int, int], level_context) -> None:
        super().__init__(pos[0], pos[1], ENEMY_WIDTH, ENEMY_HEIGHT, level_context, 25)
        self.color = PURPLE

        self.attack_timeout = (False, 0)

        self.target = None
        self.speed = 3

        self.started_attack = False

        # self.sprite = shapes.Rectangle(
        #     x=self.pos[0],
        #     y=self.pos[1],
        #     width=self.hitbox[0],
        #     height=self.hitbox[1],
        #     color=self.color,
        #     batch=batch,
        # )

        self.load_mode_sprite_map(
            "assets/sprites/enemy/skeleton/",
            [
                SpriteConfig(
                    mode=EntityMode.IDLE,
                    is_animation=True,
                    duration=0.3,
                    columns=11,
                    column_padding=0,
                    rows=1,
                ),
                SpriteConfig(
                    mode=EntityMode.WALKING,
                    is_animation=True,
                    duration=0.2,
                    columns=13,
                    column_padding=0,
                    rows=1,
                ),
                SpriteConfig(
                    mode=EntityMode.JUMPING,
                    is_animation=True,
                    duration=0.2,
                    columns=13,
                    column_padding=0,
                    rows=1,
                ),
                SpriteConfig(
                    mode=EntityMode.ATTACKING,
                    is_animation=True,
                    duration=0.1,
                    columns=18,
                    column_padding=0,
                    rows=1,
                ),
            ],
        )

    def update(self):
        self.center = self.pos + self.hitbox / 2
        dist = distance_between_points(self.center, self.level_context.player.center)

        if dist > 1000:
            return

        self.handle_ground()

        self.target_player(dist)
        self.move_toward_target()

        self.handle_collisions(self.level_context.blocks)

        self.handle_jump()

        player_vec = self.level_context.player.center - self.pos

        self.direction = (
            Direction.RIGHT.get() if player_vec[0] > 0 else Direction.LEFT.get()
        )

        if time.time() > self.attack_timeout[1]:
            self.attack_timeout = (False, 0)

        if self.current_mode == EntityMode.ATTACKING and not self.attack_timeout[0]:
            self.level_context.player.health -= 50
            self.attack_timeout = (True, time.time() + ATTACK_TIMEOUT)

        self.vel += self.acc
        self.pos += self.vel

        # for block in self.level_context.blocks:
        #     print(self.are_sides_colliding(block))

        # self.show_hitbox()

    def target_player(self, dist):

        if 50 < dist < 500:
            self.target = self.level_context.player.center - self.pos
            return

        self.target = None

        if dist < 50:
            if not self.started_attack:
                # self.attack_timeout = (True, time.time() + 0.2)
                self.started_attack = True

            self.vel[0] = 0
            self.current_mode = EntityMode.ATTACKING
            return

        self.started_attack = False

    def move_toward_target(self):
        if self.target is not None:
            self.vel[0] = self.target[0] / abs(self.target[0]) * self.speed
            return
        self.vel[0] = 0

    def handle_jump(self):
        if self.target is not None and self.vel[0] == 0:
            if self.grounded:
                self.acc += JUMP_ACC

    def __str__(self) -> str:
        return f"pos: {self.pos}, shape: {self.hitbox}"
