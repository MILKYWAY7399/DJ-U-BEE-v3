import discord
import wavelink

from models.song import Song


class MusicManager:
    def __init__(self, bot):
        self.bot = bot

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

    async def play(
        self,
        interaction: discord.Interaction,
        song: Song,
    ):
        player: wavelink.Player | None = interaction.guild.voice_client

        if player is None:
            player = await self.join(
                interaction
            )

        await player.play(song.track)