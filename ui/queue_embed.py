import math
import discord

from music.guild_state import GuildState


SONGS_PER_PAGE = 10


def format_duration(ms: int) -> str:
    total = ms // 1000

    hours = total // 3600
    minutes = (total % 3600) // 60
    seconds = total % 60

    if hours:
        return f"{hours}h {minutes}m"

    return f"{minutes}m {seconds:02}s"


def build_queue_embed(
    bot,
    state: GuildState,
    page: int,
) -> discord.Embed:

    current = state.current
    queue = state.queue

    pages = max(
        1,
        math.ceil(len(queue) / SONGS_PER_PAGE),
    )

    page = max(
        0,
        min(page, pages - 1),
    )

    start = page * SONGS_PER_PAGE
    end = start + SONGS_PER_PAGE

    embed = discord.Embed(
        title=f"🎵 DJ U BEE Queue • Page {page + 1}/{pages}",
        color=0x5865F2,
    )

    if current and current.thumbnail:
        embed.set_thumbnail(
            url=current.thumbnail
        )

    if current:
        embed.add_field(
            name="▶ Now Playing",
            value=(
                f"**{current.title}**\n"
                f"{current.artist}"
            ),
            inline=False,
        )

    if queue:
        lines = []

        for index, song in enumerate(
            queue[start:end],
            start=start + 1,
        ):
            lines.append(
                f"`{index:>2}.` **{song.title}** • {song.artist}"
            )

        embed.add_field(
            name="Up Next",
            value="\n".join(lines),
            inline=False,
        )

    else:
        embed.add_field(
            name="Up Next",
            value="Nothing queued.",
            inline=False,
        )

    remaining = sum(
        song.duration
        for song in queue
    )

    embed.set_footer(
        text=(
            f"📜 {len(queue)} songs   •   "
            f"⏱ {format_duration(remaining)} remaining   •   "
            f"Page {page + 1}/{pages}"
        )
    )

    return embed