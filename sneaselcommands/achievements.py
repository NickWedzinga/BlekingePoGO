from typing import Dict

import discord
from discord.ext import commands

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
        table_name=tables.ACHIEVEMENTS_HIGHSCORES,
    )).all(as_dict=True)


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
        user_name = user.nick if user is not None else ctx.author.display_name
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

        if available_timeless_objectives:
            status_list += "**Challenges**\n"
        for available_objective in available_timeless_objectives:
            available_achievement_name = available_objective["achievement_name"]
            if user_objectives and any(user_obj["achievement_name"] == available_achievement_name for user_obj in user_objectives):
                if awarded_dict[available_achievement_name] == "1":
                    status_list += f"**:white_check_mark:[{awarded_dict[available_achievement_name]}/{nr_of_participants}] {available_achievement_name.replace('_', ' ').title()}**\n"
                else:
                    status_list += f":white_check_mark:[{awarded_dict[available_achievement_name]}/{nr_of_participants}] {available_achievement_name.replace('_', ' ').title()}\n"
            else:
                status_list += f":no_entry:[{awarded_dict[available_achievement_name]}/{nr_of_participants}] {available_achievement_name.replace('_', ' ').title()}\n"

        if any(user_objective["time_limited"] == "true" for user_objective in user_objectives):
            status_list += "**Time-Limited**\n"

            for user_objective in user_objectives:
                if user_objective["time_limited"] == "true":
                    achievement_name = user_objective['achievement_name']
                    status_list += f":hourglass:[{awarded_dict[achievement_name]}/{nr_of_participants}] {achievement_name.replace('_', ' ').title()}\n"

        if available_timeless_objectives or user_highscores:
            await ctx.send(status_list)
        else:
            raise ValueError(f"Database Error: Empty {tables.ACHIEVEMENTS_OBJECTIVES_LIST} table")

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
    async def add(self, ctx, type: str, achievement_name: str, time_limited: str, user_id: str, user_name: str, score: str = None):
        """Usage: ?achievement add <objective/highscore> <achievement_name> <time_limited=[true/false]> <user_id> <user_name> <score>"""
        if time_limited != "true" and time_limited != "false":
            return await ctx.send(f"time_limited has to be true or false, but was: [{time_limited}]")
        if not user_id.isnumeric:
            return await ctx.send(f"Expected user_id to be numeric, but got [{user_id}]")

        if type == "objective":
            maybe_achievement_exists = execute_statement(create_select_query(
                table_name=tables.ACHIEVEMENTS_OBJECTIVES_LIST,
                where_key="achievement_name",
                where_value=f"'{achievement_name}'"
            )).first(as_dict=True)

            if not maybe_achievement_exists:
                return await ctx.send(f":no_entry: Achievement Objective: [{achievement_name}] doesn't exist, hasn't been registered, or should be a highscore")

            if maybe_achievement_exists["time_limited"] != time_limited:
                return await ctx.send(f":no_entry: This achievement has time_limited=[{maybe_achievement_exists['time_limited']}], but you wanted to add it with [{time_limited}]")

            maybe_already_completed = execute_statement(create_select_query(
                table_name=tables.ACHIEVEMENTS_OBJECTIVES,
                where_key="achievement_name",
                where_value=f"'{achievement_name}'"
            )).all(as_dict=True)

            if any(user_id == entry["user_id"] for entry in maybe_already_completed):
                await ctx.send(f"{user_name} has already completed this objective")
                return
            execute_statement(create_insert_query(
                table_name=tables.ACHIEVEMENTS_OBJECTIVES,
                keys="(achievement_name, user_id, user_name, time_limited)",
                values=f"('{achievement_name}', '{user_id}', '{user_name}', '{str(time_limited)}')"
            ))
            execute_statement(create_update_query(
                table_name=tables.ACHIEVEMENTS_OBJECTIVES_LIST,
                where_key="achievement_name",
                where_value=f"'{achievement_name}'",
                column="awarded",
                new_value=f"'{int(maybe_achievement_exists['awarded']) + 1}'"
            ))
            await ctx.send(f"Added achievement {achievement_name} to {user_name}, now {int(maybe_achievement_exists['awarded']) + 1} have this achievement")
            return
        elif type == "highscore":
            if score is None:
                await ctx.send("Score is a mandatory field for highscores")
                return
            maybe_achievement_exists = execute_statement(create_select_query(
                table_name=tables.ACHIEVEMENTS_HIGHSCORES_LIST,
                where_key="achievement_name",
                where_value=f"'{achievement_name}'"
            )).all(as_dict=True)

            previous_highscores = execute_statement(create_select_query(
                table_name=tables.ACHIEVEMENTS_HIGHSCORES,
                where_key="achievement_name",
                where_value=f"'{achievement_name}'"
            )).all(as_dict=True)

            if not maybe_achievement_exists:
                await ctx.send(f"Achievement Highscore: [{achievement_name}] doesn't exist, hasn't been registered, or should be an objective")
                return

            # If this is the first entry for this achievement, just insert
            if not previous_highscores:
                execute_statement(create_upsert_query(
                    tablename=tables.ACHIEVEMENTS_HIGHSCORES,
                    keys="(achievement_name, user_id, user_name, score, time_limited)",
                    values=f"('{achievement_name}', '{user_id}', '{user_name}', '{score}', '{str(time_limited)}')",
                    key_to_update="score",
                    update_value=f"'{score}'"
                ))
                await ctx.send(
                    f"No previous highscores found, adding first entry for {user_name} with score {score}")
            # or if the new submission is also already currently the sole record holder, just update the score
            elif len(previous_highscores) == 1 and previous_highscores[0]["user_id"] == user_id:
                execute_statement(create_update_query(
                    table_name=tables.ACHIEVEMENTS_HIGHSCORES,
                    where_key="achievement_name",
                    where_value=f"'{achievement_name}'",
                    column="score",
                    new_value=f"'{score}'"
                ))
                await ctx.send(
                    f"Previous highscore was held by same person, updating score from {previous_highscores[0]['score']} to {score}")
            # or if the new submission is tied with record holder, insert new tied entry
            elif previous_highscores[0]["score"] == score:
                # just making sure the new entry isn't already currently the recordholder with same score
                if any(user_id == entry['user_id'] for entry in previous_highscores):
                    await ctx.send(f"{user_name} already has an entry with score {score}")
                    return
                else:
                    execute_statement(create_insert_query(
                        table_name=tables.ACHIEVEMENTS_HIGHSCORES,
                        keys="(achievement_name, user_id, user_name, score, time_limited)",
                        values=f"('{achievement_name}', '{user_id}', '{user_name}', '{score}', '{str(time_limited)}')"
                    ))
                    await ctx.send(f"{user_name} is currently tied with record holder, inserting new entry for shared record holder with score {score}")
            # new entry has higher score than current recordholder, delete all current entries and insert new entry
            else:
                execute_statement(create_delete_query(
                    table_name=tables.ACHIEVEMENTS_HIGHSCORES,
                    where_key="achievement_name",
                    where_value=f"'{achievement_name}'"
                ))
                execute_statement(create_insert_query(
                    table_name=tables.ACHIEVEMENTS_HIGHSCORES,
                    keys="(achievement_name, user_id, user_name, score, time_limited)",
                    values=f"('{achievement_name}', '{user_id}', '{user_name}', '{score}', '{str(time_limited)}')"
                ))
                await ctx.send(f"New record with score {score}, deleted previous record holder(s) and inserting new entry")
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
                new_value=f"'{user_id}'"
            ))
            return
        else:
            await ctx.send("Type has to be one of [objective, highscore]")

    @add.error
    async def add_on_error(self, _, error):
        """Catches errors with achievements add command"""
        await pm_dev_error(client=self.bot, error_message=error, source="achievements add command")


async def setup(bot):
    await bot.add_cog(Achievements(bot))
