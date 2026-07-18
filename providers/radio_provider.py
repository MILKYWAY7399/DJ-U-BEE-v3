import random

from models.song import Song


class RadioProvider:
    def __init__(self, lavalink):
        self.lavalink = lavalink

    async def recommend(
        self,
        current: Song,
    ):
        query = f"{current.title} {current.artist}"

        results = await self.lavalink.search_many(
            query,
            current.requester_id,
            limit=10,
        )

        songs = [
            song
            for song in results
            if (
                song.title.lower() != current.title.lower()
                or song.artist.lower() != current.artist.lower()
            )
        ]

        if not songs:
            return None

        return random.choice(songs)