import schedule

import common
from sneaselcommands.raids.utils.raid_embeds import update_time_in_embed
from utils.database_connector import execute_statement, create_insert_query, create_delete_query
from utils.scheduler import schedule_new_hourly_task, schedule_new_daily_task


def get_interval(interval):
    return {
        "hourly": schedule_new_hourly_task,
        "daily": schedule_new_daily_task
    }.get(interval)


async def update_raids_channel(bot, ctx):
    update_raids = bot.get_cog("Raids")
    if update_raids is not None:
        await update_raids.raids(ctx)


def schedule_reminding_task(bot, ctx, created_channel, message, at_time, task_interval):
    """Schedules a reminding message that executes every hour, used for raid train channels"""
    get_interval(task_interval)(
        remind_task,
        f"send{created_channel.id}",
        bot=bot,
        channel=created_channel,
        at_time=at_time,
        message=message)

    execute_statement(create_insert_query(
        table_name=common.SCHEDULE_RAID,
        keys="(task, task_interval, at_time, tag, channel_id, reporter_id, message)",
        values=f"('remind', '{task_interval}', '{at_time}', 'send{created_channel.id}', {created_channel.id}, {ctx.author.id}, '{message}')"
    ))


def remind_task(**kwargs):
    kwargs.get("bot").loop.create_task(kwargs.get("channel").send(kwargs.get("message")))


def schedule_delete_channel_at(bot, ctx, created_channel, at_time):
    """Schedules the deletion of the raid channel"""
    schedule_new_daily_task(
        delete_channel_at_time,
        f"delete{created_channel.id}",
        bot=bot,
        ctx=ctx,
        channel=created_channel,
        at_time=at_time)

    execute_statement(create_insert_query(
        table_name=common.SCHEDULE_RAID,
        keys="(task, task_interval, at_time, tag, channel_id, reporter_id, message)",
        values=f"('remove_channel_at', 'daily', '{at_time}', 'delete{created_channel.id}', {created_channel.id}, {ctx.author.id}, 'empty')"
    ))


def delete_channel_at_time(**kwargs):
    kwargs.get("bot").loop.create_task(kwargs.get("channel").delete())

    channel_id = kwargs.get("channel").id
    execute_statement(create_delete_query(
        table_name=common.ACTIVE_RAID_CHANNEL_OWNERS,
        where_key="channel_id",
        where_value=channel_id))

    execute_statement(create_delete_query(
        table_name=common.SCHEDULE_RAID,
        where_key="channel_id",
        where_value=channel_id))

    # TODO: Can't get context from configure upon start-up, so can't run raids command upon restart
    if kwargs.get("ctx") is not None:
        kwargs.get("bot").loop.create_task(update_raids_channel(kwargs.get("bot"), kwargs.get("ctx")))
    return schedule.CancelJob


def schedule_edit_embed(bot, ctx, channel, at_time):
    """Schedules an edit of an embed"""
    schedule_new_daily_task(
        update_embed,
        f"edit_embed{channel.id}",
        bot=bot,
        ctx=ctx,
        channel=channel,
        at_time=at_time)

    execute_statement(create_insert_query(
        table_name=common.SCHEDULE_RAID,
        keys="(task, task_interval, at_time, tag, channel_id, reporter_id, message)",
        values=f"('edit_embed', 'daily', '{at_time}', 'edit_embed{channel.id}', {channel.id}, {0}, 'empty')"
    ))


def update_embed(**kwargs):
    """Updates an existing embed, deletes schedule from db since it's done now, cancels scheduled job"""
    kwargs.get("bot").loop.create_task(update_time_in_embed(**kwargs))

    execute_statement(create_delete_query(
        table_name=common.SCHEDULE_RAID,
        where_key="tag",
        where_value=f"'edit_embed{kwargs.get('channel').id}'"))

    # TODO: Can't get context from configure upon start-up, so can't run raids command upon restart
    if kwargs.get("ctx") is not None:
        kwargs.get("bot").loop.create_task(update_raids_channel(kwargs.get("bot"), kwargs.get("ctx")))
    return schedule.CancelJob
