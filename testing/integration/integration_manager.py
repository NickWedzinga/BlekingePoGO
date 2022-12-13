import traceback
from datetime import datetime

import discord
from discord.ext import commands

from common import constants
from testing.integration import leaderboard_integration, list_integration, support_integration, configure_integration, \
    dex_integration, raid_integration, rolewindow_integration, trainercode_integration, roles_integration, \
    achievements_integration
from utils.exception_wrapper import pm_dev_error
from utils.global_error_manager import in_channel_list


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
        for dev in constants.DEVELOPERS:
            user = ctx.bot.get_user(dev)
            await user.send(f"""Error in TEST command: {error}""")

    @commands.command(name="test", help=".", hidden=True)
    @commands.is_owner()
    @in_channel_list(["sneasel_commands"])
    async def test(self, ctx):
        """
        [Admin only]: Run integration-tests in test environment.

        Usage: ?test
        """
        try:
            constants.TEST_RESULTS_CHANNEL = discord.utils.get(ctx.guild.channels, name="test_results")
            await constants.TEST_RESULTS_CHANNEL.send(
                f"""---**INTEGRATION-TESTS - STARTED: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**---""")
            await ctx.send(
                f"Sending results to {constants.TEST_RESULTS_CHANNEL.mention}. This may take a while :sweat_smile:")

            # TODO: Add all the tests to a list or something to run
            await leaderboard_integration.run_tests(self.bot, ctx)
            await list_integration.run_tests(ctx, self.bot)
            await support_integration.run_tests(ctx, self.bot)
            await configure_integration.run_tests(self.bot, ctx)
            await dex_integration.run_tests(self.bot, ctx)
            await raid_integration.run_tests(self.bot, ctx)
            await rolewindow_integration.run_tests(self.bot, ctx)
            await trainercode_integration.run_tests(self.bot, ctx)
            await roles_integration.run_tests(self.bot, ctx)
            await achievements_integration.run_tests(self.bot, ctx)

            await ctx.send(f""":white_check_mark: All integration-tests are a-okay {ctx.message.author.mention}!""")
        except Exception as e:
            traceback.print_exc()
            await ctx.send(f""":no_entry: At least one error found: {e}!""")

    @test.error
    async def test_on_error(self, ctx, error):
        await pm_dev_error(bot=self.bot, error_message=error, source="Test")


async def setup(bot):
    await bot.add_cog(TestManager(bot))
