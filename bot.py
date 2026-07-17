from pathlib import Path

import discord
import wavelink
from discord.ext import commands

from config import (
    DISCORD_TOKEN,
    LAVALINK_PASSWORD,
    LAVALINK_URI,
)
from music.manager import MusicManager
from providers.lavalink import LavalinkProvider
from providers.spotify import SpotifyProvider
from providers.lastfm import LastFMProvider
from providers.lyrics import LyricsProvider
from providers.playlist_provider import PlaylistProvider


class DJUBEE(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()

        super().__init__(
            command_prefix="!",
            intents=intents,
        )

        self.music = MusicManager(self)
        self.lavalink = LavalinkProvider()
        self.spotify = SpotifyProvider()
        self.lastfm = LastFMProvider()
        self.lyrics = LyricsProvider()
        self.playlists = PlaylistProvider()

    async def setup_hook(self):
        node = wavelink.Node(
            identifier="main",
            uri=LAVALINK_URI,
            password=LAVALINK_PASSWORD,
        )

        await wavelink.Pool.connect(
            nodes=[node],
            client=self,
        )

        print("✅ Connected to Lavalink")

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