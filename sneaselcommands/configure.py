import threading
import time

import discord
import schedule
from discord.ext import commands

from utils import scheduler
from utils.channel_wrapper import purge_channel, create_channel, delete_channel
from utils.database_connector import create_insert_scheduled_event_query, create_delete_query, execute_statement, \
    create_select_query
from utils.exception_wrapper import pm_dev_error
from utils.message_wrapper import message_channel
from utils.scheduler import re_schedule_task


def _create_channel(bot: discord.ext.commands.Bot, **kwargs):
    """Schedules the creation of a channel with the specified [channel_name]"""
    bot.loop.create_task(create_channel(bot, kwargs.get("guild"), kwargs.get("channel_name"), kwargs.get("category", None), source="configure/schedule/create_channel"))


def _remove_channel(bot: discord.ext.commands.Bot, **kwargs):
    """Schedules the removal of a channel with the specified [channel_id]"""
    bot.loop.create_task(delete_channel(bot, kwargs.get("channel"), source="Configure/schedule/delete_channel"))


def _schedule_purge(bot: discord.ext.commands.Bot, **kwargs):
    """Schedules a purge of [number] messages in [channel]"""
    number = None if kwargs.get("number") == 0 else kwargs.get("number")
    bot.loop.create_task(purge_channel(bot, kwargs.get("channel"), number, source="configure/schedule/purge"))


def _message_channel(bot: discord.ext.commands.Bot, **kwargs):
    """Schedules a send_message of [message] in channel with the specified [channel_id]"""
    bot.loop.create_task(message_channel(bot, kwargs.get("channel"), kwargs.get("message"), source="configure/schedule/_message_channel"))


def _get_task(task):
    return {
        "create_channel": _create_channel,
        "remove_channel": _remove_channel,
        "purge": _schedule_purge,
        "send_message": _message_channel
    }.get(task)


def _schedule_event(bot: discord.ext.commands.Bot):
    task_info_list = execute_statement(create_select_query("configure__schedule")).all(as_dict=True)
    for task_info in task_info_list:
        local_guild: discord.Guild = bot.get_guild(task_info.get("guild_id"))
        re_schedule_task(
            bot,
            _get_task(task_info.get("task")),
            task_info.get("weekday"),
            task_info.get("at_time"),
            task_info.get("tag"),
            message=task_info.get("message"),
            channel=bot.get_channel(int(task_info.get("channel_id"))),
            number=task_info.get("number"),
            guild=local_guild,
            category=None if local_guild is None else discord.utils.get(local_guild.categories, id=int(task_info.get("category_id")))
        )


