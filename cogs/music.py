import discord
from discord import app_commands
from discord.ext import commands
import re
import uuid

from ui.search_view import SearchView
from ui.lastfm_login_view import LastFMLoginView
from models.song import Song
from ui.playlist_save_modal import PlaylistSaveModal

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.music = bot.music
        self.lavalink = bot.lavalink
        self.spotify = bot.spotify
        self.lastfm_provider = bot.lastfm
        self.autocomplete_cache: dict[str, Song] = {}
        self.playlists = bot.playlists

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


    playlist = app_commands.Group(
        name="playlist",
        description="Manage your saved playlists.",
    )

    @playlist.command(
        name="save",
        description="Save a custom playlist.",
    )
    async def playlist_save(
        self,
        interaction: discord.Interaction,
    ):
        await interaction.response.send_modal(
            PlaylistSaveModal(self)
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
    async def play_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        if len(current) < 2:
            return []

        try:
            songs = await self.lavalink.search_many(
                current,
                interaction.user.id,
                limit=25,
            )

        except Exception:
            return []

        seen = set()
        choices = []

        for song in songs:
            name = f"{song.artist} - {song.title}"

            if name in seen:
                continue

            seen.add(name)

            key = uuid.uuid4().hex[:8]

            self.autocomplete_cache[key] = song

            choices.append(
                app_commands.Choice(
                    name=name[:100],
                    value=key,
                )
            )

            if len(choices) == 25:
                break

        return choices
    @app_commands.command(
        name="play",
        description="Play a song.",
    )
    @app_commands.describe(
        query="Song name or URL"
    )
    @app_commands.autocomplete(
        query=play_autocomplete
    )
    
    async def play(
        self,
        interaction: discord.Interaction,
        query: str,
    ):
        try:

            if query in self.autocomplete_cache:
                song = self.autocomplete_cache.pop(query)

                played = await self.music.play(
                    interaction,
                    song,
                )

                if played:
                    await interaction.response.send_message(
                        f"▶️ Now playing **{song.title}**",
                        ephemeral=True,
                    )
                else:
                    await interaction.response.send_message(
                        f"➕ Added **{song.title}** to the queue.",
                        ephemeral=True,
                    )

                return

            # Spotify track
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
        name="playnext",
        description="Play a song next.",
    )
    @app_commands.describe(
        query="Song name or URL"
    )
    @app_commands.autocomplete(
        query=play_autocomplete
    )
    async def playnext(
        self,
        interaction: discord.Interaction,
        query: str,
    ):
        try:

            if query in self.autocomplete_cache:
                song = self.autocomplete_cache.pop(query)

                played = await self.music.playnext(
                    interaction,
                    song,
                )

                if played:
                    await interaction.response.send_message(
                        f"▶️ Now playing **{song.title}**",
                        ephemeral=True,
                    )
                else:
                    await interaction.response.send_message(
                        f"➕ Added **{song.title}** to the queue.",
                        ephemeral=True,
                    )

                return

            # Spotify track
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
                    view=SearchView(
                        songs,
                        play_next=True
                    ),
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

                        await self.music.playnext(
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
                view=SearchView(
                    songs,
                    play_next=True
                ),
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


    @playlist.command(
        name="import",
        description="Import Spotify playlist from pasted track links.",
    )
    @app_commands.describe(
        tracks="Paste Spotify track links (one per line)"
    )
    async def playlist_import(
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

    async def playlist_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        playlists = self.playlists.list_playlists(
            interaction.user.id
        )

        return [
            app_commands.Choice(
                name=name,
                value=name,
            )
            for name in playlists
            if current.lower() in name.lower()
        ][:25]
    
    @playlist.command(
    name="play",
    description="Play one of your saved playlists.",
)
    @app_commands.describe(
        name="Playlist name"
    )
    @app_commands.autocomplete(
        name=playlist_autocomplete
    )
    async def playlist_play(
        self,
        interaction: discord.Interaction,
        name: str,
    ):
        songs = self.playlists.get_playlist(
            interaction.user.id,
            name,
        )

        if songs is None:
            await interaction.response.send_message(
                "❌ Playlist not found.",
                ephemeral=True,
            )
            return

        await interaction.response.defer()

        await self.music.join(
            interaction
        )

        added = 0

        for entry in songs:
            try:
                song = await self.lavalink.search(
                    f"{entry['title']} {entry['artist']}",
                    interaction.user.id,
                )

                await self.music.play(
                    interaction,
                    song,
                )

                added += 1

            except Exception:
                continue

        await interaction.followup.send(
            f"📀 Added **{added}** songs from **{name}**."
        )

    @playlist.command(
        name="list",
        description="View your saved playlists.",
    )
    async def playlist_list(
        self,
        interaction: discord.Interaction,
    ):
        playlists = self.playlists.list_playlists(
            interaction.user.id
        )

        if not playlists:
            await interaction.response.send_message(
                "📂 You don't have any saved playlists.",
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            title="📀 Your Playlists",
            color=discord.Color.blurple(),
        )

        for name in playlists:
            songs = self.playlists.get_playlist(
                interaction.user.id,
                name,
            )

            embed.add_field(
                name=name,
                value=f"🎵 {len(songs)} songs",
                inline=False,
            )

        embed.set_footer(
            text=f"{len(playlists)} playlist(s)"
        )

        await interaction.response.send_message(
            embed=embed
        )

    @playlist.command(
        name="delete",
        description="Delete one of your saved playlists.",
    )
    @app_commands.describe(
        name="Playlist name",
    )
    @app_commands.autocomplete(
        name=playlist_autocomplete,
    )
    async def playlist_delete(
        self,
        interaction: discord.Interaction,
        name: str,
    ):
        success = self.playlists.delete_playlist(
            interaction.user.id,
            name,
        )

        if not success:
            await interaction.response.send_message(
                "❌ Playlist not found.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"🗑️ Deleted **{name}**.",
        )

    @app_commands.command(
    name="lyrics",
    description="Show lyrics for the current song.",
)
    async def lyrics(
        self,
        interaction: discord.Interaction,
    ):

        await interaction.response.defer()

        state = self.music.get_state(
            interaction.guild.id
        )

        if state.current is None:
            await interaction.followup.send(
                "❌ Nothing is currently playing.",
                ephemeral=True,
            )
            return

        try:
            data = await self.bot.lyrics.search(
                state.current.artist,
                state.current.title,
            )

        except Exception as e:
            import traceback

            print("=== LYRICS ERROR ===")
            traceback.print_exc()

            await interaction.followup.send(
                f"❌ Exception:\n```{e}```",
                ephemeral=True,
            )
            return

        if data is None:
            await interaction.followup.send(
                "❌ Lyrics not found.",
                ephemeral=True,
            )
            return

        lyrics = (
            data.get("plainLyrics")
            or data.get("syncedLyrics")
        )

        if not lyrics:
            await interaction.followup.send(
                "❌ Lyrics not found.",
                ephemeral=True,
            )
            return

        chunks = [
            lyrics[i:i + 4000]
            for i in range(
                0,
                len(lyrics),
                4000,
            )
        ]

        embeds = []

        for index, chunk in enumerate(chunks):
            embed = discord.Embed(
                title=(
                    f"🎤 {state.current.title}"
                    if index == 0
                    else None
                ),
                description=chunk,
                color=0x5865F2,
            )

            if index == 0:
                embed.set_author(
                    name=state.current.artist
                )

            embed.set_footer(
                text=f"Page {index + 1}/{len(chunks)}"
            )

            embeds.append(embed)

        await interaction.followup.send(
            embeds=embeds
        )

async def setup(bot):
    await bot.add_cog(
        Music(bot)
    )