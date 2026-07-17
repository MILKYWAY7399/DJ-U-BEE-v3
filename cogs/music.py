import discord
from discord import app_commands
from discord.ext import commands
import re

from ui.search_view import SearchView
from ui.lastfm_login_view import LastFMLoginView

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.music = bot.music
        self.lavalink = bot.lavalink
        self.spotify = bot.spotify
        self.lastfm_provider = bot.lastfm

    lastfm = app_commands.Group(
        name="lastfm",
        description="Manage your Last.fm account.",
    )

    @lastfm.command(
        name="login",
        description="Link your Last.fm account.",
    )
    async def login(
        self,
        interaction: discord.Interaction,
    ):
        if self.lastfm_provider.is_logged_in(interaction.user.id):
            await interaction.response.send_message(
                "❌ Your Last.fm account is already linked.",
                ephemeral=True,
            )
            return

        url = await self.lastfm_provider.create_login(
            interaction.user.id
        )

        await interaction.response.send_message(
            "Click **Authorize Last.fm**, approve access in your browser, then come back and press **I've Authorized**.",
            view=LastFMLoginView(
                self.lastfm_provider,
                url,
            ),
            ephemeral=True,
        )

    @lastfm.command(
    name="logout",
    description="Unlink your Last.fm account.",
)
    async def logout(
        self,
        interaction: discord.Interaction,
    ):
        username = self.lastfm_provider.get_username(
            interaction.user.id
        )

        if username is None:
            await interaction.response.send_message(
                "❌ You don't have a linked Last.fm account.",
                ephemeral=True,
            )
            return

        self.lastfm_provider.logout(
            interaction.user.id
        )

        await interaction.response.send_message(
            f"✅ Unlinked **{username}**.",
            ephemeral=True,
        )

    @lastfm.command(
        name="profile",
        description="View your linked Last.fm profile.",
    )
    async def lastfm_profile(
        self,
        interaction: discord.Interaction,
    ):
        profile = await self.lastfm_provider.get_profile(
            interaction.user.id
        )
        recent = await self.lastfm_provider.get_recent_track(
            interaction.user.id
        )

        if profile is None:
            await interaction.response.send_message(
                "❌ You haven't linked your Last.fm account.",
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            title=f"{profile['name']}'s Last.fm Profile",
            url=profile["url"],
            color=0xD51007,
        )

        images = profile.get("image", [])

        if images:
            image = images[-1].get("#text")

            if image:
                embed.set_thumbnail(
                    url=image
                )

        embed.add_field(
            name="Scrobbles",
            value=profile["playcount"],
            inline=True,
        )

        embed.add_field(
            name="Country",
            value=profile["country"] if profile["country"] else "Unknown",
            inline=True,
        )

        embed.add_field(
            name="Registered",
            value=f"<t:{profile['registered']['unixtime']}:D>",
            inline=True,
        )

        if recent and recent.get("@attr", {}).get("nowplaying") == "true":
            embed.add_field(
                name="Now Playing",
                value=f"🎵 **{recent['name']}**\nby **{recent['artist']['#text']}**",
                inline=False,
            )

        embed.set_footer(
            text="Powered by Last.fm"
        )

        await interaction.response.send_message(
            embed=embed
        )

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

            # Spotiy track
            if "open.spotify.com/track/" in query:
                title, artist = (
                    await self.spotify.get_track(
                        query
                    )
                )

                query = (
                    f"{title} {artist}"
                )

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

                return

            # Spotify Album
            if "open.spotify.com/album/" in query:

                await interaction.response.defer()

                tracks = await self.spotify.get_album(
                    query
                )

                await self.music.join(
                    interaction
                )

                added = 0

                for title, artist in tracks:

                    print(
                        f"Searching: {title} - {artist}"
                    )

                    try:
                        song = await self.lavalink.search(
                            f"{title} {artist}",
                            interaction.user.id,
                        )

                        await self.music.play(
                            interaction,
                            song,
                        )

                        added += 1

                    except Exception as e:
                        print(
                            f"Skipped: {title} - {artist}"
                        )
                        print(e)

                await interaction.followup.send(
                    f"💿 Added **{added}** songs to the queue."
                )

                return

            # Normal search
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
            if interaction.response.is_done():
                await interaction.followup.send(
                    f"❌ {e}",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    f"❌ {e}",
                    ephemeral=True,
                )


    @app_commands.command(
        name="playlist",
        description="Import Spotify playlist from pasted track links.",
    )
    @app_commands.describe(
        tracks="Paste Spotify track links (one per line)"
    )
    async def playlist(
        self,
        interaction: discord.Interaction,
        tracks: str,
    ):
        print(repr(tracks))
        await interaction.response.defer()

        # urls = [
        #     line.strip()
        #     for line in tracks.split()
        #     if "open.spotify.com/track/" in line
        # ]

        urls = re.findall(
            r"https://open\.spotify\.com/track/[^\s]+",
            tracks,
        )

        if not urls:
            await interaction.followup.send(
                "❌ No Spotify track links found."
            )
            return

        await self.music.join(
            interaction
        )

        added = 0
        skipped = 0

        for url in urls:
            try:
                title, artist = (
                    await self.spotify.get_track(
                        url
                    )
                )

                song = await self.lavalink.search(
                    f"{title} {artist}",
                    interaction.user.id,
                )

                await self.music.play(
                    interaction,
                    song,
                )

                added += 1

            except Exception as e:
                skipped += 1
                print(f"Skipped: {url}")
                print(e)

        embed = discord.Embed(
            title="📋 Playlist Imported",
            description=(
                f"✅ Added: **{added}**\n"
                f"❌ Skipped: **{skipped}**"
            ),
            color=0x5865F2,
        )

        await interaction.followup.send(
            embed=embed
        )

async def setup(bot):
    await bot.add_cog(
        Music(bot)
    )