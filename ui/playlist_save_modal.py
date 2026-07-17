import discord


class PlaylistSaveModal(discord.ui.Modal, title="Save Playlist"):
    def __init__(self, cog):
        super().__init__()

        self.cog = cog

        self.name = discord.ui.TextInput(
            label="Playlist Name",
            placeholder="Workout",
            max_length=50,
        )

        self.songs = discord.ui.TextInput(
            label="Songs",
            placeholder=(
                "One song per line\n"
                "Supports Spotify links and song names."
            ),
            style=discord.TextStyle.paragraph,
            max_length=4000,
        )

        self.add_item(self.name)
        self.add_item(self.songs)

    async def on_submit(
        self,
        interaction: discord.Interaction,
    ):
        entries = [
            line.strip()
            for line in self.songs.value.splitlines()
            if line.strip()
        ]

        if not entries:
            await interaction.response.send_message(
                "❌ No songs provided.",
                ephemeral=True,
            )
            return

        songs = []

        await interaction.response.defer(
            ephemeral=True,
        )

        for entry in entries:
            try:
                if "open.spotify.com/track/" in entry:
                    title, artist = (
                        await self.cog.spotify.get_track(
                            entry
                        )
                    )
                else:
                    result = await self.cog.lavalink.search(
                        entry,
                        interaction.user.id,
                    )

                    title = result.title
                    artist = result.artist

                songs.append(
                    {
                        "title": title,
                        "artist": artist,
                    }
                )

            except Exception:
                continue

        if not songs:
            await interaction.followup.send(
                "❌ Couldn't resolve any songs.",
                ephemeral=True,
            )
            return

        created = self.cog.playlists.create_playlist(
            interaction.user.id,
            self.name.value,
            songs,
        )

        if not created:
            await interaction.followup.send(
                "❌ You already have a playlist with that name.",
                ephemeral=True,
            )
            return

        await interaction.followup.send(
            f"✅ Saved **{self.name.value}** with **{len(songs)}** songs.",
            ephemeral=True,
        )