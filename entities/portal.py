from core.entity import Entity, EntityMode, SpriteConfig

PORTAL_WIDTH = 70
PORTAL_HEIGHT = 120


class Portal(Entity):
    def __init__(
        self,
        x,
        y,
        level_context,
    ):
        super().__init__(x, y, PORTAL_WIDTH, PORTAL_HEIGHT, level_context, 0)

        self.current_mode = EntityMode.IDLE

        self.load_mode_sprite_map(
            "assets/sprites/portal/",
            [
                SpriteConfig(
                    mode=EntityMode.IDLE,
                    is_animation=True,
                    duration=0.15,
                    column_padding=0,
                    columns=3,
                    rows=2,
                )
            ],
        )

    def update(self):
        if self.is_colliding(self.level_context.player):
            self.level_context.game_context.next_level()
