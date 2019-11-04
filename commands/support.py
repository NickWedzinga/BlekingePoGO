from discord.ext import commands
import Common
import leaderboards


class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="refresh", pass_context=True, help="This command refreshes a given leaderboard."
                                                              "Example: ?refresh jogger")
    async def refresh(self, ctx, leaderboard_type):
        leaderboard_type = leaderboard_type.lower()

        if leaderboard_type in Common.leaderboard_list:
            await leaderboards.leaderboard(ctx, ctx.message)

    @refresh.error
    async def refresh_on_error(self, ctx, error):
        for dev in Common.developers:
            user = ctx.bot.get_user(dev)
            await user.send(f"""Error in REFRESH command: {error}""")


def setup(bot):
    bot.add_cog(Support(bot))