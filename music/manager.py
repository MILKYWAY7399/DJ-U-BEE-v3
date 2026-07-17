from collections import defaultdict

import discord
import wavelink
import random
import asyncio
import time

from models.song import Song
from music.guild_state import GuildState
from music.loop_mode import LoopMode
from ui.player_view import PlayerView
from ui.player_embed import build_player_embed

class MusicManager:
    def __init__(self, bot):
        self.bot = bot

        self.guilds: dict[int, GuildState] = defaultdict(
            GuildState
        )

    def push_history(
        self,
        guild_id: int,
    ):
        state = self.get_state(
            guild_id
        )

        if state.current is not None:
            state.history.append(
                state.current
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
        state = self.get_state(
            guild_id
        )

        if state.text_channel is None:
            return

        embed = build_player_embed(
            self.bot,
            state,
        )

        try:
            if state.player_message is None:
                state.player_message = (
                    await state.text_channel.send(
                        embed=embed,
                        view=PlayerView(
                            enabled=state.current is not None
                        ),
                    )
                )
            else:
                await state.player_message.edit(
                    embed=embed,
                    view=PlayerView(
                        enabled=state.current is not None
                    ),
                )

        except discord.NotFound:
            state.player_message = (
                await state.text_channel.send(
                    embed=embed,
                    view=PlayerView(
                        enabled=state.current is not None
                    ),
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

        await self.bot.lastfm.update_now_playing(
            user_id=song.requester_id,
            artist=song.artist,
            track=song.title,
        )

        if state.scrobble_task is not None:
            state.scrobble_task.cancel()

        state.scrobble_task = asyncio.create_task(
            self.schedule_scrobble(
                interaction.guild.id,
                song,
            )
        )

        await self.update_player(
            interaction.guild.id
        )

        return True

    #This method is for /playnext command
    async def playnext(
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
            state.queue.insert(
                0,
                song,
            )

            await self.update_player(
                interaction.guild.id
            )

            return False

        return await self.play(
            interaction,
            song,
        )

    async def schedule_scrobble(
        self,
        guild_id: int,
        song: Song,
    ):
        state = self.get_state(guild_id)

        wait_time = min(
            song.duration / 2000,
            240,
        )

        try:
            await asyncio.sleep(wait_time)

            await self.bot.lastfm.scrobble(
                user_id=song.requester_id,
                artist=song.artist,
                track=song.title,
                timestamp=int(time.time() - wait_time),
            )

        except asyncio.CancelledError:
            pass

    #While this method is for the next button
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

            # Save finished song to history
            self.push_history(
                player.guild.id
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

        await self.bot.lastfm.update_now_playing(
            user_id=next_song.requester_id,
            artist=next_song.artist,
            track=next_song.title,
        )

        if state.scrobble_task is not None:
            state.scrobble_task.cancel()

        state.scrobble_task = asyncio.create_task(
            self.schedule_scrobble(
                player.guild.id,
                next_song,
            )
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

        if state.scrobble_task is not None:
            state.scrobble_task.cancel()

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

    async def previous(
        self,
        guild_id: int,
    ) -> bool:
        state = self.get_state(
            guild_id
        )

        player = state.player

        if (
            player is None
            or not state.history
        ):
            return False

        if state.current is not None:
            state.queue.insert(
                0,
                state.current,
            )

        state.current = state.history.pop()

        await player.play(
            state.current.track
        )

        await self.update_player(
            guild_id
        )

        return True

    async def shuffle(
        self,
        guild_id: int,
    ) -> bool:
        state = self.get_state(
            guild_id
        )

        if len(state.queue) < 2:
            return False

        random.shuffle(
            state.queue
        )

        await self.update_player(
            guild_id
        )

        return True

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

    async def stop(
        self,
        guild_id: int,
    ) -> bool:
        state = self.get_state(
            guild_id
        )

        player = state.player

        if player is None:
            return False

        state.queue.clear()
        state.history.clear()
        state.current = None

        await player.stop()

        await self.update_player(
            guild_id
        )

        return True

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