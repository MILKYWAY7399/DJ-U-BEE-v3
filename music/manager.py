from collections import defaultdict

import discord
import wavelink

from models.song import Song
from music.guild_state import GuildState
from music.loop_mode import LoopMode
from ui.player_view import PlayerView


class MusicManager:
    def __init__(self, bot):
        self.bot = bot

        self.guilds: dict[int, GuildState] = defaultdict(
            GuildState
        )

    def get_state(
        self,
        guild_id: int,
    ) -> GuildState:
        return self.guilds[guild_id]

    async def update_player(
        self,
        guild_id: int,
    ):
        state = self.get_state(guild_id)

        if (
            state.current is None
            or state.text_channel is None
        ):
            return

        song = state.current

        loop_text = {
            LoopMode.OFF: "Off",
            LoopMode.TRACK: "Track",
            LoopMode.QUEUE: "Queue",
        }[state.loop_mode]

        status_text = (
            "⏸ Paused"
            if state.player is not None
            and state.player.paused
            else "▶ Playing"
        )

        embed = discord.Embed(
            title="🎵 DJ U BEE",
            description=(
                f"## {song.title}\n"
                f"**{song.artist}**\n\n"
                f"{status_text}\n"
                f"🔁 **Loop:** {loop_text}"
            ),
            color=0x5865F2,
        )

        if song.thumbnail:
            embed.set_thumbnail(
                url=song.thumbnail
            )

        try:
            if state.player_message is None:
                state.player_message = (
                    await state.text_channel.send(
                        embed=embed,
                        view=PlayerView(),
                    )
                )
            else:
                await state.player_message.edit(
                    embed=embed,
                    view=PlayerView(),
                )

        except discord.NotFound:
            state.player_message = (
                await state.text_channel.send(
                    embed=embed,
                    view=PlayerView(),
                )
            )

    async def join(
        self,
        interaction: discord.Interaction,
    ) -> wavelink.Player:
        if interaction.user.voice is None:
            raise RuntimeError(
                "You must join a voice channel first."
            )

        state = self.get_state(
            interaction.guild.id
        )

        if state.player is not None:
            return state.player

        channel = interaction.user.voice.channel

        player: wavelink.Player = await channel.connect(
            cls=wavelink.Player
        )

        state.player = player

        return player

    async def leave(
        self,
        interaction: discord.Interaction,
    ):
        state = self.get_state(
            interaction.guild.id
        )

        if state.player is None:
            raise RuntimeError(
                "I'm not connected."
            )

        await state.player.disconnect()

        self.guilds.pop(
            interaction.guild.id,
            None,
        )

    async def play(
        self,
        interaction: discord.Interaction,
        song: Song,
    ):
        state = self.get_state(
            interaction.guild.id
        )

        state.text_channel = interaction.channel

        player = state.player

        if player is None:
            player = await self.join(
                interaction
            )

        if player.playing:
            state.queue.append(song)
            return False

        state.current = song

        await player.play(
            song.track
        )

        await self.update_player(
            interaction.guild.id
        )

        return True

    async def play_next(
        self,
        player: wavelink.Player,
    ):
        state = self.get_state(
            player.guild.id
        )

        if state.current is not None:
            if state.loop_mode == LoopMode.TRACK:
                await player.play(
                    state.current.track
                )
                return

            if state.loop_mode == LoopMode.QUEUE:
                state.queue.append(
                    state.current
                )

        if not state.queue:
            state.current = None
            await self.update_player(
                player.guild.id
            )
            return

        next_song = state.queue.pop(0)

        state.current = next_song

        await player.play(
            next_song.track
        )

        await self.update_player(
            player.guild.id
        )

    async def skip(
        self,
        guild_id: int,
    ) -> bool:
        state = self.get_state(
            guild_id
        )

        player = state.player

        if (
            player is None
            or not player.playing
        ):
            return False

        await player.skip()

        return True

    async def pause_resume(
        self,
        guild_id: int,
    ) -> str | None:
        state = self.get_state(
            guild_id
        )

        player = state.player

        if player is None:
            return None

        if player.paused:
            await player.pause(False)
            await self.update_player(
                guild_id
            )
            return "resumed"

        if player.playing:
            await player.pause(True)
            await self.update_player(
                guild_id
            )
            return "paused"

        return None

    def get_queue(
        self,
        guild_id: int,
    ) -> tuple[Song | None, list[Song]]:
        state = self.get_state(
            guild_id
        )

        return (
            state.current,
            state.queue.copy(),
        )

    def cycle_loop_mode(
        self,
        guild_id: int,
    ) -> LoopMode:
        state = self.get_state(
            guild_id
        )

        if state.loop_mode == LoopMode.OFF:
            state.loop_mode = LoopMode.TRACK

        elif state.loop_mode == LoopMode.TRACK:
            state.loop_mode = LoopMode.QUEUE

        else:
            state.loop_mode = LoopMode.OFF

        return state.loop_mode