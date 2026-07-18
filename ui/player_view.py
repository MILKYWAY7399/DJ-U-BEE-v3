import discord

from music.loop_mode import LoopMode
from ui.queue_embed import build_queue_embed
from ui.queue_view import QueueView
from ui.seek_view import SeekView

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
        success = await interaction.client.music.previous(
            interaction.guild.id
        )

        if success:
            await interaction.response.send_message(
                "⏮ Playing previous song.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "❌ No previous song.",
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
        mode = interaction.client.music.cycle_loop_mode(
            interaction.guild.id
        )

        await interaction.client.music.update_player(
            interaction.guild.id
        )

        if mode == LoopMode.OFF:
            message = "🔁 Loop disabled."

        elif mode == LoopMode.TRACK:
            message = "🔂 Track loop enabled."

        else:
            message = "🔁 Queue loop enabled."

        await interaction.response.send_message(
            message,
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
        state = interaction.client.music.get_state(
            interaction.guild.id
        )

        if state.current is None:
            await interaction.response.send_message(
                "📜 Queue is empty.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            embed=build_queue_embed(
                interaction.client,
                state,
                0,
            ),
            view=QueueView(
                interaction.client,
                state,
            ),
            ephemeral=True,
        )


class ShuffleButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            emoji="🔀",
            style=discord.ButtonStyle.secondary,
            row=2,
        )

    async def callback(
        self,
        interaction: discord.Interaction,
    ):
        success = await interaction.client.music.shuffle(
            interaction.guild.id
        )

        if success:
            await interaction.response.send_message(
                "🔀 Queue shuffled.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "❌ Need at least 2 queued songs.",
                ephemeral=True,
            )

class StopButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            emoji="⏹",
            style=discord.ButtonStyle.danger,
            row=2,
        )

    async def callback(
        self,
        interaction: discord.Interaction,
    ):
        success = await interaction.client.music.stop(
            interaction.guild.id
        )

        if success:
            await interaction.response.send_message(
                "⏹ Playback stopped.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "❌ Nothing is playing.",
                ephemeral=True,
            )

class SeekButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            emoji="📍",
            style=discord.ButtonStyle.secondary,
            row=2,
        )

    async def callback(
        self,
        interaction: discord.Interaction,
    ):
        await interaction.response.send_message(
            "📍 Seek Controls",
            view=SeekView(),
            ephemeral=True,
        )

class PlayerView(discord.ui.View):
    def __init__(
        self,
        enabled: bool = True,
    ):
        super().__init__(
            timeout=None
        )

        self.add_item(PreviousButton())
        self.add_item(PauseButton())
        self.add_item(SkipButton())
        self.add_item(LoopButton())
        self.add_item(QueueButton())
        self.add_item(ShuffleButton())
        self.add_item(StopButton())
        self.add_item(SeekButton())

        if not enabled:
            for item in self.children:
                if isinstance(
                    item,
                    QueueButton,
                ):
                    continue

                item.disabled = True