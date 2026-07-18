import discord


def make_embed(category: str):
    embed = discord.Embed(color=discord.Color.orange())

    if category == "home":
        embed.title = "📖 DJ U BEE Help"
        embed.description = (
            "Welcome to **DJ U BEE v3**! 🐝\n\n"
            "Browse the categories below to discover commands and features.\n\n"
            "Need help with music, playlists, Last.fm or statistics?\n"
            "Simply click one of the buttons below."
        )

    elif category == "music":
        embed.title = "🎵 Music Commands"
        embed.description = (
            "**`/play <song>`**\n"
            "Play a song from YouTube or Spotify.\n\n"

            "**`/playnext <song>`**\n"
            "Queue a song to play immediately after the current track.\n\n"

            "**`/lyrics`**\n"
            "Display lyrics for the currently playing song."
        )

    elif category == "playback":
        embed.title = "🎛 Playback Controls"
        embed.description = (
            "**`Pause`**\n"
            "Pause or resume playback.\n\n"

            "**`Skip`**\n"
            "Skip the current song.\n\n"

            "**`Shuffle`**\n"
            "Randomize the current queue.\n\n"

            "**`Loop`**\n"
            "Switch between Off, Track and Queue looping.\n\n"

            "**Stop**\n"
            "Click on the stop button while a song is playing to stop the playback\n\n"

            "**Seek Controls**\n"
            "Use the player buttons to jump forward or backward in the current song."
        )

    elif category == "lastfm":
        embed.title = "🎼 Last.fm"
        embed.description = (
            "**`/login`**\n"
            "Connect your Last.fm account.\n\n"

            "**`/logout`**\n"
            "Disconnect your Last.fm account.\n\n"

            "**`/profile`**\n"
            "View your linked Last.fm profile."
        )

    elif category == "playlist":
        embed.title = "🎧 Playlist Commands"
        embed.description = (

            "**`/playlist save`**\n"
            "Create a new playlist and save it to DJ U BEE for further playbacks!\n\n"

            "**`/playlist play`**\n"
            "Load one of your saved playlists.\n\n"

            "**`/playlist import`**\n"
            "Import a Spotify playlist as track links.\n\n"

            "**`/playlist list`**\n"
            "View all of your saved playlists.\n\n"

            "**`/playlist delete`**\n"
            "Delete one of your playlists."
        )

    elif category == "stats":
        embed.title = "📊 Listening Statistics"
        embed.description = (
            "**`/stats`**\n"
            "View your listening statistics including total listening time, songs played, top artists and top tracks."
        )

    elif category == "about":
        embed.title = "🐝 About DJ U BEE"
        embed.description = (
            "**DJ U BEE v3**\n\n"
            "A modern Discord music bot built with **discord.py**, **Wavelink**, and **Lavalink**.\n\n"
            "**Features**\n"
            "• Interactive music player\n"
            "• Spotify integration\n"
            "• Last.fm scrobbling\n"
            "• Lyrics\n"
            "• Personal playlists\n"
            "• Listening statistics"
        )

    embed.set_footer(text="DJ U BEE v3 • Use /help anytime")
    return embed


class HelpView(discord.ui.View):
    def __init__(self, category: str = "home"):
        super().__init__(timeout=None)

        self.category = category

        self.add_item(MusicButton())
        self.add_item(PlaybackButton())
        self.add_item(LastFMButton())
        self.add_item(PlaylistButton())
        self.add_item(StatsButton())
        self.add_item(AboutButton())

        if category != "home":
            self.add_item(HomeButton())


class MusicButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="🎵 Music", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=make_embed("music"),
            view=HelpView("music"),
        )


class PlaybackButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="🎛 Playback", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=make_embed("playback"),
            view=HelpView("playback"),
        )


class LastFMButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="🎼 Last.fm", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=make_embed("lastfm"),
            view=HelpView("lastfm"),
        )


class PlaylistButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="🎧 Playlists", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=make_embed("playlist"),
            view=HelpView("playlist"),
        )


class StatsButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="📊 Stats", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=make_embed("stats"),
            view=HelpView("stats"),
        )


class AboutButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="ℹ️ About", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=make_embed("about"),
            view=HelpView("about"),
        )


class HomeButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="⬅ Home",
            style=discord.ButtonStyle.primary,
            row=1,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=make_embed("home"),
            view=HelpView("home"),
        )