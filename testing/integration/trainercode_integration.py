import logging

from common import constants, tables
from utils.database_connector import execute_statement, create_select_query


async def call_trainercode_tests(bot, ctx):
    try:
        await add_and_remove_code_test(bot, ctx)
        await double_users_test(bot, ctx)
        await constants.TEST_RESULTS_CHANNEL.send(
            ":white_check_mark: Trainercode: Command invocation without error.")
    except Exception as e:
        logging.exception(e)
        await constants.TEST_RESULTS_CHANNEL.send(
            f":no_entry: Error during trainer code integration-tests: {e}")
        raise ValueError("Error during trainer code integration-tests") from e


async def add_and_remove_code_test(bot, ctx):
    trainercode_command = bot.get_command("trainercode")

    await ctx.invoke(trainercode_command, "remove")
    maybe_code_in_db = check_in_db(ctx)
    assert not maybe_code_in_db

    await invoke_command_and_assert(ctx, trainercode_command, "111122223333")
    await invoke_command_and_assert(ctx, trainercode_command, "000011112222")
    await invoke_command_and_assert(ctx, trainercode_command, "0000", "1111", "2222")

    await ctx.invoke(trainercode_command, "remove")

    maybe_code_in_db = check_in_db(ctx)
    assert not maybe_code_in_db


async def double_users_test(bot, ctx):
    trainercode_command = bot.get_command("trainercode")

    await ctx.invoke(trainercode_command, "remove")
    maybe_code_in_db = check_in_db(ctx)
    assert not maybe_code_in_db

    await invoke_command_and_assert(ctx, trainercode_command, ctx.author.display_name, nr_of_codes=0)
    await invoke_command_and_assert(ctx, trainercode_command, "000011112222")
    await invoke_command_and_assert(ctx, trainercode_command, ctx.author.display_name, nr_of_codes=1)
    await invoke_command_and_assert(
        ctx, trainercode_command, ctx.author.display_name, ctx.author.display_name, nr_of_codes=1)
    await invoke_command_and_assert(ctx, trainercode_command, "McMomo2", "123412341234", nr_of_codes=2)
    await invoke_command_and_assert(ctx, trainercode_command, "McMomo3", "111122223333", nr_of_codes=3)

    await invoke_command_and_assert(ctx, trainercode_command, "remove", "McMomo3", nr_of_codes=2)
    await invoke_command_and_assert(ctx, trainercode_command, "remove", nr_of_codes=0)

    await ctx.invoke(trainercode_command, "remove")

    maybe_code_in_db = check_in_db(ctx)
    assert not maybe_code_in_db


async def invoke_command_and_assert(ctx, command, *code, nr_of_codes: int = 1):
    """Invokes given command, passes args and asserts number of rows in database"""
    await ctx.invoke(command, *code)
    maybe_code_in_db = check_in_db(ctx)
    assert len(maybe_code_in_db) == nr_of_codes
    if maybe_code_in_db:
        assert maybe_code_in_db[0].get("user_id") == str(ctx.author.id)


def check_in_db(ctx) -> list:
    return execute_statement(create_select_query(
        table_name=tables.TRAINERCODES,
        where_key="user_id",
        where_value=ctx.author.id
    )).all(as_dict=True)


async def run_tests(bot, ctx):
    await call_trainercode_tests(bot, ctx)
