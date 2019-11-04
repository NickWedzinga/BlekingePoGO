from discord.ext import commands
import Common


class Leaderboards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=Common.leaderboard_list, pass_context=True, help="This command adds an entry to a given"
                                                                               " leaderboard.\nExample: ?jogger 507")
    async def leaderboard(self, ctx):
        await ctx.send(f"""..zzzZZ.. va? Jag är vaken {ctx.message.author.mention}! :sweat_smile:""")

    @leaderboard.error
    async def leaderboard_on_error(self, ctx, error):
        for dev in Common.developers:
            user = ctx.bot.get_user(dev)
            await user.send(f"""Error in LEADERBOARD command: {error}""")


def setup(bot):
    bot.add_cog(Leaderboards(bot))
