from dataclasses import dataclass, field

import discord
import wavelink

from models.song import Song


@dataclass(slots=True)
class GuildState:
    player: wavelink.Player | None = None

    current: Song | None = None

    queue: list[Song] = field(
        default_factory=list
    )

    text_channel: discord.TextChannel | None = None

    player_message: discord.Message | None = None