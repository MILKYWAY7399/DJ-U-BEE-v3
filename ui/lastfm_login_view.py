import discord

from providers.lastfm import LastFMProvider


class LastFMAuthorizedButton(discord.ui.Button):
    def __init__(
        self,
        provider: LastFMProvider,
    ):
        super().__init__(
            label="I've Authorized",
            style=discord.ButtonStyle.success,
        )

        self.provider = provider

    async def callback(
        self,
        interaction: discord.Interaction,
    ):
        try:
            username = await self.provider.finish_login(
                interaction.user.id
            )

            if self.view is None:
                return

            for item in self.view.children:
                item.disabled = True

            await interaction.response.edit_message(
                content=(
                    f"✅ Successfully linked **{username}**.\n\n"
                    "Your Last.fm account is now connected to DJ U BEE."
                ),
                view=self.view,
            )

        except Exception as e:
            await interaction.response.send_message(
                f"❌ {e}",
                ephemeral=True,
            )


class LastFMLoginView(discord.ui.View):
    def __init__(
        self,
        provider: LastFMProvider,
        login_url: str,
    ):
        super().__init__(timeout=600)

        self.add_item(
            discord.ui.Button(
                label="Authorize Last.fm",
                url=login_url,
            )
        )

        self.add_item(
            LastFMAuthorizedButton(provider)
        )