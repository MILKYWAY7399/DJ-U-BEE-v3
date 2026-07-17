import discord

from ui.queue_embed import build_queue_embed


class QueueView(discord.ui.View):
    def __init__(
        self,
        bot,
        state,
    ):
        super().__init__(timeout=300)

        self.bot = bot
        self.state = state
        self.page = 0
        self.update_buttons()

    def update_buttons(self):
        pages = max(
            1,
            (len(self.state.queue) + 9) // 10,
        )

        self.previous.disabled = self.page == 0
        self.next.disabled = self.page >= pages - 1


    async def update(
        self,
        interaction: discord.Interaction,
    ):
        self.update_buttons()
        await interaction.response.edit_message(
            embed=build_queue_embed(
                self.bot,
                self.state,
                self.page,
            ),
            view=self,
        )

    @discord.ui.button(
        emoji="⬅️",
        style=discord.ButtonStyle.secondary,
    )
    async def previous(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        if self.page > 0:
            self.page -= 1

        await self.update(interaction)

    @discord.ui.button(
        emoji="➡️",
        style=discord.ButtonStyle.secondary,
    )
    async def next(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        pages = max(
            1,
            (len(self.state.queue) + 9) // 10,
        )

        if self.page < pages - 1:
            self.page += 1

        await self.update(interaction)