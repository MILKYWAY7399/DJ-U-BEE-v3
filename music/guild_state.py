from dataclasses import dataclass, field

from models.song import Song


@dataclass(slots=True)
class GuildState:
    queue: list[Song] = field(
        default_factory=list
    )

    current: Song | None = None