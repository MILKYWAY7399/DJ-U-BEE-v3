import json
from pathlib import Path


class PlaylistProvider:
    def __init__(self):
        self.path = Path("storage/playlists.json")

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.path.exists():
            self.path.write_text(
                "{}",
                encoding="utf-8",
            )

        self.data = self.load()

    def load(self) -> dict:
        with open(
            self.path,
            "r",
            encoding="utf-8",
        ) as f:
            return json.load(f)

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
                ensure_ascii=False,
            )

    def create_playlist(
        self,
        user_id: int,
        name: str,
        songs: list[dict],
    ) -> bool:
        user_id = str(user_id)

        if user_id not in self.data:
            self.data[user_id] = {}

        if name in self.data[user_id]:
            return False

        self.data[user_id][name] = songs
        self.save()

        return True

    def get_playlist(
        self,
        user_id: int,
        name: str,
    ) -> list[dict] | None:
        return (
            self.data
            .get(str(user_id), {})
            .get(name)
        )

    def list_playlists(
        self,
        user_id: int,
    ) -> list[str]:
        return list(
            self.data.get(
                str(user_id),
                {},
            ).keys()
        )

    def delete_playlist(
        self,
        user_id: int,
        name: str,
    ) -> bool:
        user_id = str(user_id)

        if (
            user_id not in self.data
            or name not in self.data[user_id]
        ):
            return False

        del self.data[user_id][name]

        self.save()

        return True