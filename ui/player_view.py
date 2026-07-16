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
        result = await interaction.client.music.pause_resume(
            interaction.guild.id
        )

        if result is None:
            await interaction.response.send_message(
                "❌ Nothing is playing.",
                ephemeral=True,
            )
            return

        if result == "paused":
            self.emoji = "▶️"
            message = "⏸ Paused."
        else:
            self.emoji = "⏸"
            message = "▶️ Resumed."

        await interaction.response.edit_message(
            view=self.view
        )

        await interaction.followup.send(
            message,
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
        success = await interaction.client.music.skip(
            interaction.guild.id
        )

        if success:
            await interaction.response.send_message(
                "⏭ Skipped.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "❌ Nothing to skip.",
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