import json
from pathlib import Path


class SettingsProvider:
    def __init__(self):
        self.path = Path("storage/settings.json")

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.path.exists():
            self.path.write_text("{}")

        self.data = json.loads(
            self.path.read_text()
        )

    def save(self):
        self.path.write_text(
            json.dumps(
                self.data,
                indent=4,
            )
        )

    def get_radio(
        self,
        guild_id: int,
    ) -> bool:
        guild = self.data.setdefault(
            str(guild_id),
            {}
        )

        return guild.get(
            "radio",
            True,
        )

    def set_radio(
        self,
        guild_id: int,
        enabled: bool,
    ):
        guild = self.data.setdefault(
            str(guild_id),
            {}
        )

        guild["radio"] = enabled

        self.save()