import re
from datetime import datetime

import discord
from discord.ext import commands

from common import constants
from utils.channel_wrapper import delete_channel_messages
from utils.database_connector import execute_statement, create_select_query, create_select_top_x_scores_query, \
    get_ranking_of_user
from utils.exception_wrapper import pm_dev_error, catch_with_channel_message
from utils.global_error_manager import in_channel_list


def _validate_score(score: str):
    """Validates that score is a legitimate float value"""
    if not re.search("^[0-9]+[.,]?[0-9]?$", score):
        raise AssertionError("Score contains illegal characters")


async def _validate_claimed_user(bot, ctx):
    """Validates that current nickname matches claimed_id"""
    author_id = ctx.author.id
    author_name = ctx.author.display_name
    statement = create_select_query(table_name="leaderboard__idclaims", where_key="user_id", where_value=author_id)
    user_id = "DEFAULT"
    user_name = "DEFAULT"
    rows = []
    try:
        result = execute_statement(statement)
        user_id = result.first(as_dict=True).get("user_id")
        user_name = result.first(as_dict=True).get("name")
        rows = result.all()

        if len(rows) > 1 or user_id != author_id or user_name != author_name:
            raise AssertionError("Username doesn't match claimed username")
    except Exception as e:
        if user_id != author_id:
            await ctx.send("Error with your claimed id, did you change discord account? Contact an admin.")
        elif user_name != author_name:
            await ctx.send("Error with your claimed name, did you change your nickname? Contact an admin.")
        else:
            await ctx.send("Error when validating claimed id. Contact an admin.")
        await pm_dev_error(
            bot=bot,
            error_message=f"\nDiscord display name: {author_name}, database display name: {user_name}"
                          f"\nDiscord user id: {author_id}, database user id: {user_id}"
                          f"\nAmount of entries found for this claimed user in id_claims should be 1, "
                          f"was: {len(rows)}"
                          f"\nSQL QUERY: {statement}",
            source="_validate_claimed_user")
        raise AssertionError("Username doesn't match claimed username")


async def _validate_user(bot, ctx, score):
    """Validates that the user has a eligible claimed name and score"""
    await catch_with_channel_message(
        _validate_score,
        ctx.channel,
        "Incorrect score format, has to be a number.",
        True,
        "leaderboard/validate_score",
        *{score}
    )

    await _validate_claimed_user(bot, ctx)


def _create_leaderboard_embed(leaderboard: str, score_dict: dict, command_channel):
    """Creates the embed for the leaderboard channel"""
    embed = discord.Embed(title=f"Leaderboard Blekinge: {leaderboard.capitalize()} \n", color=0xff9900,
                          description=f"Submit your score with '?{leaderboard} score' in {command_channel.mention}")
    embed.set_thumbnail(url=f"https://vignette.wikia.nocookie.net/pokemongo/images/{constants.MEDAL_ICON_URLS.get(leaderboard)}")
    embed.set_footer(text=f"Showing top 10 scores, find your scores with ?ranks in {command_channel}")
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    for index, user in enumerate(score_dict):
        embed.add_field(
            name=f"{index + 1}. {user.get('name')} - {user.get('score')}",
            value=f"Updated: {user.get('submit_date')}", inline=True)
    return embed


async def _update_leaderboard_embed(embed, channel):
    """Updates the embed leaderboard in the provided channel"""
    await delete_channel_messages(channel, should_delay_between_deletes=False)
    await channel.send(embed=embed)


async def _congratulate_submitter(ctx, leaderboard_channel, previous_top_3: dict, current_top_3: dict):
    """Sends a congratulations message custom to which ranking the user got"""
    name = ctx.author.display_name

    # if submission made top 3
    if any(name == entry.get("name") for entry in current_top_3):
        for index, user in enumerate(current_top_3):
            # new rank 1
            if index == 0 and name == user.get("name") and not name == previous_top_3[0].get("name"):
                await ctx.send(f":crown: :first_place: CONGRATULATIONS {ctx.author.mention} on your new #{index + 1} placement in the {leaderboard_channel.mention} leaderboard!"
                               f"\nPlease send an in-game screenshot to any admin for verification.")
            # new top 3
            elif name == user.get("name") and not any(name == user_entry.get("name") for user_entry in previous_top_3):
                await ctx.send(f":crown: Congratulations {ctx.author.mention} on your #{index + 1} placement in the {leaderboard_channel.mention} leaderboard!"
                               f"\nPlease send an in-game screenshot to any admin for verification.")
            elif name == user.get("name"):
                await ctx.send(f":crown: Congratulations {ctx.author.mention} on your #{index + 1} position in the {leaderboard_channel.mention} leaderboard!")
    # submission not top 3
    else:
        record_collection = execute_statement(create_select_top_x_scores_query(leaderboard_channel.name))
        ranking = get_ranking_of_user(name=name, record_collection=record_collection)
        await ctx.send(f"Nice work {ctx.author.mention} on your #{ranking} position in the {leaderboard_channel.mention} leaderboard, keep it up!")


class Leaderboards(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    @commands.command(aliases=constants.LEADERBOARD_LIST)
    @in_channel_list(constants.COMMAND_CHANNEL_LIST)
    async def leaderboard(self, ctx, score):
        """
        Submit your score to a given leaderboard.

        Usage: ?jogger 507
        """
        await _validate_user(self.bot, ctx, score)

        # extract data
        try:
            score = float(score.replace(",", "."))
            invoked_leaderboard = ctx.invoked_with.lower()
            if invoked_leaderboard == "leaderboard":
                await ctx.send("Please submit to a specific leaderboard, such as jogger, type ?help for example usage.")
                return

            if invoked_leaderboard != "jogger":
                score = int(score)
        except:
            return

        # get previous top 3
        previous_top_3 = execute_statement(create_select_top_x_scores_query(table_name=invoked_leaderboard, limit=3)).all(as_dict=True)

        # insert entry into leaderboard
        execute_statement(f"INSERT INTO leaderboard__{invoked_leaderboard} (name, score, submit_date) VALUES ('{ctx.author.display_name}', {score}, DATE '{datetime.now().date()}')")

        # select 10 highest ranks
        descending_score_dict = execute_statement(create_select_top_x_scores_query(table_name=invoked_leaderboard, limit=10)).all(as_dict=True)

        leaderboard_channel = discord.utils.get(ctx.guild.channels, name=invoked_leaderboard)
        embed = _create_leaderboard_embed(
            leaderboard=invoked_leaderboard,
            score_dict=descending_score_dict,
            command_channel=discord.utils.get(ctx.guild.channels, name="leaderboards")
        )
        if ctx.channel.name != "momos_test_dungeon":
            await _update_leaderboard_embed(embed, leaderboard_channel)
        await _congratulate_submitter(ctx, leaderboard_channel, previous_top_3, descending_score_dict[:3])

    @leaderboard.error
    async def leaderboard_on_error(self, _, error):
        await pm_dev_error(bot=self.bot, error_message=error, source="Leaderboards")


async def setup(bot):
    await bot.add_cog(Leaderboards(bot))
