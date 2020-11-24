import discord
from discord.ext import commands

from common import constants
from utils.database_connector import execute_statement, create_select_top_x_scores_query
from utils.exception_wrapper import pm_dev_error
from utils.global_error_manager import in_channel_list


class List(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="list")
    @in_channel_list(constants.COMMAND_CHANNEL_LIST)
    async def list(self, ctx, leaderboard):
        """
        List your position in a given leaderboard.

        This command will list the top 5 of the leaderboard as well as your position and your closest competitors.

        Usage: ?list jogger
        """
        if leaderboard not in constants.LEADERBOARD_LIST:
            await ctx.send(f"The **{leaderboard}** leaderboard does not exist.")
            return

        rows = execute_statement(create_select_top_x_scores_query(leaderboard)).all(as_dict=True)

        found = False
        list_message = f"**---{leaderboard.capitalize()} list:---**\n"

        for index, entry in enumerate(rows):
            # if user is top 5
            if index < 5:
                if entry.get("name") == ctx.author.display_name:
                    found = True
                list_message += f"{index + 1}. {entry.get('name')} {entry.get('score')}\n"
            elif index == 5:
                if found:
                    await ctx.send(list_message)
                    return
                else:
                    list_message += "-----------------\n"
            elif index > 5 and entry.get("name") == ctx.author.display_name:
                list_message += f"{index - 1}. {rows[index - 2].get('name')} {entry.get('score')}\n"
                list_message += f"{index}. {rows[index - 1].get('name')} {entry.get('score')}\n"
                list_message += f"{index + 1}. {entry.get('name')} {entry.get('score')}\n"
                await ctx.send(list_message)
                return

        if not found:
            await ctx.send(f"Could not find {ctx.author.display_name} in {discord.utils.get(ctx.guild.channels, name=leaderboard).mention}")
        # Leaderboard had fewer than 5 entries
        else:
            await ctx.send(list_message)

    @list.error
    async def list_on_error(self, _, error):
        await pm_dev_error(bot=self.bot, error_message=error, source="List")


def setup(bot):
    bot.add_cog(List(bot))
