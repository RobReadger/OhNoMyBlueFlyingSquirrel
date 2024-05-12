import json


class Level:
    def __init__(self) -> None:
        self.player_spawn: tuple[int, int] = None
        self.blocks: list[tuple[int, int]] = []
        self.enemies: list[tuple[int, int]] = []
        self.ammo: list[tuple[int, int]] = []
        self.level_end: tuple[int, int] = None


class LevelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Level):
            return {
                "player_spawn": obj.player_spawn,
                "blocks": obj.blocks,
                "enemies": obj.enemies,
                "ammo": obj.ammo,
                "level_end": obj.level_end,
            }
        return json.JSONEncoder.default(self, obj)


class LevelDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if "player_spawn" in obj and "blocks" in obj:
            level = Level()

            level.player_spawn = (
                None if obj["player_spawn"] is None else tuple(obj["player_spawn"])
            )
            if "blocks" in obj:
                level.blocks = [tuple(block) for block in obj["blocks"]]
            if "enemies" in obj:
                level.enemies = [tuple(enemy) for enemy in obj["enemies"]]
            if "ammo" in obj:
                level.ammo = [tuple(ammo) for ammo in obj["ammo"]]
            level.level_end = (
                None if obj["level_end"] is None else tuple(obj["level_end"])
            )
            return level
        return obj
