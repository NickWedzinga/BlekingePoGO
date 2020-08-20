from discord.ext import commands

import common
from utils.database_connector import execute_statements, create_select_top_x_scores_query
from utils.exception_wrapper import pm_dev_error
from utils.global_error_manager import in_channel_list


def _create_rank_string(rank, name, leaderboard_type, score):
    """
    :param rank: The member's leaderboard rank
    :param name: The member's name
    :param leaderboard_type: Name of the leaderboard that is being processed
    :param score: The member's submitted score
    :return: Returns a prettified string listing the member's name, rank and score in this leaderboard
    """
    rank_to_emoji = {1: ':trophy:', 2: ':second_place:', 3: ':third_place:', 4: ':four:', 5: ':five:',
                     6: ':six:', 7: ':seven:', 8: ':eight:', 9: ':nine:', 10: ':keycap_ten:'}
    return f"{rank_to_emoji.get(rank, ':asterisk:')} {name} is ranked #{rank} in the {leaderboard_type.capitalize()}" \
           f" leaderboard with a score of {score}."


def _build_rank_message(message_list, from_, to_):
    """
    :param message_list: Concatenated list of all detailed rank messages
    :param from_: Index in the list to start at
    :param to_: Index in the list to end at
    :return: Takes a list of strings and returns a joined string with a newline denominator
    """
    return "\n".join(message_list[from_:to_ + 1])


def _every_fifteenth_or_last(number, last):
    """
    :param number: Current index in iteration of leaderboard list
    :param last: Index of last iteration of leaderboard list
    :return: Returns True every 15th index and for the last index
    """
    if (number != 0 and number % 15 == 0) or number == last:
        return True
    return False


# TODO: maybe send as embed?
async def _send_ranks(ctx, concat_message):
    """
    :param ctx: The member's sent message context
    :param concat_message: The message to send to the member, contains details on rank and score for each leaderboard
    :return: Sends message with leaderboard details to the member that requested them
    """
    previously_sent = 0
    for num, msg in enumerate(concat_message):
        if _every_fifteenth_or_last(num, len(concat_message) - 1):
            await ctx.message.author.send(_build_rank_message(concat_message, previously_sent, num))
            previously_sent += 16
    await ctx.send(f"You have received a PM with your ranks {ctx.author.mention}")


class Ranks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ranks")
    @in_channel_list(common.COMMAND_CHANNEL_LIST)
    async def ranks(self, ctx):
        """
        Get all your current ranks in a private message.

        Usage: ?ranks
        """
        statements = []
        for leaderboard in common.LEADERBOARD_LIST:
            statements.append(create_select_top_x_scores_query(leaderboard))

        all_leaderboards_data = execute_statements(statements)
        concat_message = []
        for leaderboard_name, leaderboard_data in zip(common.LEADERBOARD_LIST, all_leaderboards_data):
            for rank, user in enumerate(leaderboard_data.all(as_dict=True)):
                if user.get("name") == ctx.author.display_name:
                    concat_message.append(
                        _create_rank_string(
                            rank=rank + 1,
                            name=ctx.author.mention,
                            leaderboard_type=leaderboard_name.capitalize(),
                            score=user.get("score")
                        )
                    )
        await _send_ranks(ctx, concat_message)

    @ranks.error
    async def ranks_on_error(self, _, error):
        await pm_dev_error(bot=self.bot, error_message=error, source="Ranks")


def setup(bot):
    bot.add_cog(Ranks(bot))
