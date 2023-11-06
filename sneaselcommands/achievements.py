import logging
from typing import Dict

import discord
from discord.ext import commands
from records import RecordCollection

from common import constants, tables
from utils.database_connector import execute_statement, create_select_query, create_upsert_query, create_insert_query, \
    create_update_query, create_delete_query
from utils.exception_wrapper import pm_dev_error
from utils.global_error_manager import in_channel_list


def _get_objective_lists() -> [list, list]:
    """Returns tuple of [normal_objectives, timed_objectives]"""
    available_objectives = execute_statement(create_select_query(
        table_name=tables.ACHIEVEMENTS_OBJECTIVES_LIST
    )).all(as_dict=True)
    available_timeless_objectives = []
    available_time_limited_objectives = []
    for available_objective in available_objectives:
        if available_objective["time_limited"] == "false":
            available_timeless_objectives.append(available_objective)
        else:
            available_time_limited_objectives.append(available_objective)
    return available_timeless_objectives, available_time_limited_objectives


def _get_highscore_list() -> list:
    """Returns a list of available highscores"""
    return execute_statement(create_select_query(
        table_name=tables.ACHIEVEMENTS_HIGHSCORES_LIST,
    )).all(as_dict=True)


async def _add_members_to_objective(ctx, achievement: RecordCollection, *members: discord.Member):
    awarded = int(achievement["awarded"])
    time_limited = achievement["time_limited"]
    achievement_name = achievement["achievement_name"]

    for member in members:
        maybe_already_completed = execute_statement(f"select * FROM {tables.ACHIEVEMENTS_OBJECTIVES} WHERE achievement_name='{achievement_name}' AND user_id='{member.id}'").all(as_dict=True)
        if maybe_already_completed:
            await ctx.send(f"{member.mention} already has completed this achievement")
        else:
            execute_statement(create_insert_query(
                table_name=tables.ACHIEVEMENTS_OBJECTIVES,
                keys="(achievement_name, user_id, user_name, time_limited)",
                values=f"('{achievement_name}', '{member.id}', '{member.display_name}', '{time_limited}')"
            ))
            awarded += 1
            execute_statement(create_update_query(
                table_name=tables.ACHIEVEMENTS_OBJECTIVES_LIST,
                where_key="achievement_name",
                where_value=f"'{achievement_name}'",
                column="awarded",
                new_value=f"'{awarded}'"
            ))
            await ctx.send(
                f"Added achievement **{achievement_name}** to {member.mention}, now **{awarded}** have this achievement")


async def _add_members_to_highscore(ctx, achievement: RecordCollection, score: int, *members: discord.Member):
    time_limited = achievement["time_limited"]  # TODO: remove time_limited from highscore
    achievement_name = achievement["achievement_name"]

    previous_highscores = execute_statement(create_select_query(
        table_name=tables.ACHIEVEMENTS_HIGHSCORES,
        where_key="achievement_name",
        where_value=f"'{achievement_name}'"
    )).all(as_dict=True)

    if previous_highscores and int(previous_highscores[0]["score"]) != score:
        execute_statement(create_delete_query(
            table_name=tables.ACHIEVEMENTS_HIGHSCORES,
            where_key="achievement_name",
            where_value=f"'{achievement_name}'"
        ))
        await ctx.send(f"New record with score **{score}**, deleted previous record holder(s) and inserting new entries")

    for member in members:
        if any(member.id == entry['user_id'] for entry in previous_highscores):
            await ctx.send(f"{member.display_name} already has an entry with score {score}")
        else:
            execute_statement(create_insert_query(
                table_name=tables.ACHIEVEMENTS_HIGHSCORES,
                keys="(achievement_name, user_id, user_name, score, time_limited)",
                values=f"('{achievement_name}', '{member.id}', '{member.display_name}', '{score}', '{str(time_limited)}')"
            ))
            await ctx.send(
                f"Added highscore for {member.mention} with score **{score}**")

        # TODO: combine into one update
        execute_statement(create_update_query(
            table_name=tables.ACHIEVEMENTS_HIGHSCORES_LIST,
            where_key="achievement_name",
            where_value=f"'{achievement_name}'",
            column="score",
            new_value=f"'{score}'"
        ))
        execute_statement(create_update_query(
            table_name=tables.ACHIEVEMENTS_HIGHSCORES_LIST,
            where_key="achievement_name",
            where_value=f"'{achievement_name}'",
            column="user_id",
            new_value=f"'{member.id}'"
        ))


