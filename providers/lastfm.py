import hashlib

import aiohttp

from config import (
    LASTFM_API_KEY,
    LASTFM_SHARED_SECRET,
)

from storage.lastfm_sessions import (
    LastFMSessionStorage,
)


class LastFMProvider:
    def __init__(self):
        self.api_key = LASTFM_API_KEY
        self.shared_secret = LASTFM_SHARED_SECRET

        self.storage = LastFMSessionStorage()
        self.pending_tokens: dict[int, str] = {}

    async def get_login_url(
        self,
    ) -> tuple[str, str]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://ws.audioscrobbler.com/2.0/",
                params={
                    "method": "auth.getToken",
                    "api_key": self.api_key,
                    "format": "json",
                },
            ) as response:

                data = await response.json()

                if response.status != 200:
                    print(data)

                    raise RuntimeError(
                        "Failed to get Last.fm auth token."
                    )

                token = data["token"]

                url = (
                    "https://www.last.fm/api/auth/"
                    f"?api_key={self.api_key}"
                    f"&token={token}"
                )

                return url, token

    async def get_session(
        self,
        token: str,
    ) -> dict:

        api_sig = hashlib.md5(
            (
                f"api_key{self.api_key}"
                f"methodauth.getSession"
                f"token{token}"
                f"{self.shared_secret}"
            ).encode("utf-8")
        ).hexdigest()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://ws.audioscrobbler.com/2.0/",
                params={
                    "method": "auth.getSession",
                    "api_key": self.api_key,
                    "token": token,
                    "api_sig": api_sig,
                    "format": "json",
                },
            ) as response:

                data = await response.json()

                if response.status != 200:
                    print(data)

                    raise RuntimeError(
                        "Failed to get Last.fm session."
                    )

                return data["session"]
            

    async def update_now_playing(
        self,
        user_id: int,
        artist: str,
        track: str,
    ):
        user = self.storage.get(user_id)

        if user is None:
            return

        session_key = user["session_key"]

        api_sig = hashlib.md5(
            (
                f"api_key{self.api_key}"
                f"artist{artist}"
                f"methodtrack.updateNowPlaying"
                f"sk{session_key}"
                f"track{track}"
                f"{self.shared_secret}"
            ).encode("utf-8")
        ).hexdigest()

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://ws.audioscrobbler.com/2.0/",
                data={
                    "method": "track.updateNowPlaying",
                    "artist": artist,
                    "track": track,
                    "api_key": self.api_key,
                    "sk": session_key,
                    "api_sig": api_sig,
                    "format": "json",
                },
            ) as response:

                if response.status != 200:
                    print(
                        "Last.fm Now Playing failed:",
                        await response.text(),
                    )


    async def scrobble(
        self,
        user_id: int,
        artist: str,
        track: str,
        timestamp: int,
    ):
        user = self.storage.get(user_id)

        if user is None:
            return

        session_key = user["session_key"]

        api_sig = hashlib.md5(
            (
                f"api_key{self.api_key}"
                f"artist{artist}"
                f"methodtrack.scrobble"
                f"sk{session_key}"
                f"timestamp{timestamp}"
                f"track{track}"
                f"{self.shared_secret}"
            ).encode("utf-8")
        ).hexdigest()

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://ws.audioscrobbler.com/2.0/",
                data={
                    "method": "track.scrobble",
                    "artist": artist,
                    "track": track,
                    "timestamp": timestamp,
                    "api_key": self.api_key,
                    "sk": session_key,
                    "api_sig": api_sig,
                    "format": "json",
                },
            ) as response:

                if response.status != 200:
                    print(
                        "Last.fm Scrobble failed:",
                        await response.text(),
                    )

    async def get_profile(
        self,
        user_id: int,
    ):
        user = self.storage.get(user_id)

        if user is None:
            return None

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://ws.audioscrobbler.com/2.0/",
                params={
                    "method": "user.getInfo",
                    "user": user["username"],
                    "api_key": self.api_key,
                    "format": "json",
                },
            ) as response:
                data = await response.json()

        return data["user"]

    async def get_recent_track(
        self,
        user_id: int,
    ):
        user = self.storage.get(user_id)

        if user is None:
            return None

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://ws.audioscrobbler.com/2.0/",
                params={
                    "method": "user.getRecentTracks",
                    "user": user["username"],
                    "limit": 1,
                    "api_key": self.api_key,
                    "format": "json",
                },
            ) as response:
                data = await response.json()

        tracks = data["recenttracks"]["track"]

        if not tracks:
            return None

        return tracks[0]

    async def create_login(
        self,
        user_id: int,
    ) -> str:
        url, token = await self.get_login_url()

        self.pending_tokens[user_id] = token

        return url
    
    async def finish_login(
        self,
        user_id: int,
    ) -> str:

        token = self.pending_tokens.get(user_id)

        if token is None:
            raise RuntimeError(
                "No pending login found."
            )

        session = await self.get_session(token)

        self.storage.set(
            user_id,
            session["name"],
            session["key"],
        )

        self.pending_tokens.pop(user_id, None)

        return session["name"]

    def logout(
        self,
        user_id: int,
    ):
        self.storage.remove(user_id)

    def get_username(
        self,
        user_id: int,
    ) -> str | None:
        user = self.storage.get(user_id)

        if user is None:
            return None

        return user["username"]

    def is_logged_in(
        self,
        user_id: int,
    ) -> bool:
        return self.storage.get(user_id) is not None

    def get_user(
        self,
        user_id: int,
    ) -> dict | None:
        return self.storage.get(user_id)


    def save_user(
        self,
        user_id: int,
        username: str,
        session_key: str,
    ):
        self.storage.set(
            user_id,
            username,
            session_key,
        )


    def remove_user(
        self,
        user_id: int,
    ):
        self.storage.remove(user_id)


    def add_pending_token(
        self,
        user_id: int,
        token: str,
    ):
        self.pending_tokens[user_id] = token


    def get_pending_token(
        self,
        user_id: int,
    ) -> str | None:
        return self.pending_tokens.get(user_id)


    def remove_pending_token(
        self,
        user_id: int,
    ):
        self.pending_tokens.pop(user_id, None)