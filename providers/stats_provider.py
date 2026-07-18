import json
from pathlib import Path


class StatsProvider:
    def __init__(self):
        self.path = Path("storage/stats.json")

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if self.path.exists():
            with open(
                self.path,
                "r",
                encoding="utf-8",
            ) as f:
                self.data = json.load(f)
        else:
            self.data = {
                "guilds": {}
            }
            self.save()

    def save(self):
        with open(
            self.path,
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                self.data,
                f,
                indent=4,
            )

    def record_play(
        self,
        guild_id: int,
        user_id: int,
        song,
    ):
        guild = self.data["guilds"].setdefault(
            str(guild_id),
            {
                "users": {},
                "songs": {},
                "artists": {},
            },
        )

        user = guild["users"].setdefault(
            str(user_id),
            {
                "songs_played": 0,
                "listening_time": 0,
                "songs": {},
                "artists": {},
            },
        )

        user["songs_played"] += 1
        user["listening_time"] += song.duration

        user["songs"][song.title] = (
            user["songs"].get(
                song.title,
                0,
            )
            + 1
        )

        user["artists"][song.artist] = (
            user["artists"].get(
                song.artist,
                0,
            )
            + 1
        )

        guild["songs"][song.title] = (
            guild["songs"].get(
                song.title,
                0,
            )
            + 1
        )

        guild["artists"][song.artist] = (
            guild["artists"].get(
                song.artist,
                0,
            )
            + 1
        )

        self.save()

    def get_user_stats(
        self,
        guild_id: int,
        user_id: int,
    ):
        guild = self.data["guilds"].get(str(guild_id))

        if guild is None:
            return None

        return guild["users"].get(str(user_id))


    def format_time(
        self,
        milliseconds: int,
    ):
        seconds = milliseconds // 1000

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        return f"{hours}h {minutes}m"