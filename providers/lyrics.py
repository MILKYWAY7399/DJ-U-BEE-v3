import aiohttp
import re

class LyricsProvider:
    BASE_URL = "https://lrclib.net/api"

    def clean_title(
        self,
        title: str,
    ) -> str:
        title = re.sub(
            r"\(.*?(official|lyrics|audio|video|visualizer|live|remaster).*?\)",
            "",
            title,
            flags=re.IGNORECASE,
        )

        title = re.sub(
            r"\[.*?(official|lyrics|audio|video|visualizer|live|remaster).*?\]",
            "",
            title,
            flags=re.IGNORECASE,
        )

        title = re.sub(
            r"-\s*remaster.*",
            "",
            title,
            flags=re.IGNORECASE,
        )

        return " ".join(title.split())

    async def search(
        self,
        artist: str,
        title: str,
    ):
        title = self.clean_title(title)

        async with aiohttp.ClientSession() as session:

            # Exact match
            async with session.get(
                f"{self.BASE_URL}/get",
                params={
                    "artist_name": artist,
                    "track_name": title,
                },
            ) as response:

                if response.status == 200:
                    return await response.json()

            # Fallback search
            async with session.get(
                f"{self.BASE_URL}/search",
                params={
                    "q": f"{artist} {title}",
                },
            ) as response:

                if response.status != 200:
                    return None

                results = await response.json()

                if not results:
                    return None

                return results[0]