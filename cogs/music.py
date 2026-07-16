import discord
from discord import app_commands
from discord.ext import commands

from music.manager import MusicManager


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music = MusicManager(bot)

    @app_commands.command(
        name="join",
        description="Join your voice channel.",
    )
    async def join(
        self,
        interaction: discord.Interaction,
    ):
        try:
            player = await self.music.join(
                interaction
            )

            await interaction.response.send_message(
                f"✅ Joined **{player.channel.name}**"
            )

        except RuntimeError as e:
            await interaction.response.send_message(
                f"❌ {e}",
                ephemeral=True,
            )

    @app_commands.command(
        name="leave",
        description="Leave the voice channel.",
    )
    async def leave(
        self,
        interaction: discord.Interaction,
    ):
        try:
            await self.music.leave(
                interaction
            )

            await interaction.response.send_message(
                "👋 Disconnected."
            )

        except RuntimeError as e:
            await interaction.response.send_message(
                f"❌ {e}",
                ephemeral=True,
            )


async def setup(bot):
    await bot.add_cog(
        Music(bot)
    )