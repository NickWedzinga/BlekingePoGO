import traceback

from common import constants, tables
from utils.database_connector import execute_statement, create_select_query


async def call_trainercode_tests(bot, ctx):
    try:
        await add_and_remove_code_test(bot, ctx)
        await constants.TEST_RESULTS_CHANNEL.send(f":white_check_mark: Trainercode: Command invocation without error.")
    except Exception as e:
        traceback.print_exc()
        await constants.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during trainer code integration-tests: {e}")
        raise ValueError(f"Error during trainer code integration-tests")


async def add_and_remove_code_test(bot, ctx):
    trainercode_command = bot.get_command("trainercode")
    remove_command = bot.get_command("remove_trainercode")

    maybe_code_in_db = check_in_db(ctx)
    assert(not maybe_code_in_db)

    await ctx.invoke(trainercode_command, 111122223333)

    maybe_code_in_db = check_in_db(ctx)
    assert maybe_code_in_db

    await ctx.invoke(remove_command)

    maybe_code_in_db = check_in_db(ctx)
    assert(not maybe_code_in_db)


def check_in_db(ctx) -> list:
    return execute_statement(create_select_query(
        table_name=tables.TRAINERCODES,
        where_key="user_id",
        where_value=ctx.author.id
    )).all(as_dict=True)



async def run_tests(bot, ctx):
    await call_trainercode_tests(bot, ctx)
