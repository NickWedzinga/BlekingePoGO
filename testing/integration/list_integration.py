import filecmp
import os
import shutil
import traceback

import common


async def call_all_lists_test(ctx, bot):
    try:
        list_command = bot.get_command("list")
        for leaderboard in common.LEADERBOARD_LIST[1:]:
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

        await common.TEST_RESULTS_CHANNEL.send(f":white_check_mark: LIST command integration-tests passed successfully!")
    except Exception as e:
        traceback.print_exc()
        await common.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during list integration-tests: {e}")


async def run_tests(ctx, bot):
    await call_all_lists_test(ctx, bot)