from pathlib import Path

import discord
from discord.ext import commands

from config import DISCORD_TOKEN


class DJUBEE(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()

        super().__init__(
            command_prefix="!",
            intents=intents,
        )

    async def setup_hook(self):
        cogs_path = Path(__file__).parent / "cogs"

        for file in cogs_path.glob("*.py"):
            if file.stem.startswith("_"):
                continue

            await self.load_extension(
                f"cogs.{file.stem}"
            )

        synced = await self.tree.sync()

        print(
            f"✅ Synced {len(synced)} commands"
        )

    async def on_ready(self):
        print(
            f"🐝 Logged in as {self.user}"
        )


bot = DJUBEE()

bot.run(DISCORD_TOKEN)