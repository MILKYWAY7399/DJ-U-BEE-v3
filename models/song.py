from dataclasses import dataclass

import wavelink


@dataclass(slots=True)
class Song:
    track: wavelink.Playable

    requester_id: int

    @property
    def title(self) -> str:
        return self.track.title

    @property
    def artist(self) -> str:
        return self.track.author

    @property
    def duration(self) -> int:
        return self.track.length

    @property
    def thumbnail(self) -> str | None:
        return getattr(
            self.track,
            "artwork",
            None,
        )

    @property
    def url(self) -> str:
        return self.track.uri or ""