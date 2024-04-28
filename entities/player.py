import time
from pyglet import app
from pyglet.window import key
from core.direction import Direction
from entities.bullet import Bullet
from core.entity import JUMP_ACC, Entity, EntityMode, SpriteConfig


PLAYER_WIDTH = 75
PLAYER_HEIGHT = 75

BULLET_TIMEOUT = 1


class Player(Entity):
    def __init__(self, pos: tuple[int, int], level_context) -> None:
        super().__init__(
            pos[0], pos[1], PLAYER_WIDTH, PLAYER_HEIGHT, level_context, 100
        )

        self.bullet_timeout = (False, 0)
        self.load_mode_sprite_map(
            "assets/sprites/player/",
            [
                SpriteConfig(
                    mode=EntityMode.IDLE,
                    is_animation=True,
                    duration=0.2,
                    columns=6,
                    column_padding=35,
                ),
                SpriteConfig(
                    mode=EntityMode.WALKING,
                    is_animation=True,
                    duration=0.1,
                    columns=8,
                    column_padding=35,
                ),
                SpriteConfig(
                    mode=EntityMode.JUMPING,
                    is_animation=False,
                    duration=None,
                    columns=None,
                    column_padding=35,
                ),
            ],
        )

    def update(self, keys: key.KeyStateHandler):
        if self.health <= 0:
            app.exit()

        self.center = self.pos + self.hitbox / 2

        self.handle_ground()

        self.handle_shooting(keys, self.level_context.bullets)
        self.handle_movement(keys)
        self.handle_collisions(self.level_context.blocks)

        self.vel += self.acc
        self.pos += self.vel

        # self.show_hitbox()

    def handle_shooting(self, keys, bullets):
        if time.time() > self.bullet_timeout[1]:
            self.bullet_timeout = (False, 0)

        if keys[key.F]:
            if not self.bullet_timeout[0]:
                Bullet(
                    self.pos[0] + self.hitbox[0] // 2,
                    self.pos[1] + self.hitbox[1] // 2,
                    self.direction,
                    bullets,
                    self.level_context,
                )
                self.bullet_timeout = (True, time.time() + BULLET_TIMEOUT)

    def handle_movement(self, keys):
        if keys[key.W]:
            if self.grounded:
                self.acc += JUMP_ACC

        if keys[key.D]:
            self.vel[0] = (Direction.RIGHT.get() * self.speed)[0]
            self.direction = Direction.RIGHT.get()
        elif keys[key.A]:
            self.vel[0] = (Direction.LEFT.get() * self.speed)[0]
            self.direction = Direction.LEFT.get()

        else:
            self.vel[0] = 0
