import discord

from discord import app_commands
from discord.ext import commands


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="stats",
        description="View your listening statistics.",
    )
    async def stats(
        self,
        interaction: discord.Interaction,
    ):
        stats = self.bot.stats.get_user_stats(
            interaction.guild.id,
            interaction.user.id,
        )

        if stats is None:
            await interaction.response.send_message(
                "You don't have any listening stats yet.",
                ephemeral=True,
            )
            return

        top_artists = sorted(
            stats["artists"].items(),
            key=lambda x: x[1],
            reverse=True,
        )[:5]

        top_songs = sorted(
            stats["songs"].items(),
            key=lambda x: x[1],
            reverse=True,
        )[:5]

        artist_text = "\n".join(
            f"{i}. **{artist}** ({plays})"
            for i, (artist, plays)
            in enumerate(top_artists, 1)
        ) or "None"

        song_text = "\n".join(
            f"{i}. **{song}** ({plays})"
            for i, (song, plays)
            in enumerate(top_songs, 1)
        ) or "None"

        embed = discord.Embed(
            title=f"{interaction.user.display_name}'s Stats",
            color=discord.Color.orange(),
        )

        embed.add_field(
            name="Overview",
            value=(
                f"🎵 Songs Played: **{stats['songs_played']}**\n"
                f"⏱ Listening Time: **{self.bot.stats.format_time(stats['listening_time'])}**\n"
                f"🎤 Unique Artists: **{len(stats['artists'])}**\n"
                f"🎶 Unique Songs: **{len(stats['songs'])}**"
            ),
            inline=False,
        )

        embed.add_field(
            name="🏆 Top Artists",
            value=artist_text,
            inline=True,
        )

        embed.add_field(
            name="🎧 Top Songs",
            value=song_text,
            inline=True,
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(
        Stats(bot)
    )