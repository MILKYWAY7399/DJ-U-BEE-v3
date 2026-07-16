import time

import aiohttp

from oauth.spotify_oauth import SpotifyOAuth


class SpotifyProvider:
    def __init__(self):
        self.oauth = SpotifyOAuth()

        self.access_token: str | None = None

        self.expires_at = 0

    async def refresh_access_token(
        self,
    ) -> str:
        if (
            self.access_token is not None
            and time.time() < self.expires_at
        ):
            return self.access_token

        refresh_token = (
            self.oauth.load_refresh_token()
        )

        if refresh_token is None:
            raise RuntimeError(
                "Spotify account not linked."
            )

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://accounts.spotify.com/api/token",
                data={
                    "grant_type":
                        "refresh_token",
                    "refresh_token":
                        refresh_token,
                },
                auth=aiohttp.BasicAuth(
                    self.oauth.client_id,
                    self.oauth.client_secret,
                ),
            ) as response:

                data = await response.json()

                if response.status != 200:
                    print(data)

                    raise RuntimeError(
                        "Couldn't refresh Spotify token."
                    )

        self.access_token = data[
            "access_token"
        ]

        self.expires_at = (
            time.time()
            + data["expires_in"]
            - 60
        )

        return self.access_token

    async def api_get(
        self,
        endpoint: str,
    ):
        token = await self.refresh_access_token()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.spotify.com/v1/{endpoint}",
                headers={
                    "Authorization": f"Bearer {token}"
                },
            ) as response:

                if response.status != 200:
                    text = await response.text()

                    print(text)

                    raise RuntimeError(
                        f"Spotify API error ({response.status})"
                    )

                return await response.json()

    async def get_track(
        self,
        url: str,
    ) -> tuple[str, str]:
        track_id = (
            url.split("/track/")[1]
            .split("?")[0]
        )

        data = await self.api_get(
            f"tracks/{track_id}"
        )

        return (
            data["name"],
            data["artists"][0]["name"],
        )

    async def get_album(
        self,
        url: str,
    ) -> list[tuple[str, str]]:
        album_id = (
            url.split("/album/")[1]
            .split("?")[0]
        )

        data = await self.api_get(
            f"albums/{album_id}"
        )

        songs = []

        for track in data["tracks"]["items"]:
            songs.append(
                (
                    track["name"],
                    track["artists"][0]["name"],
                )
            )

        return songs