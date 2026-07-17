from aiohttp import web


class CallbackServer:
    def __init__(self):
        self.code = None
        self.state = None

        self.app = web.Application()

        self.app.router.add_get(
            "/callback",
            self.callback,
        )

        self.runner = web.AppRunner(
            self.app
        )

    async def start(
        self,
    ):
        await self.runner.setup()

        site = web.TCPSite(
            self.runner,
            "127.0.0.1",
            8888,
        )

        await site.start()

        print(
            "✅ OAuth server started."
        )

    async def stop(
        self,
    ):
        await self.runner.cleanup()

    async def callback(
        self,
        request: web.Request,
    ):
        self.code = request.query.get(
            "code"
        )

        self.state = request.query.get(
            "state"
        )

        return web.Response(
            text=(
                "You may now close this window."
            )
        )