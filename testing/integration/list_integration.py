import traceback

import common


async def call_list_test(ctx, bot):
    try:
        list_command = bot.get_command("list")
        await ctx.invoke(list_command, "totalxp")
        await common.TEST_RESULTS_CHANNEL.send(f":white_check_mark: List[Changing files]: List command invocation without error.")
    except Exception as e:
        traceback.print_exc()
        await common.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during list integration-tests: {e}")
        raise ValueError(f"Error during list integration-tests")


async def run_tests(ctx, bot):
    await call_list_test(ctx, bot)
