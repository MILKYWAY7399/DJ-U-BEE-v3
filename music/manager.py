import discord
import wavelink


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