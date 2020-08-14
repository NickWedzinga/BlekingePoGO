import traceback
from datetime import datetime

from discord.ext import commands

import common
from testing.integration import leaderboard_integration, list_integration, support_integration, configure_integration, \
    dex_integration


class TestManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="healthcheck", hidden=True)
    @commands.has_role("Admin")
    async def healthcheck(self, ctx):
        """
        [Admin only]: This command acts as a health-check.

        Usage: ?healthcheck
        """
        await ctx.send(f"""..zzzZZ.. huh? Yes, hello, I'm awake {ctx.message.author.mention}! :sweat_smile:""")

    @healthcheck.error
    async def healthcheck_on_error(self, ctx, error):
        traceback.print_exc()
        for dev in common.DEVELOPERS:
            user = ctx.bot.get_user(dev)
            await user.send(f"""Error in TEST command: {error}""")

    @commands.command(name="test", help=".", hidden=True)
    @commands.is_owner()
    async def test(self, ctx):
        """
        [Admin only]: Run integration-tests in test environment.

        Usage: ?test
        """
        if str(ctx.message.channel) == common.COMMAND_CHANNEL_LIST[1]:
            try:
                common.TEST_RESULTS_CHANNEL = self.bot.get_channel(640964820732084233)
                await common.TEST_RESULTS_CHANNEL.send(
                    f"""---**INTEGRATION-TESTS - STARTED: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**---""")
                await ctx.send(
                    f"Sending results to {common.TEST_RESULTS_CHANNEL.mention}. This may take a while :sweat_smile:")

                # TODO: Add all the tests to a list or something to run
                await leaderboard_integration.run_tests(ctx, self.bot)
                await list_integration.run_tests(ctx, self.bot)
                await support_integration.run_tests(ctx, self.bot)
                await configure_integration.run_tests(self.bot, ctx)
                await dex_integration.run_tests(self.bot, ctx)

                await ctx.send(f""":white_check_mark: All integration-tests are a-okay {ctx.message.author.mention}!""")
            except Exception as e:
                traceback.print_exc()
                await ctx.send(f""":no_entry: At least one error found: {e}!""")

    @test.error
    async def test_on_error(self, ctx, error):
        traceback.print_exc()
        for dev in common.DEVELOPERS:
            user = ctx.bot.get_user(dev)
            await user.send(f"""Error in TEST command: {error}""")


def setup(bot):
    bot.add_cog(TestManager(bot))
