import discord


class PreviousButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            emoji="⏮",
            style=discord.ButtonStyle.secondary,
        )

    async def callback(
        self,
        interaction: discord.Interaction,
    ):
        await interaction.response.send_message(
            "⏮ Coming soon.",
            ephemeral=True,
        )


class PauseButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            emoji="⏸",
            style=discord.ButtonStyle.primary,
        )

    async def callback(
        self,
        interaction: discord.Interaction,
    ):
        await interaction.response.send_message(
            "⏸ Coming soon.",
            ephemeral=True,
        )


class SkipButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            emoji="⏭",
            style=discord.ButtonStyle.primary,
        )

    async def callback(
        self,
        interaction: discord.Interaction,
    ):
        await interaction.response.send_message(
            "⏭ Coming soon.",
            ephemeral=True,
        )


class LoopButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            emoji="🔁",
            style=discord.ButtonStyle.secondary,
        )

    async def callback(
        self,
        interaction: discord.Interaction,
    ):
        await interaction.response.send_message(
            "🔁 Coming soon.",
            ephemeral=True,
        )


class QueueButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            emoji="📜",
            style=discord.ButtonStyle.secondary,
        )

    async def callback(
        self,
        interaction: discord.Interaction,
    ):
        await interaction.response.send_message(
            "📜 Coming soon.",
            ephemeral=True,
        )


class PlayerView(discord.ui.View):
    def __init__(self):
        super().__init__(
            timeout=None
        )

        self.add_item(PreviousButton())
        self.add_item(PauseButton())
        self.add_item(SkipButton())
        self.add_item(LoopButton())
        self.add_item(QueueButton())