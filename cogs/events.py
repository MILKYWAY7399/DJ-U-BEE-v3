import wavelink
from discord.ext import commands


class MusicEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_wavelink_track_end(
        self,
        payload: wavelink.TrackEndEventPayload,
    ):
        print("🔥 TRACK END EVENT")

        await self.bot.music.play_next(
            payload.player
        )


async def setup(bot):
    await bot.add_cog(
        MusicEvents(bot)
    )