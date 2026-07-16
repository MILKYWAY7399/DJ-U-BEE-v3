import discord

from music.guild_state import GuildState
from music.loop_mode import LoopMode


def build_player_embed(
    bot,
    state: GuildState,
) -> discord.Embed:
    song = state.current

    if song is None:
        return discord.Embed(
            title="🎵 DJ U BEE",
            description="Nothing is playing.",
            color=0x5865F2,
        )

    minutes = song.duration // 60000
    seconds = (
        song.duration % 60000
    ) // 1000

    duration = (
        f"{minutes}:{seconds:02}"
    )

    queue_count = len(
        state.queue
    )

    requester = bot.get_user(
        song.requester_id
    )

    requester_name = (
        requester.display_name
        if requester
        else f"<@{song.requester_id}>"
    )

    loop_text = {
        LoopMode.OFF: "Off",
        LoopMode.TRACK: "Track",
        LoopMode.QUEUE: "Queue",
    }[state.loop_mode]

    status_text = (
        "⏸ Paused"
        if state.player
        and state.player.paused
        else "▶ Playing"
    )

    embed = discord.Embed(
        title="🎵 DJ U BEE",
        description=(
            f"## {song.title}\n"
            f"**{song.artist}**\n\n"
            f"{status_text}\n"
            f"⏱ **Duration:** {duration}\n"
            f"👤 **Requested by:** {requester_name}\n"
            f"📜 **Queue:** {queue_count} song(s)\n"
            f"🔁 **Loop:** {loop_text}"
        ),
        color=0x5865F2,
    )

    if song.thumbnail:
        embed.set_thumbnail(
            url=song.thumbnail
        )

    return embed