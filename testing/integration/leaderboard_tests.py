import filecmp
import os
import shutil
import traceback

import Common
from Instance import bot


async def add_to_leaderboard(ctx, leaderboard):
    leaderboard_command = bot.get_command(leaderboard)

    orgl_file = f"leaderboards/{leaderboard}.txt"
    copied_file = f"leaderboards/{leaderboard}2.txt"

    shutil.copy(orgl_file, copied_file)
    if not filecmp.cmp(orgl_file, copied_file):
        await ctx.send(":no_entry: Contents changed, see traceback.")
        traceback.print_exc()
        raise ValueError(f"Comparison Error: {orgl_file} contents were changed during list function call.")
    os.remove(copied_file)
    await ctx.invoke(leaderboard_command, leaderboard)


async def add_to_leaderboards_test(ctx):
    try:
        for leaderboard in Common.leaderboard_list[1:]:
            await add_to_leaderboard(ctx, leaderboard)
        await Common.test_results_channel.send(f":white_check_mark: LEADERBOARD command integration-tests passed successfully!")
    except Exception as e:
        traceback.print_exc()
        await Common.test_results_channel.send(f":no_entry: Error during list integration-tests: {e}")


async def renamed_member_test(ctx):
    try:
        filename = "textfiles/idclaims.txt"
        with open(filename) as f:
            newText = f.read().replace('McMomo', 'McTester')

        with open(filename, "w") as f:
            f.write(newText)
        await add_to_leaderboard(ctx, "totalxp")
        await Common.test_results_channel.send(":no_entry: Leaderboard successfully added user with changed name,"
                                               " should have thrown Exception.")
    except AssertionError as e:
        filename = "textfiles/idclaims.txt"
        with open(filename) as f:
            newText = f.read().replace('McTester', 'McMomo')

        with open(filename, "w") as f:
            f.write(newText)
        await Common.test_results_channel.send(":white_check_mark: Correctly thrown exception when attempting to"
                                               "add to a leaderboard with a changed nickname.")


async def run_tests(ctx):
    await add_to_leaderboards_test(ctx)
    await renamed_member_test(ctx)