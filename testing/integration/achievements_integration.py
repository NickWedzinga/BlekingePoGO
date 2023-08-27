import asyncio
import logging

from common import constants, tables
from utils.database_connector import execute_statement, create_select_query, create_delete_query


async def call_achievements_test(bot, ctx):
    await achievements_empty_database(bot, ctx)
    await objective_achievement_tests(bot, ctx)
    await highscore_base_achievement_tests(bot, ctx)
    #await highscore_corner_cases_achievement_tests(bot, ctx) TODO cant test add as invoke converts mention to str


async def achievements_empty_database(bot, ctx):
    try:
        execute_statement(create_delete_query(
            table_name=tables.ACHIEVEMENTS_OBJECTIVES
        ))
        execute_statement(create_delete_query(
            table_name=tables.ACHIEVEMENTS_OBJECTIVES_LIST
        ))
        execute_statement(create_delete_query(
            table_name=tables.ACHIEVEMENTS_HIGHSCORES
        ))
        execute_statement(create_delete_query(
            table_name=tables.ACHIEVEMENTS_HIGHSCORES_LIST
        ))

        achievements_command = bot.get_command("achievements")
        await ctx.invoke(achievements_command)
    except Exception as e:
        if "Database Error: Empty" in str(e):
            await constants.TEST_RESULTS_CHANNEL.send(f":white_check_mark: Achievements[Empty Table]: Achievements command invocation without error.")
        else:
            logging.exception(e)
            await constants.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during achievements integration-tests: {e}")
            raise ValueError(f"Error during achievements integration-tests")


async def objective_achievement_tests(bot, ctx):
    try:
        achievements_create_command = bot.get_command("achievement create")
        await ctx.invoke(achievements_create_command, "objective", "test_objective", "false")

        achievements_command = bot.get_command("achievements")
        await ctx.invoke(achievements_command)

        # TODO: invoke converts args to str, so can't test add
        #add_command = bot.get_command("achievement add_objective")
        #await ctx.invoke(add_command, "test_objective", ctx.author.mention, ctx.author.mention)

        await constants.TEST_RESULTS_CHANNEL.send(
            f":white_check_mark: Achievements[Objectives]: Achievement objective command invocation without error.")
    except Exception as e:
        logging.exception(e)
        await constants.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during achievements objective integration-tests: {e}")
        raise ValueError(f"Error during achievements objectives integration-tests")


async def highscore_base_achievement_tests(bot, ctx):
    try:
        achievements_create_command = bot.get_command("achievement create")
        await ctx.invoke(achievements_create_command, "highscore", "test_highscore", "false")

        achievements_command = bot.get_command("achievements")
        await ctx.invoke(achievements_command)

        # TODO: invoke converts args to str, so can't test add
        #add_command = bot.get_command("achievement add_highscore")
        #await ctx.invoke(add_command, "test_objective", 1, ctx.author.mention)

        await constants.TEST_RESULTS_CHANNEL.send(
            f":white_check_mark: Achievements[Highscores Base]: Achievement highscore base command invocation without error.")
    except Exception as e:
        logging.exception(e)
        await constants.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during achievements highscores base integration-tests: {e}")
        raise ValueError(f"Error during achievements highscores base integration-tests")


async def highscore_corner_cases_achievement_tests(bot, ctx):
    try:
        # add 2nd person with same score and verify number of entries are 2
        add_command = bot.get_command("achievement add")
        await ctx.invoke(add_command, "highscore", "test_highscore", "false", "169688623699066881", "McMomo2", "1")
        await asyncio.sleep(5)
        highscore_entries = execute_statement(create_select_query(
            table_name=tables.ACHIEVEMENTS_HIGHSCORES
        )).all(as_dict=True)
        assert(len(highscore_entries) == 2)

        # add new score and verify that both previous are deleted and only new remains
        await ctx.invoke(add_command, "highscore", "test_highscore", "false", "169688623699066880", "McMomo", "0")
        await asyncio.sleep(5)
        highscore_entries = execute_statement(create_select_query(
            table_name=tables.ACHIEVEMENTS_HIGHSCORES
        )).all(as_dict=True)
        assert (len(highscore_entries) == 1)

        # try to insert same score again and verify that we dont crash
        await ctx.invoke(add_command, "highscore", "test_highscore", "false", "169688623699066880", "McMomo", "0")
        await asyncio.sleep(5)
        highscore_entries = execute_statement(create_select_query(
            table_name=tables.ACHIEVEMENTS_HIGHSCORES
        )).all(as_dict=True)
        assert (len(highscore_entries) == 1)

        await constants.TEST_RESULTS_CHANNEL.send(
            f":white_check_mark: Achievements[Highscores Corner Cases]: Achievement highscore corner cases command invocation without error.")
    except Exception as e:
        logging.exception(e)
        await constants.TEST_RESULTS_CHANNEL.send(
            f":no_entry: Error during achievements highscores corner cases integration-tests: {e}")
        raise ValueError(f"Error during achievements highscores corner cases integration-tests")


async def run_tests(bot, ctx):
    await call_achievements_test(bot, ctx)
