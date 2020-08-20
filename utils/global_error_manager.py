from discord.ext import commands


def in_channel_list(channel_list):
    def predicate(ctx):
        return ctx.message.channel.name in channel_list
    return commands.check(predicate)


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
            await ctx.send(f"Command [**{ctx.invoked_with}**] was not found.")


def setup(bot):
    bot.add_cog(ErrorHandling(bot))
