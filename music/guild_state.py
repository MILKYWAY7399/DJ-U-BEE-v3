from dataclasses import dataclass, field

import discord
import wavelink
import asyncio

from models.song import Song
from music.loop_mode import LoopMode


@dataclass(slots=True)
class GuildState:
    player: wavelink.Player | None = None

    current: Song | None = None

    history: list[Song] = field(
        default_factory=list
    )

    queue: list[Song] = field(
        default_factory=list
    )

    loop_mode: LoopMode = LoopMode.OFF

    text_channel: discord.TextChannel | None = None

    player_message: discord.Message | None = None

    scrobble_task: asyncio.Task | None = None

    radio: bool = False

    settings_loaded: bool = False

    progress_task: asyncio.Task | None = None