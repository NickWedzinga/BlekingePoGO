from typing import Any
from typing import Dict

import discord

from common.constants import Leaderboards
from sneaselcommands.leaderboards.leaderboard_controller import LeaderboardController
from sneaselcommands.leaderboards.views.leaderboard_choice_view import LeaderboardChoiceView
from utils.exception_wrapper import pm_dev_error


# TODO: not happy with naming of first/second, but discord forces view to have max 25 buttons
class LeaderboardButtonsViewSecond(discord.ui.View):
    def __init__(self, leaderboard_controllers: Dict[Leaderboards, LeaderboardController]):
        super().__init__(timeout=None)
        self.leaderboard_controllers = leaderboard_controllers
        self.embed = discord.Embed(title="Would you like to submit a score or see the leaderboard?", color=0xff9900)

    @discord.ui.button(label='ranger', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.RANGER.value}')
    async def ranger(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.RANGER]),
                                                ephemeral=True)

    @discord.ui.button(label='risingstar', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.RISINGSTAR.value}')
    async def risingstar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.RISINGSTAR]),
                                                ephemeral=True)

    @discord.ui.button(label='risingstarduo', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.RISINGSTARDUO.value}')
    async def risingstarduo(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.RISINGSTARDUO]),
                                                ephemeral=True)

    @discord.ui.button(label='scientist', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.SCIENTIST.value}')
    async def scientist(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.SCIENTIST]),
                                                ephemeral=True)

    @discord.ui.button(label='sightseer', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.SIGHTSEER.value}')
    async def sightseer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.SIGHTSEER]),
                                                ephemeral=True)

    @discord.ui.button(label='successor', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.SUCCESSOR.value}')
    async def successor(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.SUCCESSOR]),
                                                ephemeral=True)

    @discord.ui.button(label='ultraleague', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.ULTRALEAGUE.value}')
    async def ultraleague(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.ULTRALEAGUE]),
                                                ephemeral=True)

    @discord.ui.button(label='unown', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.UNOWN.value}')
    async def unown(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.UNOWN]),
                                                ephemeral=True)

    @discord.ui.button(label='youngster', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.YOUNGSTER.value}')
    async def youngster(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.YOUNGSTER]),
                                                ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception, item: discord.ui.Item[Any], /) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        await pm_dev_error(interaction.client, source="SECOND BUTTONS VIEW")
