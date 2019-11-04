from discord.ext import commands
import Common


class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test", pass_context=True, help="This command acts as a health-check.")
    async def test(self, ctx):
        await ctx.send(f"""..zzzZZ.. va? Jag är vaken {ctx.message.author.mention}! :sweat_smile:""")

    @test.error
    async def test_on_error(self, ctx, error):
        for dev in Common.developers:
            user = ctx.bot.get_user(dev)
            await user.send(f"""Error in TEST command: {error}""")


def setup(bot):
    bot.add_cog(Testing(bot))