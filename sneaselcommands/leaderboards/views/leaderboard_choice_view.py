from typing import Any

import discord

from sneaselcommands.leaderboards.leaderboard_controller import LeaderboardController
from sneaselcommands.leaderboards.leaderboard_submit_modal import LeaderboardSubmitModal
from utils.exception_wrapper import pm_dev_error


class LeaderboardChoiceView(discord.ui.View):
    def __init__(self, leaderboard_controller: LeaderboardController):
        super().__init__()
        self.leaderboard_controller = leaderboard_controller

    @discord.ui.button(label='submit', style=discord.ButtonStyle.green)
    async def submit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(LeaderboardSubmitModal(self.leaderboard_controller))

    @discord.ui.button(label='leaderboard', style=discord.ButtonStyle.green)
    async def leaderboard(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.leaderboard_controller.create_leaderboard_embed(interaction.user)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception, item: discord.ui.Item[Any], /) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        await pm_dev_error(interaction.client, source="CHOICE BUTTONS")
