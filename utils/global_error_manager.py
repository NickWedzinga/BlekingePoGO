from discord.ext import commands

import common
from utils.database_connector import execute_statement, create_select_query


def in_channel_list(channel_list):
    def predicate(ctx):
        return ctx.message.channel.name in channel_list
    return commands.check(predicate)


def validate_active_raid_and_user():
    async def predicate(ctx):
        maybe_channel_dict = execute_statement(create_select_query(common.ACTIVE_RAID_CHANNEL_OWNERS, "channel_id", f"'{ctx.channel.id}'")).all(as_dict=True)

        if "help" not in ctx.invoked_with:
            if not maybe_channel_dict:
                await ctx.send("This command can only be used in a created raid channel")

            if not (any(channel_info.get("reporter_id") == ctx.author.id for channel_info in maybe_channel_dict) or
                    any(role.name in ["Admin", "Moderator"] for role in ctx.author.roles)):
                await ctx.send("This command can only be used by the raid reporter, admins and moderators")

        return maybe_channel_dict and \
               (any(channel_info.get("reporter_id") == ctx.author.id for channel_info in maybe_channel_dict) or
                any(role.name in ["Admin", "Moderator"] for role in ctx.author.roles))
    return commands.check(predicate)


class ErrorHandling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if '@EVERYONE' in message.content.upper() and 342771363884302339 not in [role.id for role in
                                                                                 message.author.roles]:
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
