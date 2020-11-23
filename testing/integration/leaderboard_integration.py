import traceback

from common import constants
from testing.integration.test_utils import invoke_wrapper
from utils.exception_wrapper import catch_with_channel_message
from utils.database_connector import execute_statement, create_select_query, create_delete_query


async def add_to_leaderboards_test(bot, ctx):
    # check that user is not in test leaderboard before
    assert (len(execute_statement(create_select_query(table_name="leaderboard__test", where_key="name", where_value=f"'{ctx.author.display_name}'")).all(as_dict=True)) == 0)
    try:
        await catch_with_channel_message(
            invoke_wrapper.invoke_event_now,
            constants.TEST_RESULTS_CHANNEL,
            f":no_entry: Error during leaderboard #test invocation",
            True,
            f"integration/leaderboard",
            bot,
            ctx,
            f"leaderboard",
            f"leaderboard",
            *["500000000"]
        )
        await constants.TEST_RESULTS_CHANNEL.send(f":white_check_mark:  Leaderboard[Add to leaderboard]: Successfully added "
                                               f"a user to the test leaderboard!")

        # check that user is in test leaderboard after
        assert (len(execute_statement(create_select_query(table_name="leaderboard__test", where_key="name", where_value=f"'{ctx.author.display_name}'")).all(as_dict=True)) == 1)
        # remove user from leaderboard table again
        execute_statement(create_delete_query(table_name="leaderboard__test", where_key="name", where_value=f"'{ctx.author.display_name}'"))
        # check that user is no longer in leaderboard
        assert (len(execute_statement(create_select_query(table_name="leaderboard__test", where_key="name", where_value=f"'{ctx.author.display_name}'")).all(as_dict=True)) == 0)
    except Exception as e:
        traceback.print_exc()
        await constants.TEST_RESULTS_CHANNEL.send(f":no_entry: Leaderboard: Error during add_to_leaderboard integration-tests: {e}")
        raise ValueError("Error in Leaderboards integration-test")


async def run_tests(bot, ctx):
    await add_to_leaderboards_test(bot, ctx)
