import discord

from sneaselcommands.leaderboards.leaderboard_controller import LeaderboardController
from utils.exception_wrapper import pm_dev_error


class LeaderboardSubmitModal(discord.ui.Modal, title='Leaderboard Score Submission'):
    def __init__(self, leaderboard_controller: LeaderboardController):
        super().__init__()
        self.leaderboard_controller = leaderboard_controller

    score = discord.ui.TextInput(label=f"Enter your score", placeholder='1337')

    async def on_submit(self, interaction: discord.Interaction):
        if not self.leaderboard_controller.validate_score(self.score.value):
            await interaction.response.send_message(
                f':no_entry: Please submit your score with numbers only {interaction.user.mention}', ephemeral=True)
            return

        previous_top_3 = self.leaderboard_controller.get_previous_top_3()
        self.leaderboard_controller.insert_score(self.score.value, interaction)

        await self.leaderboard_controller.congratulate(interaction, previous_top_3)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        await pm_dev_error(interaction.client, source="SUBMIT MODAL")
