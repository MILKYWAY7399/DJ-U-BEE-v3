from collections import defaultdict

import discord
import wavelink

from models.song import Song
from music.guild_state import GuildState


class MusicManager:
    def __init__(self, bot):
        self.bot = bot

        self.guilds: dict[int, GuildState] = defaultdict(
            GuildState
        )

    def get_state(
        self,
        guild_id: int,
    ) -> GuildState:
        return self.guilds[guild_id]

    async def join(
        self,
        interaction: discord.Interaction,
    ) -> wavelink.Player:
        if interaction.user.voice is None:
            raise RuntimeError(
                "You must join a voice channel first."
            )

        channel = interaction.user.voice.channel

        player: wavelink.Player = await channel.connect(
            cls=wavelink.Player
        )

        return player

    async def leave(
        self,
        interaction: discord.Interaction,
    ):
        player: wavelink.Player | None = interaction.guild.voice_client

        if player is None:
            raise RuntimeError(
                "I'm not connected."
            )

        await player.disconnect()

        self.guilds.pop(
            interaction.guild.id,
            None,
        )

    async def play(
        self,
        interaction: discord.Interaction,
        song: Song,
    ):
        state = self.get_state(
            interaction.guild.id
        )

        player: wavelink.Player | None = interaction.guild.voice_client

        if player is None:
            player = await self.join(
                interaction
            )

        if player.playing:
            state.queue.append(song)
            return False

        state.current = song

        await player.play(
            song.track
        )

        return True