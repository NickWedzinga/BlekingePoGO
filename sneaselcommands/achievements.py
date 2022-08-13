import discord
from discord.ext import commands

from common import constants, tables
from utils.database_connector import execute_statement, create_select_query, create_upsert_query, create_insert_query, \
    create_update_query, create_delete_query
from utils.exception_wrapper import pm_dev_error
from utils.global_error_manager import in_channel_list


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
        available_objectives = execute_statement(create_select_query(
            table_name=tables.ACHIEVEMENTS_OBJECTIVES_LIST
        )).all(as_dict=True)

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

        status_list = f"**{user_name}'s Achievements - Requested by {ctx.author.mention}**\n"
        for entry in user_highscores:
            highscore_name = entry["achievement_name"]
            status_list += f":crown: Currently in the lead for {highscore_name.replace('_', ' ').title()}\n"

        for available_objective in available_objectives:
            available_achievement_name = available_objective["achievement_name"]
            if user_objectives and any(user_obj["achievement_name"] == available_achievement_name for user_obj in user_objectives):
                status_list += f":white_check_mark: {available_achievement_name.replace('_', ' ').title()}\n"
            else:
                status_list += f":no_entry: {available_achievement_name.replace('_', ' ').title()}\n"

        if available_objectives or user_highscores:
            await ctx.send(status_list)
        else:
            raise ValueError(f"Database Error: Empty {tables.ACHIEVEMENTS_OBJECTIVES_LIST} table")

    @achievements.error
    async def achievements_on_error(self, _, error):
        await pm_dev_error(bot=self.bot, error_message=error, source="Achievements")

    @commands.group(hidden=True)
    @in_channel_list(constants.COMMAND_CHANNEL_LIST)
    async def achievement(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid achievement command, options: achievement add, achievement create")

    @achievement.error
    async def achievement_on_error(self, _, error):
        """Catches errors with achievement base command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="achievement base command")

    @achievement.group()
    @commands.has_role("Admin")
    async def create(self, ctx, type: str, achievement_name: str):
        """Usage: ?achievements create <objective/highscore> <achievement_name>"""
        if type == "objective":
            execute_statement(create_insert_query(
                table_name=tables.ACHIEVEMENTS_OBJECTIVES_LIST,
                keys="(achievement_name, awarded)",
                values=f"('{achievement_name}', '{'0'}')"
            ))
        elif type == "highscore":
            execute_statement(create_insert_query(
                table_name=tables.ACHIEVEMENTS_HIGHSCORES_LIST,
                keys="(achievement_name, user_id, score)",
                values=f"('{achievement_name}', '{'N/A'}', '{'N/A'}')"
            ))
        else:
            await ctx.send("Type has to be one of [objective, highscore]")
        await ctx.send(f"Created {type} achievement with name {achievement_name}")

    @create.error
    async def create_on_error(self, _, error):
        """Catches errors with achievements create command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="achievements create command")

    @achievement.group()
    @commands.has_role("Admin")
    async def add(self, ctx, type: str, achievement_name: str, user_id: str, user_name: str, score: str = None):
        """Usage: ?achievements add <objective/highscore> <achievement_name> <user_id> <user_name> <score>"""

        if type == "objective":
            maybe_achievement_exists = execute_statement(create_select_query(
                table_name=tables.ACHIEVEMENTS_OBJECTIVES_LIST,
                where_key="achievement_name",
                where_value=f"'{achievement_name}'"
            )).all(as_dict=True)

            if not maybe_achievement_exists:
                await ctx.send(f"Achievement Objective: [{achievement_name}] doesn't exist, hasn't been registered, or should be a highscore")
                return

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
                keys="(achievement_name, user_id, user_name)",
                values=f"('{achievement_name}', '{user_id}', '{user_name}')"
            ))
            execute_statement(create_update_query(
                table_name=tables.ACHIEVEMENTS_OBJECTIVES_LIST,
                where_key="achievement_name",
                where_value=f"'{achievement_name}'",
                column="awarded",
                new_value=f"'{int(maybe_achievement_exists[0]['awarded']) + 1}'"
            ))
            await ctx.send(f"Added achievement {achievement_name} to {user_name}, now {int(maybe_achievement_exists[0]['awarded']) + 1} have this achievement")
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
                    keys="(achievement_name, user_id, user_name, score)",
                    values=f"('{achievement_name}', '{user_id}', '{user_name}', '{score}')",
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
                        keys="(achievement_name, user_id, user_name, score)",
                        values=f"('{achievement_name}', '{user_id}', '{user_name}', '{score}')"
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
                    keys="(achievement_name, user_id, user_name, score)",
                    values=f"('{achievement_name}', '{user_id}', '{user_name}', '{score}')"
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
        await pm_dev_error(bot=self.bot, error_message=error, source="achievements add command")


def setup(bot):
    bot.add_cog(Achievements(bot))
