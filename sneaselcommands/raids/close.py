import discord
import discord.ext.commands.context
import schedule
from discord.ext import commands

import common
from sneaselcommands.raids.utils.raid_scheduler import update_raids_channel
from utils.database_connector import execute_statement, create_delete_query
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

        execute_statement(create_delete_query(
            table_name=common.ACTIVE_RAID_CHANNEL_OWNERS,
            where_key="channel_id",
            where_value=f"{ctx.channel.id if channel_id is None else channel_id}"))

        execute_statement(create_delete_query(
            table_name=common.SCHEDULE_RAID,
            where_key="channel_id",
            where_value=f"{ctx.channel.id if channel_id is None else channel_id}"))

        schedule.clear(f"send{ctx.channel.id if channel_id is None else channel_id}")
        schedule.clear(f"delete{ctx.channel.id if channel_id is None else channel_id}")
        schedule.clear(f"edit_embed{ctx.channel.id if channel_id is None else channel_id}")

        await update_raids_channel(self.bot, ctx)

    @close.error
    async def close_on_error(self, _, error):
        await pm_dev_error(bot=self.bot, error_message=error, source="Close")


def setup(bot):
    bot.add_cog(Close(bot))
