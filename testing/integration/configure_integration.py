import calendar
import logging
from datetime import datetime, timedelta

import discord
import schedule

from common import constants
from testing.integration.test_utils import invoke_wrapper
from utils.exception_wrapper import catch_with_channel_message


async def call_configure_tests(bot, ctx):
    """Calls all the sub-commands of configure"""
    channel_name = "test_create_channel"

    await test_clean_table(bot, ctx)
    await test_create_channel(bot, ctx, channel_name)
    await test_send_message(bot, ctx, channel_name)
    await test_purge(bot, ctx, channel_name)
    await test_delete_channel(bot, ctx, channel_name)
    await test_remove_scheduled_events(bot, ctx, channel_name)


async def test_clean_table(bot, ctx):
    """Cleans any leftover scheduled events in case of previously broken tests"""
    await catch_with_channel_message(
        invoke_wrapper.invoke_event_now,
        constants.TEST_RESULTS_CHANNEL,
        f":no_entry: Error during remove_scheduled_events inital cleanup",
        True,
        "integration/schedule/remove_scheduled_events",
        bot,
        ctx,
        "remove_scheduled_events",
        "Schedule"
    )
    assert (len(schedule.jobs) == 0)


async def test_create_channel(bot, ctx, channel_name):
    """Test the configure schedule create_channel command"""
    today = calendar.day_name[datetime.today().weekday()]
    time_to_run = "0"

    await catch_with_channel_message(
        invoke_wrapper.invoke_event_now,
        constants.TEST_RESULTS_CHANNEL,
        f":no_entry: Error during configure schedule create_channel invocation",
        True,
        "integration/schedule/create_channel",
        bot,
        ctx,
        "configure schedule create_channel",
        "Schedule",
        *[channel_name, 469121458904367125, str(today), time_to_run]
    )

    try:
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if channel is None:
            raise ValueError(f"Error during create_channel, can't find the created channel")
        await constants.TEST_RESULTS_CHANNEL.send(f":white_check_mark: Schedule[create_channel]: "
                                               f"Verified that the channel created exists!")
    except Exception as e:
        logging.exception(e)
        await constants.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during configure schedule create_channel "
                                               f"can't find the created_channel: {e}")
        raise ValueError(f"Error during create_channel, can't find the created channel")


async def test_send_message(bot, ctx, channel_name):
    """Test the configure schedule send_message command"""
    today = calendar.day_name[datetime.today().weekday()]
    time_to_run = "0"
    channel_id = discord.utils.get(ctx.guild.channels, name=channel_name).id

    channel = discord.utils.get(ctx.guild.channels, id=channel_id)
    logs = [log async for log in channel.history()]
    assert (len(logs) == 0)

    await catch_with_channel_message(
        invoke_wrapper.invoke_event_now,
        constants.TEST_RESULTS_CHANNEL,
        f":no_entry: Error during configure schedule send_message invocation",
        True,
        "integration/schedule/send_message",
        bot,
        ctx,
        "configure schedule send_message",
        "Schedule",
        *[str(channel_id), str(today), time_to_run, "test-message"],
    )

    logs = [log async for log in channel.history()]
    assert(len(logs) == 1)


async def test_purge(bot, ctx, channel_name):
    """Test the configure schedule purge command"""
    today = calendar.day_name[datetime.today().weekday()]
    time_to_run = "0"
    channel_id = str(discord.utils.get(ctx.guild.channels, name=channel_name).id)

    await catch_with_channel_message(
        invoke_wrapper.invoke_event_now,
        constants.TEST_RESULTS_CHANNEL,
        f":no_entry: Error during configure schedule purge invocation",
        True,
        "integration/schedule/purge",
        bot,
        ctx,
        "configure schedule purge",
        "Schedule",
        *[channel_id, str(today), time_to_run]
    )


async def test_delete_channel(bot, ctx, channel_name):
    """Test the configure schedule delete_channel command"""
    today = calendar.day_name[datetime.today().weekday()]
    time_to_run = "0"
    channel_id = str(discord.utils.get(ctx.guild.channels, name=channel_name).id)

    await catch_with_channel_message(
        invoke_wrapper.invoke_event_now,
        constants.TEST_RESULTS_CHANNEL,
        f":no_entry: Error during configure schedule delete_channel invocation",
        True,
        "integration/schedule/delete_channel",
        bot,
        ctx,
        "configure schedule delete_channel",
        "Schedule",
        *[channel_id, str(today), time_to_run],
    )


async def test_remove_scheduled_events(bot, ctx, channel_name):
    """Test the remove_scheduled_events command"""
    today = calendar.day_name[datetime.today().weekday()]
    time_to_run = str((datetime.now() + timedelta(minutes=1)).time())[:8]

    await catch_with_channel_message(
        invoke_wrapper.invoke_event_now,
        constants.TEST_RESULTS_CHANNEL,
        f":no_entry: Error during configure schedule create_channel invocation",
        True,
        "integration/schedule/create_channel",
        bot,
        ctx,
        "configure schedule create_channel",
        "Schedule",
        *[channel_name, 469121458904367125, str(today), time_to_run]
    )
    assert(len(schedule.jobs) == 1)
    await catch_with_channel_message(
        invoke_wrapper.invoke_event_now,
        constants.TEST_RESULTS_CHANNEL,
        f":no_entry: Error during list_scheduled_events invocation",
        True,
        "integration/schedule/list_scheduled_events",
        bot,
        ctx,
        "list_scheduled_events",
        "Schedule"
    )

    await catch_with_channel_message(
        invoke_wrapper.invoke_event_now,
        constants.TEST_RESULTS_CHANNEL,
        f":no_entry: Error during remove_scheduled_events invocation",
        True,
        "integration/schedule/remove_scheduled_events",
        bot,
        ctx,
        "remove_scheduled_events",
        "Schedule",
        *["create"+channel_name]
    )
    assert (len(schedule.jobs) == 0)


async def run_tests(bot, ctx):
    await call_configure_tests(bot, ctx)
