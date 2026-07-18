import discord


class BackButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Back",
            emoji="🏠",
            style=discord.ButtonStyle.primary,
            row=2,
        )

    async def callback(
        self,
        interaction: discord.Interaction,
    ):
        # Local import to avoid circular import
        from ui.player_view import PlayerView

        state = interaction.client.music.get_state(
            interaction.guild.id
        )

        await interaction.response.edit_message(
            content=None,
            view=PlayerView(
                enabled=state.current is not None,
            ),
        )


class SeekView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(BackButton())

    async def _seek(
        self,
        interaction: discord.Interaction,
        offset: int,
    ):
        success = await interaction.client.music.seek(
            interaction.guild.id,
            offset,
        )

        if success:
            await interaction.response.defer()
        else:
            await interaction.response.send_message(
                "❌ Nothing is playing.",
                ephemeral=True,
            )

    @discord.ui.button(
        label="-30s",
        style=discord.ButtonStyle.secondary,
    )
    async def minus30(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await self._seek(
            interaction,
            -30000,
        )

    @discord.ui.button(
        label="-10s",
        style=discord.ButtonStyle.secondary,
    )
    async def minus10(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await self._seek(
            interaction,
            -10000,
        )

    @discord.ui.button(
        label="-5s",
        style=discord.ButtonStyle.secondary,
    )
    async def minus5(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await self._seek(
            interaction,
            -5000,
        )

    @discord.ui.button(
        label="+5s",
        style=discord.ButtonStyle.secondary,
    )
    async def plus5(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await self._seek(
            interaction,
            5000,
        )

    @discord.ui.button(
        label="+10s",
        style=discord.ButtonStyle.secondary,
    )
    async def plus10(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await self._seek(
            interaction,
            10000,
        )

    @discord.ui.button(
        label="+30s",
        style=discord.ButtonStyle.secondary,
    )
    async def plus30(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await self._seek(
            interaction,
            30000,
        )