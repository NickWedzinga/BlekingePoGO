import filecmp
import os
import shutil
import traceback

import Common
from Instance import bot


async def leaderboard_test(ctx):
    try:
        await ctx.send(f"Sending results to {Common.test_results_channel.mention}. This may take a while :sweat_smile:")
        for leaderboard in Common.leaderboard_list[1:]:
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
        await Common.test_results_channel.send(f":white_check_mark: LEADERBOARD command unit-tests passed successfully!")
    except Exception as e:
        traceback.print_exc()
        await Common.test_results_channel.send(f":no_entry: Error during list unit tests: {e}")


async def list_test(ctx):
    try:
        list_command = bot.get_command("list")
        for leaderboard in Common.leaderboard_list[1:]:
            orgl_file = f"leaderboards/{leaderboard}.txt"
            copied_file = f"leaderboards/{leaderboard}2.txt"

            shutil.copy(orgl_file, copied_file)
            if not filecmp.cmp(orgl_file, copied_file):
                await ctx.send(":no_entry: Contents changed, see traceback.")
                traceback.print_exc()
                raise ValueError(f"Comparison Error: {orgl_file} contents were changed during list function call.")
            os.remove(copied_file)

            await ctx.invoke(list_command, leaderboard)
        await Common.test_results_channel.send(f":white_check_mark: LIST command unit-tests passed successfully!")
    except Exception as e:
        traceback.print_exc()
        await Common.test_results_channel.send(f":no_entry: Error during list unit tests: {e}")