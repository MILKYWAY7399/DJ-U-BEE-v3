import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

LAVALINK_URI = os.getenv(
    "LAVALINK_URI",
    "http://127.0.0.1:2333",
)

LAVALINK_PASSWORD = os.getenv(
    "LAVALINK_PASSWORD",
    "youshallnotpass",
)

SPOTIFY_CLIENT_ID = os.getenv(
    "SPOTIFY_CLIENT_ID"
)

SPOTIFY_CLIENT_SECRET = os.getenv(
    "SPOTIFY_CLIENT_SECRET"
)

LASTFM_API_KEY = os.getenv(
    "LASTFM_API_KEY"
)

LASTFM_SHARED_SECRET = os.getenv(
    "LASTFM_SHARED_SECRET"
)

if not DISCORD_TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN not found."
    )

if not SPOTIFY_CLIENT_ID:
    raise RuntimeError(
        "SPOTIFY_CLIENT_ID not found."
    )

if not SPOTIFY_CLIENT_SECRET:
    raise RuntimeError(
        "SPOTIFY_CLIENT_SECRET not found."
    )

if not LASTFM_API_KEY:
    raise RuntimeError(
        "LASTFM_API_KEY not found"
    )

if not LASTFM_SHARED_SECRET:
    raise RuntimeError(
        "LASTFM_SHARED_SECRET not found"
    )