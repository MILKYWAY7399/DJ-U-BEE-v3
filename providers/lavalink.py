import wavelink

from models.song import Song


class LavalinkProvider:
    async def search(
        self,
        query: str,
        requester_id: int,
    ) -> Song:
        songs = await self.search_many(
            query,
            requester_id,
            limit=1,
        )

        return songs[0]

    async def search_many(
        self,
        query: str,
        requester_id: int,
        limit: int = 5,
    ) -> list[Song]:
        tracks = await wavelink.Playable.search(
            query
        )

        if not tracks:
            raise RuntimeError(
                "No results found."
            )

        songs = []

        for track in tracks[:limit]:
            songs.append(
                Song(
                    track=track,
                    requester_id=requester_id,
                )
            )

        return songs