import common


async def test_test(ctx, bot):
    await common.TEST_RESULTS_CHANNEL.send(f":white_check_mark: Support[Empty]: Successfully ran empty test!")


async def run_tests(ctx, bot):
    await test_test(ctx, bot)