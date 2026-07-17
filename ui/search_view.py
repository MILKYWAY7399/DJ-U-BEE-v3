import discord

from models.song import Song


class SongSelect(discord.ui.Select):
    def __init__(
        self,
        songs: list[Song],
        play_next: bool = False,
    ):
        self.songs = songs
        self.play_next = play_next

        options = []

        for i, song in enumerate(songs):
            options.append(
                discord.SelectOption(
                    label=song.title[:100],
                    description=song.artist[:100],
                    value=str(i),
                )
            )

        super().__init__(
            placeholder="Choose a song...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(
        self,
        interaction: discord.Interaction,
    ):
        song = self.songs[
            int(self.values[0])
        ]

        if self.play_next:
            await interaction.client.music.playnext(
                interaction,
                song,
            )
        else:
            await interaction.client.music.play(
                interaction,
                song,
            )

        await interaction.response.edit_message(
            content=f"🎵 **{song.title}** selected.",
            embed=None,
            view=None,
        )


class SearchView(discord.ui.View):
    def __init__(
        self,
        songs: list[Song],
        play_next: bool = False,
    ):
        super().__init__(
            timeout=60
        )

        self.add_item(
            SongSelect(
                songs,
                play_next,
            )
        )