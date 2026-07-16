import asyncio
import webbrowser

from oauth.callback_server import (
    SpotifyCallbackServer,
)
from oauth.spotify_oauth import (
    SpotifyOAuth,
)


async def main():
    oauth = SpotifyOAuth()

    server = SpotifyCallbackServer()

    await server.start()

    url = oauth.get_login_url()

    print("\nOpen this URL if it doesn't open automatically:\n")
    print(url)

    webbrowser.open(url)

    print("\nWaiting for Spotify login...\n")

    while server.code is None:
        await asyncio.sleep(0.5)

    if server.state != oauth.state:
        print("State mismatch!")

        await server.stop()

        return

    tokens = await oauth.exchange_code(
        server.code
    )

    oauth.save_refresh_token(
        tokens["refresh_token"]
    )

    print(
        "\n✅ Spotify linked successfully!"
    )

    await server.stop()


asyncio.run(main())