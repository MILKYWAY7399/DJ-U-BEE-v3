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

if not DISCORD_TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN not found."
    )