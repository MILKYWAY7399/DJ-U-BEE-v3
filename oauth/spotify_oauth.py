import json
import secrets
from pathlib import Path
from urllib.parse import urlencode

import aiohttp

from config import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
)

REDIRECT_URI = (
    "http://127.0.0.1:8888/callback"
)


class SpotifyOAuth:
    def __init__(self):
        self.client_id = (
            SPOTIFY_CLIENT_ID
        )

        self.client_secret = (
            SPOTIFY_CLIENT_SECRET
        )

        self.state = secrets.token_urlsafe(
            32
        )

    def get_login_url(
        self,
    ) -> str:
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": REDIRECT_URI,
            "state": self.state,
            "scope": (
                "playlist-read-private "
                "playlist-read-collaborative"
            ),
        }

        return (
            "https://accounts.spotify.com/authorize?"
            + urlencode(params)
        )

    async def exchange_code(
        self,
        code: str,
    ):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://accounts.spotify.com/api/token",
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": REDIRECT_URI,
                },
                auth=aiohttp.BasicAuth(
                    self.client_id,
                    self.client_secret,
                ),
            ) as response:

                data = await response.json()

                if response.status != 200:
                    print(data)

                    raise RuntimeError(
                        "Failed to exchange code."
                    )

                return data

    def save_refresh_token(
        self,
        refresh_token: str,
    ):
        path = Path(
            "storage/spotify_token.json"
        )

        path.parent.mkdir(
            exist_ok=True
        )

        with path.open(
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                {
                    "refresh_token": refresh_token
                },
                f,
                indent=4,
            )

    def load_refresh_token(
        self,
    ) -> str | None:
        path = Path(
            "storage/spotify_token.json"
        )

        if not path.exists():
            return None

        with path.open(
            encoding="utf-8",
        ) as f:
            data = json.load(f)

        return data.get(
            "refresh_token"
        )