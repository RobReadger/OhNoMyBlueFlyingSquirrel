from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import numpy as np
from pyglet import shapes, sprite, resource, image
from core.body import Body
from core.direction import Direction
from objects.block import Block


GRAVITY = np.array([0, -1])
JUMP_ACC = np.array([0, 17])


class EntityMode(Enum):
    IDLE = "idle"
    WALKING = "walking"
    ATTACKING = "attacking"
    DYING = "dying"
    JUMPING = "jumping"


@dataclass
class SpriteConfig:
    mode: EntityMode
    is_animation: bool
    duration: float | None
    columns: int | None
    column_padding: int | None


class Entity(Body, ABC):

    def __init__(self, x, y, width, height, level_context, health: float):
        super().__init__(x, y, width, height)
        self.vel = np.array([0, 0])
        self.speed = 10
        self.direction: np.array = Direction.RIGHT.get()
        self.mode_sprite_map: dict[EntityMode : sprite.Sprite] = {
            EntityMode.IDLE: None,
            EntityMode.WALKING: None,
            EntityMode.ATTACKING: None,
            EntityMode.DYING: None,
            EntityMode.JUMPING: None,
        }
        self.current_mode = EntityMode.IDLE
        self.color = (255, 255, 255)
        self.level_context = level_context

        self.health = health

    @abstractmethod
    def update(self):
        pass

    def load_mode_sprite_map(
        self,
        sprite_folder_url: str,
        sprite_configs: list[SpriteConfig],
    ):
        for sprite_config in sprite_configs:
            if sprite_config.is_animation:
                sprite_sheet = resource.image(
                    sprite_folder_url + sprite_config.mode.value + ".png"
                )
                image_grid = image.ImageGrid(
                    sprite_sheet,
                    rows=1,
                    columns=sprite_config.columns,
                    column_padding=sprite_config.column_padding,
                )

                ani = image.Animation.from_image_sequence(
                    image_grid, duration=sprite_config.duration, loop=True
                )

                self.mode_sprite_map[sprite_config.mode] = sprite.Sprite(
                    img=ani, x=self.pos[0], y=self.pos[1]
                )
                continue

            static = resource.image(
                sprite_folder_url + sprite_config.mode.value + ".png"
            )

            self.mode_sprite_map[sprite_config.mode] = sprite.Sprite(
                img=static, x=self.pos[0], y=self.pos[1]
            )

    def show(self):
        if self.mode_sprite_map[self.current_mode] is None:
            shapes.Rectangle(
                self.pos[0],
                self.pos[1],
                self.hitbox[0],
                self.hitbox[1],
                color=self.color,
            ).draw()
            return

        current_sprite = self.mode_sprite_map[self.current_mode]
        current_sprite.update(
            x=(
                self.pos[0]
                if self.direction[0] == Direction.RIGHT.get()[0]
                else self.pos[0] + self.hitbox[0]
            ),
            y=self.pos[1],
        )
        current_sprite.scale_x = self.direction[0]

        current_sprite.draw()

    def grounded_check(self, blocks: list[Block]):
        self.grounded = False
        for block in blocks:
            if self.vel[1] <= 0 and self.is_bottom_colliding(block, self.vel[1]):
                self.grounded = True
                break

    def handle_collisions(self, blocks):
        # print(f"Acc: {self.acc}, vel: {self.vel}, pos: {self.pos}")
        for block in blocks:
            if self.vel[1] <= 0 and self.is_bottom_colliding(block, self.vel[1]):
                self.vel[1] = 0

            if self.vel[0] != 0 and self.are_sides_colliding(block, self.vel[0]):
                self.vel[0] = 0

    def handle_ground(self):
        self.grounded_check(self.level_context.blocks)

        if self.grounded and self.vel[0] != 0:
            self.current_mode = EntityMode.WALKING
        elif self.grounded and self.vel[0] == 0:
            self.current_mode = EntityMode.IDLE
        else:
            self.current_mode = EntityMode.JUMPING

        if not self.grounded:
            self.acc = GRAVITY.copy()
        else:
            self.acc = np.array([0, 0])
