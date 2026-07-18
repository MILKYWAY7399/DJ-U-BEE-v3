import discord
from discord import app_commands
from discord.ext import commands

from ui.help_view import HelpView, make_embed


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="help",
        description="Browse DJ U BEE commands."
    )
    async def help(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            embed=make_embed("home"),
            view=HelpView(),
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(Help(bot))