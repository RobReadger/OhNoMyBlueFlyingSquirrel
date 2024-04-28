import time
from core.entity import Entity, EntityMode, SpriteConfig


BULLET_WIDTH = 10
BULLET_HEIGHT = 10


class Bullet(Entity):
    def __init__(
        self,
        x,
        y,
        direction,
        bullets: list["Bullet"],
        level_context,
        lifetime: float = 3,
    ):
        super().__init__(x, y, BULLET_WIDTH, BULLET_HEIGHT, level_context, 0)
        self.direction = direction
        self.lifetime = time.time() + lifetime
        bullets.append(self)

        self.current_mode = EntityMode.WALKING

        self.load_mode_sprite_map(
            "assets/sprites/bullet/",
            [
                SpriteConfig(
                    mode=EntityMode.WALKING,
                    is_animation=False,
                    duration=None,
                    column_padding=None,
                    columns=None,
                )
            ],
        )

    def update(self):
        self.vel = self.direction * self.speed
        self.pos += self.vel
