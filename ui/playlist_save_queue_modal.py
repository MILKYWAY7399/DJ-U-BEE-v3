import discord


class PlaylistSaveQueueModal(discord.ui.Modal, title="Save Current Queue"):

    name = discord.ui.TextInput(
        label="Playlist Name",
        placeholder="Workout",
        max_length=50,
    )

    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    async def on_submit(
        self,
        interaction: discord.Interaction,
    ):
        state = self.cog.music.get_state(
            interaction.guild.id
        )
        if not state.queue: 
            await interaction.response.send_message(
                "❌ Your queue is empty.",
                ephemeral=True,
            )
            return

        songs = []

        if state.current is not None:
            songs.append(
                {
                    "title": state.current.title,
                    "artist": state.current.artist,
                }
            )

        for song in state.queue:
            songs.append(
                {
                    "title": song.title,
                    "artist": song.artist,
                }
            )

        if not self.cog.playlists.create_playlist(
            interaction.user.id,
            self.name.value,
            songs,
        ):
            await interaction.response.send_message(
                "❌ You already have a playlist with that name.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"💾 Saved **{self.name.value}** with **{len(songs)}** songs."
        )