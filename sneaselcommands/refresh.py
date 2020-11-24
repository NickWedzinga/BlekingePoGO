import discord
from discord.ext import commands

from common import constants
from sneaselcommands.leaderboards import _create_leaderboard_embed, _update_leaderboard_embed
from utils.database_connector import execute_statement, create_select_top_x_scores_query
from utils.exception_wrapper import pm_dev_error
from utils.global_error_manager import in_channel_list


class Refresh(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="refresh", hidden=True)
    @commands.has_role("Admin")
    @in_channel_list(constants.COMMAND_CHANNEL_LIST)
    async def refresh(self, ctx, leaderboard):
        """
        [Admin only] Refreshes a given leaderboard. Useful after manual intervention.
        """
        if leaderboard not in constants.LEADERBOARD_LIST and leaderboard != "test":
            await ctx.send(f"Could not find the {leaderboard} leaderboard.")
            return

        descending_score_dict = execute_statement(create_select_top_x_scores_query(table_name=leaderboard, limit=10)).all(as_dict=True)

        leaderboard_channel = discord.utils.get(ctx.guild.channels, name=leaderboard)
        embed = _create_leaderboard_embed(
            leaderboard=leaderboard,
            score_dict=descending_score_dict,
            command_channel=discord.utils.get(ctx.guild.channels, name="leaderboards")
        )

        await _update_leaderboard_embed(embed, leaderboard_channel)
        await ctx.send(f"Refreshed the {leaderboard} leaderboard.")

    @refresh.error
    async def leaderboard_on_error(self, _, error):
        await pm_dev_error(bot=self.bot, error_message=error, source="Refresh")


def setup(bot):
    bot.add_cog(Refresh(bot))
