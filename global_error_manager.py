from discord.ext import commands

import common
from instance import bot  # TODO: causes test to fail, don't reimport, pass the bot instance around


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


def in_channel_list(channel_id_list):
    def predicate(ctx):
        return ctx.message.channel.id in channel_id_list
    return commands.check(predicate)

# TODO: Somehow place this under ErrorHandling cog without losing global check
@bot.check
@in_channel_list(common.COMMAND_CHANNEL_LIST)
async def global_channel_check(ctx):
    common.INTEGRATION_TESTING = False
    if str(ctx.invoked_with) == "test":  # TODO: could this be reworked to remove integration workaround boolean?
        common.INTEGRATION_TESTING = True
        return True
    elif str(ctx.invoked_with) != "claim":
        if str(ctx.message.channel) == common.COMMAND_CHANNEL_LIST[2]:
            return False
        return True
    return True
