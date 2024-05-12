from core.entity import Entity, EntityMode, SpriteConfig

AMMO_WIDTH = 30


class Ammo(Entity):
    def __init__(
        self,
        x,
        y,
        level_context,
    ):
        super().__init__(x, y, AMMO_WIDTH, AMMO_WIDTH, level_context, 0)

        self.current_mode = EntityMode.IDLE

        self.load_mode_sprite_map(
            "assets/sprites/bullet/",
            [
                SpriteConfig(
                    mode=EntityMode.IDLE,
                    is_animation=False,
                    duration=None,
                    column_padding=None,
                    columns=None,
                    rows=None,
                )
            ],
        )

    def update(self):
        pass
