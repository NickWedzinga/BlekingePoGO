import discord
import discord.ext.commands.context
from discord.ext import commands

from sneaselcommands.raids.utils.raid_scheduler import cancel_all_scheduled_events_for_raid_channel
from sneaselcommands.raids.utils.raid_scheduler import update_raids_channel
from utils.exception_wrapper import pm_dev_error
from utils.global_error_manager import validate_active_raid_and_user


class Close(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="close")
    @validate_active_raid_and_user()
    async def close(self, ctx, channel_id=None):
        """
        Used to close active raid channels when the raid is done.
        Can only be called by the reporter or admins/moderators.

        Usage: ?close
        """
        channel = ctx.channel if channel_id is None else discord.utils.get(ctx.guild.channels, id=channel_id)
        await channel.delete()

        cancel_all_scheduled_events_for_raid_channel(channel_id=ctx.channel.id if channel_id is None else channel_id)

        await update_raids_channel(self.bot, ctx)

    @close.error
    async def close_on_error(self, _, error):
        await pm_dev_error(bot=self.bot, error_message=error, source="Close")


def setup(bot):
    bot.add_cog(Close(bot))