def _count_number_of_participants() -> int:
    """Query all objectives entries and count unique number of participants"""
    objective_rows = execute_statement(create_select_query(
        table_name=tables.ACHIEVEMENTS_OBJECTIVES
    )).all(as_dict=True)

    user_id_list = []
    for row in objective_rows:
        user_id_list.append(row["user_id"])
    return len(list(set(user_id_list)))  # convert list to set to remove duplicate entries


def _extract_awarded_by_objective() -> Dict[str, str]:
    """Query objective_list table and extract awarded information per achievement_name"""
    objectives = execute_statement(create_select_query(
        table_name=tables.ACHIEVEMENTS_OBJECTIVES_LIST
    )).all(as_dict=True)

    awarded_dict = {}
    for objective in objectives:
        awarded_dict[objective["achievement_name"]] = objective["awarded"]
    return awarded_dict


class Achievements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="achievements")
    async def achievements(self, ctx, user: discord.Member = None):
        """
        Lists your completed achievements as well as those you are yet to complete

        Usage: ?achievements
        Usage: ?achievements @McMomo
        """
        available_timeless_objectives, _ = _get_objective_lists()

        user_id = user.id if user is not None else ctx.author.id
        user_name = user.display_name if user is not None else ctx.author.display_name
        user_objectives = execute_statement(create_select_query(
            table_name=tables.ACHIEVEMENTS_OBJECTIVES,
            where_key="user_id",
            where_value=f"'{user_id}'"
        )).all(as_dict=True)

        user_highscores = execute_statement(create_select_query(
            table_name=tables.ACHIEVEMENTS_HIGHSCORES,
            where_key="user_id",
            where_value=f"'{user_id}'"
        )).all(as_dict=True)

        nr_of_participants = _count_number_of_participants()
        awarded_dict = _extract_awarded_by_objective()

        status_list = f"**{user_name}'s Achievements - Requested by {ctx.author.mention}**\n--------\n"
        status_list += f"*Example entry: :white_check_mark:[5/10] - Some Example Achievement, " \
                       f"this would mean 5 people have this achievement and 10 people have at least one achievement*" \
                       f"\n--------\n"
        if user_highscores:
            status_list += "**Records**\n"
            for entry in user_highscores:
                highscore_name = entry["achievement_name"]
                if entry["time_limited"] == "true":
                    status_list += f":crown: :hourglass: - High-score in {highscore_name.replace('_', ' ').title()} with a score of **{entry['score']}**\n"
                else:
                    status_list += f":crown: - High-score in {highscore_name.replace('_', ' ').title()} with a score of **{entry['score']}**\n"
        timeless_list = ""
        if available_timeless_objectives:
            timeless_list += "**Challenges**\n"
            for available_objective in available_timeless_objectives:
                available_achievement_name = available_objective["achievement_name"]
                if user_objectives and any(user_obj["achievement_name"] == available_achievement_name for user_obj in user_objectives):
                    if awarded_dict[available_achievement_name] == "1":
                        timeless_list += f"**:white_check_mark:[{awarded_dict[available_achievement_name]}/{nr_of_participants}] {available_achievement_name.replace('_', ' ').title()}**\n"
                    else:
                        timeless_list += f":white_check_mark:[{awarded_dict[available_achievement_name]}/{nr_of_participants}] {available_achievement_name.replace('_', ' ').title()}\n"
                else:
                    timeless_list += f":no_entry:[{awarded_dict[available_achievement_name]}/{nr_of_participants}] {available_achievement_name.replace('_', ' ').title()}\n"
        time_limited_list = ""
        if any(user_objective["time_limited"] == "true" for user_objective in user_objectives):
            time_limited_list += "**Time-Limited**\n"
            for user_objective in user_objectives:
                if user_objective["time_limited"] == "true":
                    achievement_name = user_objective['achievement_name']
                    time_limited_list += f":hourglass:[{awarded_dict[achievement_name]}/{nr_of_participants}] {achievement_name.replace('_', ' ').title()}\n"

        if status_list:
            await ctx.send(status_list)
        if timeless_list:
            await ctx.send(timeless_list)
        if time_limited_list:
            await ctx.send(time_limited_list)

    @achievements.error
    async def achievements_on_error(self, _, error):
        await pm_dev_error(client=self.bot, error_message=error, source="Achievements")

    @commands.group(hidden=True)
    @in_channel_list(constants.COMMAND_CHANNEL_LIST)
    async def achievement(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid achievement command, options: achievement add, achievement create")

    @achievement.error
    async def achievement_on_error(self, _, error):
        """Catches errors with achievement base command"""
        await pm_dev_error(client=self.bot, error_message=error, source="achievement base command")

    @achievement.group()
    @commands.has_role("Admin")
    async def list(self, ctx):
        """Usage: ?achievement list"""
        normal_objectives, timed_objectives = _get_objective_lists()
        highscores = _get_highscore_list()

        achievement_list = f"**Available achievements, only available to admins - requested by {ctx.author.mention}**\n--------\n"
        achievement_list += "**Highscores**\n"
        if not highscores:
            achievement_list += "-\n"
        else:
            for entry in highscores:
                achievement_list += f"""{entry["achievement_name"]}\n"""

        achievement_list += "\n**Challenges**\n"
        if not normal_objectives:
            achievement_list += "-\n"
        else:
            for entry in normal_objectives:
                achievement_list += f"""{entry["achievement_name"]}\n"""

        achievement_list += "\n**Time-Limited**\n"
        if not timed_objectives:
            achievement_list += "-\n"
        else:
            for entry in timed_objectives:
                achievement_list += f"""{entry["achievement_name"]}\n"""

        await ctx.send(achievement_list)

    @list.error
    async def create_on_error(self, _, error):
        """Catches errors with achievement list sub-command"""
        await pm_dev_error(client=self.bot, error_message=error, source="achievement list command")

    @achievement.group()
    @commands.has_role("Admin")
    async def create(self, ctx, type: str, achievement_name: str, time_limited: bool):
        """Usage: ?achievements create <objective/highscore> <achievement_name> <time_limited=[true/false]>"""
        if type == "objective":
            execute_statement(create_insert_query(
                table_name=tables.ACHIEVEMENTS_OBJECTIVES_LIST,
                keys="(achievement_name, awarded, time_limited)",
                values=f"('{achievement_name}', '{'0'}', '{str(time_limited).lower()}')"
            ))
        elif type == "highscore":
            execute_statement(create_insert_query(
                table_name=tables.ACHIEVEMENTS_HIGHSCORES_LIST,
                keys="(achievement_name, user_id, score, time_limited)",
                values=f"('{achievement_name}', '{'N/A'}', '{'N/A'}', '{str(time_limited).lower()}')"
            ))
        else:
            await ctx.send("Type has to be one of [objective, highscore]")
        await ctx.send(f"Created {type} achievement with name {achievement_name}")

    @create.error
    async def create_on_error(self, _, error):
        """Catches errors with achievements create command"""
        await pm_dev_error(client=self.bot, error_message=error, source="achievements create command")

    @achievement.group()
    @commands.has_role("Admin")
    async def add_highscore(self, ctx, achievement_name: str, score: int, *members: discord.Member):
        """
        Usage: ?achievement add <achievement_name> <optional_score> [list of members]
        ?achievement add catch_record 25 @McMomo
        """
        achievement = execute_statement(create_select_query(
            table_name=tables.ACHIEVEMENTS_HIGHSCORES_LIST,
            where_key="achievement_name",
            where_value=f"'{achievement_name}'"
        )).first(as_dict=True)

        if not achievement:
            return await ctx.send(f":no_entry: Achievement highscore with name [{achievement_name}] could not be found")

        return await _add_members_to_highscore(ctx, achievement, score, *members)

    @add_highscore.error
    async def add_highscore_on_error(self, ctx, error):
        """Catches errors with achievements add_highscore command"""
        if isinstance(error, discord.ext.commands.errors.MemberNotFound):
            await ctx.send(f"{error} The members have to be mentioned with @Name, like {ctx.author.mention}")
        await pm_dev_error(client=self.bot, error_message=error, source="achievements add_highscore sub-command")

    @achievement.group()
    @commands.has_role("Admin")
    async def add_objective(self, ctx, achievement_name: str, *members: discord.Member):
        """
        Usage: ?achievement add_objective <achievement_name> [list of mentioned members]
        ?achievement add_objective catch_something @McMomo @SneaselNr1 @FanOfSneasel
        """
        achievement = execute_statement(create_select_query(
            table_name=tables.ACHIEVEMENTS_OBJECTIVES_LIST,
            where_key="achievement_name",
            where_value=f"'{achievement_name}'"
        )).first(as_dict=True)

        if not achievement:
            return await ctx.send(f":no_entry: Achievement objective with name [{achievement_name}] could not be found")

        return await _add_members_to_objective(ctx, achievement, *members)

    @add_objective.error
    async def add_objective_on_error(self, ctx, error):
        """Catches errors with achievements add_objective command"""
        if isinstance(error, discord.ext.commands.errors.MemberNotFound):
            await ctx.send(f"{error} The members have to be mentioned with @Name, like {ctx.author.mention}")
        await pm_dev_error(client=self.bot, error_message=error, source="achievements add_objective sub-command")


async def setup(bot):
    await bot.add_cog(Achievements(bot))
