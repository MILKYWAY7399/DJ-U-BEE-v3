import wavelink

from models.song import Song


class LavalinkProvider:
    async def search(
        self,
        query: str,
        requester_id: int,
    ) -> Song:
        tracks = await wavelink.Playable.search(
            query
        )

        if not tracks:
            raise RuntimeError(
                "No results found."
            )

        return Song(
            track=tracks[0],
            requester_id=requester_id,
        )