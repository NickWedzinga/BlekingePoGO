from discord.ext import commands
import Common


class ErrorHandling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if '@EVERYONE' in message.content.upper() and 342771363884302339 not in [role.id for role in message.author.roles]:
            for role in message.guild.roles:
                if 435908470936698910 == role.id:
                    await message.channel.send("Ping! %s" % role.mention)
                elif 342771363884302339 == role.id:
                    await message.channel.send("Ping! %s" % role.mention)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"Command [{ctx.invoked_with}] was not found.")
        for dev in Common.developers:
            user = ctx.bot.get_user(dev)
            await user.send(f"""GENERIC error in command: {error}""")

    # global check that applies to all sneaselcommands
    # checks if sneaselcommands was sent from an expected channel
    # reads as, message was sent in a command channel and a command, other than claim, was not sent in support channel
    @commands.Cog.listener()
    async def global_channel_check(self, ctx):  # TODO: Can this be one-lined without losing readability?

        if str(ctx.message.channel) not in Common.command_channel_list:
            return False
        elif str(ctx.invoked_with) != "claim":
            if str(ctx.message.channel) == Common.command_channel_list[2]:
                return False
            return True
        else:
            return True


def setup(bot):
    bot.add_cog(ErrorHandling(bot))