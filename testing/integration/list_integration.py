import filecmp
import os
import shutil
import traceback

import common


async def call_list_test(ctx, bot):
    try:
        list_command = bot.get_command("list")
        await list_test(ctx, bot, "totalxp", list_command)
    except Exception as e:
        traceback.print_exc()
        await common.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during list integration-tests: {e}")


async def list_test(ctx, bot, leaderboard, list_command):
    original_file = f"leaderboards/{leaderboard}.txt"
    copied_file = f"leaderboards/{leaderboard}2.txt"
    shutil.copy(original_file, copied_file)

    await ctx.invoke(list_command, leaderboard)

    # compare files after list call
    if not filecmp.cmp(original_file, copied_file):
        await ctx.send(":no_entry: Contents changed, see traceback.")
        traceback.print_exc()
        raise ValueError(f"Comparison Error: {original_file} contents were changed during list function call.")
    os.remove(copied_file)

    await common.TEST_RESULTS_CHANNEL.send(f":white_check_mark: List[Changing files]: List command does not alter "
                                           f"contents of leaderboard file!")


# TODO: Test that list array returns correct values
async def run_tests(ctx, bot):
    await call_list_test(ctx, bot)
