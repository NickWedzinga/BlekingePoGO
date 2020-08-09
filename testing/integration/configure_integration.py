import calendar
import traceback
from datetime import datetime, timedelta

import discord
import schedule

import common
from utils.exception_wrapper import catch_with_channel_message


async def _invoke_scheduled_event_now(bot, ctx, command, **kwargs):
    cmd = bot.get_command(f"configure schedule {command}")
    await ctx.invoke(cmd, **kwargs)
    await common.TEST_RESULTS_CHANNEL.send(f":white_check_mark: Schedule[{command}]: Successfully invoked the {command} command.")


async def call_configure_tests(bot, ctx):
    """Calls all the sub-commands of configure"""
    channel_name = "test_create_channel"

    await test_create_channel(bot, ctx, channel_name)
    await test_send_message(bot, ctx, channel_name)
    await test_purge(bot, ctx, channel_name)
    await test_delete_channel(bot, ctx, channel_name)
    await test_remove_scheduled_events(bot, ctx, channel_name)


async def test_create_channel(bot, ctx, channel_name):
    """Test the configure schedule create_channel command"""
    today = calendar.day_name[datetime.today().weekday()]
    time_to_run = "0"

    await catch_with_channel_message(
        _invoke_scheduled_event_now,
        common.TEST_RESULTS_CHANNEL,
        f":no_entry: Error during configure schedule create_channel invocation",
        True,
        "integration/schedule/create_channel",
        bot,
        ctx,
        "create_channel",
        **{"channel_name": channel_name, "category_id": 469121458904367125, "weekday": str(today), "at_time": time_to_run}
    )

    try:
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if channel is None:
            raise ValueError(f"Error during create_channel, can't find the created channel")
        await common.TEST_RESULTS_CHANNEL.send(f":white_check_mark: Schedule[create_channel]: "
                                               f"Verified that the channel created exists!")
    except Exception as e:
        traceback.print_exc()
        await common.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during configure schedule create_channel "
                                               f"can't find the created_channel: {e}")
        raise ValueError(f"Error during create_channel, can't find the created channel")


async def test_send_message(bot, ctx, channel_name):
    """Test the configure schedule send_message command"""
    today = calendar.day_name[datetime.today().weekday()]
    time_to_run = "0"
    channel_id = discord.utils.get(ctx.guild.channels, name=channel_name).id

    channel = discord.utils.get(ctx.message.guild.channels, id=channel_id)
    logs = await channel.history().flatten()
    assert (len(logs) == 0)

    await catch_with_channel_message(
        _invoke_scheduled_event_now,
        common.TEST_RESULTS_CHANNEL,
        f":no_entry: Error during configure schedule send_message invocation",
        True,
        "integration/schedule/send_message",
        bot,
        ctx,
        "send_message",
        **{"channel_id": str(channel_id), "weekday": str(today), "at_time": time_to_run},
    )

    logs = await channel.history().flatten()
    assert(len(logs) == 1)


async def test_purge(bot, ctx, channel_name):
    """Test the configure schedule purge command"""
    today = calendar.day_name[datetime.today().weekday()]
    time_to_run = "0"
    channel_id = str(discord.utils.get(ctx.guild.channels, name=channel_name).id)

    await catch_with_channel_message(
        _invoke_scheduled_event_now,
        common.TEST_RESULTS_CHANNEL,
        f":no_entry: Error during configure schedule purge invocation",
        True,
        "integration/schedule/purge",
        bot,
        ctx,
        "purge",
        **{"channel_id": channel_id, "weekday": str(today), "at_time": time_to_run},
    )


async def test_delete_channel(bot, ctx, channel_name):
    """Test the configure schedule delete_channel command"""
    today = calendar.day_name[datetime.today().weekday()]
    time_to_run = "0"
    channel_id = str(discord.utils.get(ctx.guild.channels, name=channel_name).id)

    await catch_with_channel_message(
        _invoke_scheduled_event_now,
        common.TEST_RESULTS_CHANNEL,
        f":no_entry: Error during configure schedule delete_channel invocation",
        True,
        "integration/schedule/delete_channel",
        bot,
        ctx,
        "delete_channel",
        **{"channel_id": channel_id, "weekday": str(today), "at_time": time_to_run},
    )


async def test_remove_scheduled_events(bot, ctx, channel_name):
    """Test the configure schedule remove_scheduled_events command"""
    today = calendar.day_name[datetime.today().weekday()]
    time_to_run = str((datetime.now() + timedelta(minutes=1)).time())[:8]

    await catch_with_channel_message(
        _invoke_scheduled_event_now,
        common.TEST_RESULTS_CHANNEL,
        f":no_entry: Error during configure schedule create_channel invocation",
        True,
        "integration/schedule/create_channel",
        bot,
        ctx,
        "create_channel",
        **{"channel_name": channel_name, "category_id": 469121458904367125, "weekday": str(today),
           "at_time": time_to_run}
    )
    assert(len(schedule.jobs) == 1)
    await catch_with_channel_message(
        _invoke_scheduled_event_now,
        common.TEST_RESULTS_CHANNEL,
        f":no_entry: Error during configure schedule list_scheduled_events invocation",
        True,
        "integration/schedule/list_scheduled_events",
        bot,
        ctx,
        "list_scheduled_events"
    )

    await catch_with_channel_message(
        _invoke_scheduled_event_now,
        common.TEST_RESULTS_CHANNEL,
        f":no_entry: Error during configure schedule remove_scheduled_events invocation",
        True,
        "integration/schedule/remove_scheduled_events",
        bot,
        ctx,
        "remove_scheduled_events",
        **{"tag": "create"+channel_name}
    )
    assert (len(schedule.jobs) == 0)


async def run_tests(bot, ctx):
    await call_configure_tests(bot, ctx)
