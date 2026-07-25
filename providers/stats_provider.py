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

            self.migrate_if_needed()

            self.data.setdefault("users", {})
            self.data.setdefault("guilds", {})
        else:
            self.data = {
                "users": {},
                "guilds": {},
            }
            self.save()


    def migrate_if_needed(self):
        # Already using the new format
        if "users" in self.data:
            return

        old_guilds = self.data.get("guilds", {})

        new_data = {
            "users": {},
            "guilds": {},
        }

        for guild_id, guild_data in old_guilds.items():

            new_data["guilds"][guild_id] = {
                "songs_played": sum(
                    user["songs_played"]
                    for user in guild_data["users"].values()
                ),
                "listening_time": sum(
                    user["listening_time"]
                    for user in guild_data["users"].values()
                ),
                "songs": dict(guild_data["songs"]),
                "artists": dict(guild_data["artists"]),
            }

            for user_id, user_stats in guild_data["users"].items():

                user = new_data["users"].setdefault(
                    user_id,
                    {
                        "songs_played": 0,
                        "listening_time": 0,
                        "songs": {},
                        "artists": {},
                        "guilds": {},
                    },
                )

                user["songs_played"] += user_stats["songs_played"]
                user["listening_time"] += user_stats["listening_time"]

                for song, plays in user_stats["songs"].items():
                    user["songs"][song] = (
                        user["songs"].get(song, 0) + plays
                    )

                for artist, plays in user_stats["artists"].items():
                    user["artists"][artist] = (
                        user["artists"].get(artist, 0) + plays
                    )

                user["guilds"][guild_id] = {
                    "songs_played": user_stats["songs_played"],
                    "listening_time": user_stats["listening_time"],
                    "songs": dict(user_stats["songs"]),
                    "artists": dict(user_stats["artists"]),
                }

        self.data = new_data
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
        user = self.data["users"].setdefault(
            str(user_id),
            {
                "songs_played": 0,
                "listening_time": 0,
                "songs": {},
                "artists": {},
                "guilds": {},
            },
        )
        guild = self.data["guilds"].setdefault(
            str(guild_id),
            {
                "songs_played": 0,
                "listening_time": 0,
                "songs": {},
                "artists": {},
            },
        )

        guild_user = user["guilds"].setdefault(
            str(guild_id),
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

        guild_user["songs_played"] += 1
        guild_user["listening_time"] += song.duration

        guild_user["songs"][song.title] = (
            guild_user["songs"].get(song.title, 0) + 1
        )

        guild_user["artists"][song.artist] = (
            guild_user["artists"].get(song.artist, 0) + 1
        )

        guild["songs_played"] += 1
        guild["listening_time"] += song.duration
        
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

    def get_global_user_stats(
        self,
        user_id: int,
    ):
        return self.data["users"].get(str(user_id))

    def get_guild_user_stats(
        self,
        guild_id: int,
        user_id: int,
    ):
        user = self.data["users"].get(str(user_id))

        if user is None:
            return None

        return user["guilds"].get(str(guild_id))


    def format_time(
        self,
        milliseconds: int,
    ):
        seconds = milliseconds // 1000

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        return f"{hours}h {minutes}m"

    def get_guild_stats(
        self,
        guild_id: int,
    ):
        return self.data["guilds"].get(str(guild_id))