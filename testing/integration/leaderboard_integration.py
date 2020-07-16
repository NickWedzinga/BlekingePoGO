import filecmp
import os
import shutil
import traceback

import common


async def add_to_leaderboard(ctx, bot, leaderboard):
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


async def add_to_leaderboards_test(ctx, bot):
    try:
        for leaderboard in common.LEADERBOARD_LIST[1:]:
            await add_to_leaderboard(ctx, bot, leaderboard)
        await common.TEST_RESULTS_CHANNEL.send(f":white_check_mark:  Leaderboard[Add to leaderboard]: Successfully added"
                                               f"a user to all leaderboards in the leaderboard list!")
    except Exception as e:
        traceback.print_exc()
        await common.TEST_RESULTS_CHANNEL.send(f":no_entry: Leaderboard: Error during add_to_leaderboard integration-tests: {e}")


async def renamed_member_test(ctx, bot):
    try:
        filename = "textfiles/idclaims.txt"
        with open(filename) as f:
            newText = f.read().replace('McMomo', 'McTester')

        with open(filename, "w") as f:
            f.write(newText)
        await add_to_leaderboard(ctx, bot, "totalxp")
        await common.TEST_RESULTS_CHANNEL.send(":no_entry:  Leaderboard[Renaming]: Successfully added user with changed name,"
                                               " should have thrown Exception.")
    except AssertionError as e:
        filename = "textfiles/idclaims.txt"
        with open(filename) as f:
            newText = f.read().replace('McTester', 'McMomo')

        with open(filename, "w") as f:
            f.write(newText)
        await common.TEST_RESULTS_CHANNEL.send(":white_check_mark: Leaderboard[Renaming]: Correctly thrown exception when attempting to "
                                               "add to a leaderboard with a changed nickname.")


async def run_tests(ctx, bot):
    await add_to_leaderboards_test(ctx, bot)
    await renamed_member_test(ctx, bot)