class Configure(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot
        bot.loop.create_task(self.start_scheduler())

    async def start_scheduler(self):
        await self.bot.wait_until_ready()
        threading.Thread(name="scheduled_events", target=self._check_scheduled_events).start()

    def _check_scheduled_events(self):
        _schedule_event(self.bot)
        while True:
            schedule.run_pending()
            time.sleep(1)

    @commands.group(hidden=True)
    @commands.has_role("Admin")
    async def configure(self, ctx):
        """Configure base function"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid configure command, options: "
                           "configure schedule create_channel, "
                           "configure schedule delete_channel, "
                           "configure schedule purge, "
                           "configure schedule send_message")

    @configure.error
    async def configure_on_error(self, _, error):
        """Catches errors with configure base command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="configure base command")

    @configure.group()
    @commands.has_role("Admin")
    async def schedule(self, ctx):
        """Base function for scheduling events, use sub-commands add/remove."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid configure sub-command, options: "
                           "configure time_channel add, "
                           "configure time_channel remove")

    @schedule.error
    async def schedule_on_error(self, _, error):
        """Catches errors with schedule base command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="schedule base command")

    @schedule.command()
    @commands.has_role("Admin")
    async def create_channel(self, ctx, channel_name, category_id, weekday, at_time):
        """
        Creates a channel at a specified time every week.

        Usage: ?configure schedule create_channel some_channel_name 12756371253 monday 13:00
        """
        await scheduler.schedule_new_task(
            self.bot,
            ctx,
            _create_channel,
            "configure/schedule/create_channel",
            weekday,
            at_time,
            "create"+channel_name,
            guild=ctx.message.guild,
            channel_name=channel_name,
            category=discord.utils.get(ctx.guild.categories, id=int(category_id))
        )

        if at_time != "0":
            execute_statement(create_insert_scheduled_event_query(
                task="create_channel",
                weekday=weekday,
                at_time=at_time,
                tag="create"+channel_name,
                channel_name=channel_name,
                category_id=int(category_id),
                guild_id=ctx.message.guild.id
            ))

    @create_channel.error
    async def create_channel_on_error(self, _, error):
        """Catches errors with configure schedule create_channel sub-command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="configure schedule create_channel")

    @schedule.command()
    @commands.has_role("Admin")
    async def delete_channel(self, ctx, channel_id, weekday, at_time):
        """
        Deletes a channel at a specified time every week.

        Usage: ?configure schedule delete_channel some_channel_id monday 13:00
        """
        await scheduler.schedule_new_task(
            self.bot,
            ctx,
            _remove_channel,
            "configure/schedule/delete_channel",
            weekday,
            at_time,
            "delete"+channel_id,
            channel=self.bot.get_channel(int(channel_id))
        )

        if at_time != "0":
            execute_statement(create_insert_scheduled_event_query(
                task="remove_channel",
                weekday=weekday,
                at_time=at_time,
                tag="delete"+channel_id,
                channel_id=int(channel_id)
            ))

    @delete_channel.error
    async def delete_channel_on_error(self, _, error):
        """Catches errors with configure schedule delete_channel sub-command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="configure schedule delete_channel")

    @schedule.command()
    @commands.has_role("Admin")
    async def purge(self, ctx, channel_id, weekday, at_time, number_of_messages=0):
        """
        Purges the [number_of_messages] latest messages from the specified channel.
        If no [number_of_messages] is provided the given channel will be emptied.

        Usage: ?configure schedule purge some_channel_id monday 13:00 2
        """
        channel_to_purge = self.bot.get_channel(int(channel_id))
        number = None if number_of_messages == 0 else int(number_of_messages)

        await scheduler.schedule_new_task(
            self.bot,
            ctx,
            _schedule_purge,
            "configure/schedule/purge",
            weekday,
            at_time,
            "purge"+channel_id,
            channel=channel_to_purge,
            number=number
        )

        if at_time != "0":
            execute_statement(create_insert_scheduled_event_query(
                task="purge",
                weekday=weekday,
                at_time=at_time,
                tag="purge"+channel_id,
                channel_id=int(channel_id),
                number=number_of_messages
            ))

    @purge.error
    async def purge_on_error(self, _, error):
        """Catches errors with configure schedule purge sub-command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="schedule purge command")

    @schedule.command()
    @commands.has_role("Admin")
    async def send_message(self, ctx, channel_id, weekday, at_time, *args):
        """
        Sends [message] in the specified channel every [weekday] at [at_time].

        Usage: ?configure schedule send_message 8126387123 monday 13:00 some message here
        """
        await scheduler.schedule_new_task(
            self.bot,
            ctx,
            _message_channel,
            "configure/schedule/send_message",
            weekday,
            at_time,
            "send"+channel_id,
            channel=self.bot.get_channel(int(channel_id)),
            message=" ".join(args[:])
        )

        if at_time != "0":
            execute_statement(create_insert_scheduled_event_query(
                task="send_message",
                weekday=weekday,
                at_time=at_time,
                tag="send"+channel_id,
                channel_id=int(channel_id),
                message=" ".join(args[:])
            ))

    @send_message.error
    async def send_message_on_error(self, _, error):
        """Catches errors with configure schedule send_message sub-command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="configure schedule send_message")

    @commands.command()
    @commands.has_role("Admin")
    async def list_scheduled_events(self, ctx):
        """
        Lists all the current scheduled events.

        Usage: ?list_scheduled_events
        """
        counter = 1
        scheduled_jobs = "**Currently scheduled events:**\n"
        for job in schedule.jobs:
            scheduled_jobs += f"Job {counter}: {job.job_func.__name__}\n"
            scheduled_jobs += f"Runs every {job.interval} {job.unit} at {job.at_time} on {job.start_day}\n"
            scheduled_jobs += f"Last run: {job.last_run}\n"
            scheduled_jobs += f"Next run: {job.next_run}\n"
            scheduled_jobs += f"Tags: {job.tags}\n\n"
            counter += 1
        scheduled_jobs += "..the end"

        await ctx.send(scheduled_jobs)

    @list_scheduled_events.error
    async def list_scheduled_events_on_error(self, _, error):
        """Catches errors with configure schedule list_scheduled_events sub-command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="list_scheduled_events")

    @commands.command()
    @commands.is_owner()
    async def remove_scheduled_events(self, ctx, tag=None):
        """
        Removes a scheduled event.

        For create channel events the tag is create + the channel's name.
        For delete channel events the tag is delete + the channel's id.
        For purge messages from channel the tag is purge + the channel's id.
        For send message in channel the tag is send + the channel's id.

        If no tag is provided then all scheduled events will be canceled.

        Usage: ?remove_scheduled_events createsome_channel_name
        Usage: ?remove_scheduled_events delete182736519823
        Usage: ?remove_scheduled_events purge182736519823
        Usage: ?remove_scheduled_events send182736519823
        """

        schedule.clear(tag)
        if tag is None:
            execute_statement(create_delete_query("configure__schedule"))
            await ctx.send(f"Removed all scheduled events")
        else:
            execute_statement(create_delete_query("configure__schedule", "tag", f"'{tag}'"))
            await ctx.send(f"Removed all scheduled events with tag [{tag}]")

    @remove_scheduled_events.error
    async def remove_scheduled_events_on_error(self, _, error):
        """Catches errors with configure schedule remove_scheduled_events sub-command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="remove_scheduled_events")


def setup(bot):
    bot.add_cog(Configure(bot))
