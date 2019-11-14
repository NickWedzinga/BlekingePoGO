import traceback

from discord.ext import commands

import Common
from testing.integration import leaderboard_tests, list_tests
from datetime import datetime


class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="healthcheck", pass_context=True, help="This command acts as a health-check.")
    async def healthcheck(self, ctx):
        await ctx.send(f"""..zzzZZ.. va? Jag är vaken {ctx.message.author.mention}! :sweat_smile:""")

    @healthcheck.error
    async def healthcheck_on_error(self, ctx, error):
        traceback.print_exc()
        for dev in Common.developers:
            user = ctx.bot.get_user(dev)
            await user.send(f"""Error in TEST command: {error}""")

    @commands.command(name="test", pass_context=True, help="This command acts as a health-check.")
    async def test(self, ctx):
        if ctx.message.author.id in Common.developers and str(ctx.message.channel) == Common.command_channel_list[1]:
            try:
                Common.test_results_channel = self.bot.get_channel(640964820732084233)
                await Common.test_results_channel.send(f"""---**INTEGRATION-TESTS - STARTED: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**---""")
                await ctx.send(f"Sending results to {Common.test_results_channel.mention}. This may take a while :sweat_smile:")
                await leaderboard_tests.run_tests(ctx)
                await list_tests.run_tests(ctx)
                await ctx.send(f""":white_check_mark: All integration-tests are a-okay {ctx.message.author.mention}!""")
            except Exception as e:
                await ctx.send(f""":no_entry: At least one error found: {e}!""")

    @test.error
    async def test_on_error(self, ctx, error):
        traceback.print_exc()
        for dev in Common.developers:
            user = ctx.bot.get_user(dev)
            await user.send(f"""Error in TEST command: {error}""")


def setup(bot):
    bot.add_cog(Testing(bot))