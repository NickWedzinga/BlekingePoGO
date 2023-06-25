from typing import Dict, Any

import discord

from common.constants import Leaderboards
from sneaselcommands.leaderboards.leaderboard_controller import LeaderboardController
from sneaselcommands.leaderboards.views.leaderboard_choice_view import LeaderboardChoiceView
from utils.exception_wrapper import pm_dev_error


# TODO: not happy with naming of first/second, but discord forces view to have max 25 buttons
class LeaderboardButtonsViewFirst(discord.ui.View):
    def __init__(self, leaderboard_controllers: Dict[Leaderboards, LeaderboardController]):
        super().__init__(timeout=None)
        self.leaderboard_controllers = leaderboard_controllers
        self.embed = discord.Embed(title="Would you like to submit a score or see the leaderboard?", color=0xff9900)

    @discord.ui.button(label=Leaderboards.TOTALXP.value, style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.TOTALXP.value}')
    async def totalxp(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.TOTALXP]),
                                                ephemeral=True)

    @discord.ui.button(label=Leaderboards.ACETRAINER.value, style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.ACETRAINER.value}')
    async def acetrainer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.ACETRAINER]),
                                                ephemeral=True)

    @discord.ui.button(label='backpacker', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.BACKPACKER.value}')
    async def backpacker(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.BACKPACKER]),
                                                ephemeral=True)

    @discord.ui.button(label='battlegirl', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.BATTLEGIRL.value}')
    async def battlegirl(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.BATTLEGIRL]),
                                                ephemeral=True)

    @discord.ui.button(label='battlelegend', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.BATTLELEGEND.value}')
    async def battlelegend(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.BATTLELEGEND]),
                                                ephemeral=True)

    @discord.ui.button(label='bestbuddy', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.BESTBUDDY.value}')
    async def bestbuddy(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.BESTBUDDY]),
                                                ephemeral=True)

    @discord.ui.button(label='berrymaster', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.BERRYMASTER.value}')
    async def berrymaster(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.BERRYMASTER]),
                                                ephemeral=True)

    @discord.ui.button(label='breeder', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.BREEDER.value}')
    async def breeder(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.BREEDER]),
                                                ephemeral=True)

    @discord.ui.button(label='cameraman', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.CAMERAMAN.value}')
    async def cameraman(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.CAMERAMAN]),
                                                ephemeral=True)

    @discord.ui.button(label='champion', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.CHAMPION.value}')
    async def champion(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.CHAMPION]),
                                                ephemeral=True)

    @discord.ui.button(label='collector', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.COLLECTOR.value}')
    async def collector(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.COLLECTOR]),
                                                ephemeral=True)

    @discord.ui.button(label='fisher', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.FISHER.value}')
    async def fisher(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.FISHER]),
                                                ephemeral=True)

    @discord.ui.button(label='gentleman', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.GENTLEMAN.value}')
    async def gentleman(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.GENTLEMAN]),
                                                ephemeral=True)

    @discord.ui.button(label='goldgyms', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.GOLDGYMS.value}')
    async def goldgyms(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.GOLDGYMS]),
                                                ephemeral=True)

    @discord.ui.button(label='greatleague', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.GREATLEAGUE.value}')
    async def greatleague(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.GREATLEAGUE]),
                                                ephemeral=True)

    @discord.ui.button(label='gymleader', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.GYMLEADER.value}')
    async def gymleader(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.GYMLEADER]),
                                                ephemeral=True)

    @discord.ui.button(label='hero', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.HERO.value}')
    async def hero(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.HERO]),
                                                ephemeral=True)

    @discord.ui.button(label='idol', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.IDOL.value}')
    async def idol(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.IDOL]),
                                                ephemeral=True)

    @discord.ui.button(label='jogger', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.JOGGER.value}')
    async def jogger(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.JOGGER]),
                                                ephemeral=True)

    @discord.ui.button(label='masterleague', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.MASTERLEAGUE.value}')
    async def masterleague(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.MASTERLEAGUE]),
                                                ephemeral=True)

    @discord.ui.button(label='picnicker', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.PICNICKER.value}')
    async def picnicker(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.PICNICKER]),
                                                ephemeral=True)

    @discord.ui.button(label='pikachu', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.PIKACHU.value}')
    async def pikachu(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.PIKACHU]),
                                                ephemeral=True)

    @discord.ui.button(label='pilot', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.PILOT.value}')
    async def pilot(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.PILOT]),
                                                ephemeral=True)

    @discord.ui.button(label='pokedex', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.POKEDEX.value}')
    async def pokedex(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.POKEDEX]),
                                                ephemeral=True)

    @discord.ui.button(label='purifier', style=discord.ButtonStyle.green,
                       custom_id=f'button:{Leaderboards.PURIFIER.value}')
    async def purifier(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=self.embed, view=LeaderboardChoiceView(
            self.leaderboard_controllers[Leaderboards.PURIFIER]),
                                                ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception, item: discord.ui.Item[Any], /) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        await pm_dev_error(interaction.client, source="FIRST BUTTONS VIEW")
