import discord
from discord import app_commands
from discord.ext import commands

from ui.search_view import SearchView


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.music = bot.music
        self.lavalink = bot.lavalink

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

    @app_commands.command(
        name="play",
        description="Play a song.",
    )
    @app_commands.describe(
        query="Song name or URL"
    )
    async def play(
        self,
        interaction: discord.Interaction,
        query: str,
    ):
        try:
            songs = await self.lavalink.search_many(
                query,
                interaction.user.id,
            )

            embed = discord.Embed(
                title="🔍 Search Results",
                description="Choose the song you want to play.",
                color=0x5865F2,
            )

            await interaction.response.send_message(
                embed=embed,
                view=SearchView(songs),
                ephemeral=True,
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