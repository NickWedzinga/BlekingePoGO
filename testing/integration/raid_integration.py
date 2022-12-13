import traceback
from datetime import datetime, timedelta

import discord

from common import constants, tables
from utils.database_connector import execute_statement, create_select_query
from utils.time_wrapper import format_as_hhmm


async def call_raid_tests(bot, ctx):
    try:
        await _run_not_hatched_raid(bot, ctx)
        await _run_hatched_raid(bot, ctx)
        await _run_hatched_raid_despawn_time(bot, ctx)
        await _run_raid_train(bot, ctx)

        await constants.TEST_RESULTS_CHANNEL.send(f":white_check_mark: Raid: Successfully completed the Raid commands.")
    except Exception:
        raise ValueError(f"Error during raid integration-tests")


async def _run_not_hatched_raid(bot, ctx):
    """Run the tests for a non-hatched raid, for example ?raid heatran klockstapeln 18:15"""
    try:
        time = format_as_hhmm(datetime.now() + timedelta(minutes=2))
        update_time = format_as_hhmm(datetime.now() + timedelta(minutes=4))
        channel_name = f"{time.replace(':', '')}_sneasel_momos-hem"
        updated_name = f"{time.replace(':', '')}_weavile_momos-hem"

        await _invoke_raid_command(bot, ctx, "Sneasel", "Momos", "hem", time)
        await _check_created_rows_in_database(ctx)
        await _check_created_channel(ctx, channel_name)

        await _invoke_update_command(bot, ctx, channel_name, update_time)

        await _invoke_close_command(bot, ctx, updated_name)
        await _check_deleted_rows_from_database()

        await constants.TEST_RESULTS_CHANNEL.send(f":white_check_mark: Raid: Successfully completed non-hatched raid.")
    except Exception:
        raise ValueError(f"Error during raid integration-tests")


async def _run_hatched_raid(bot, ctx):
    """Run the tests for a hatched-raid, for example ?raid heatran klockstapeln"""
    try:
        time = format_as_hhmm(datetime.now() + timedelta(minutes=2))
        channel_name = "sneasel_momos-hem"
        updated_name = "weavile_momos-hem"

        await _invoke_raid_command(bot, ctx, "Sneasel", "Momos", "hem")
        await _check_created_rows_in_database(ctx)
        await _check_created_channel(ctx, channel_name)

        await _invoke_update_command(bot, ctx, channel_name, time)

        await _invoke_close_command(bot, ctx, updated_name)
        await _check_deleted_rows_from_database()

        await constants.TEST_RESULTS_CHANNEL.send(f":white_check_mark: Raid: Successfully completed the hatched raid.")
    except Exception:
        raise ValueError(f"Error during raid integration-tests")


async def _run_hatched_raid_despawn_time(bot, ctx):
    """Run the tests for a raid with despawn time, for example ?raid heatran klockstapeln 32"""
    try:
        time = format_as_hhmm(datetime.now() - timedelta(minutes=30))
        channel_name = f"{time.replace(':', '')}_sneasel_momos-hem"
        updated_name = f"{time.replace(':', '')}_weavile_momos-hem"

        await _invoke_raid_command(bot, ctx, "Sneasel", "Momos", "hem", "15")
        await _check_created_rows_in_database(ctx)
        await _check_created_channel(ctx, channel_name)

        await _invoke_update_command(bot, ctx, channel_name, time)

        await _invoke_close_command(bot, ctx, updated_name)
        await _check_deleted_rows_from_database()

        await constants.TEST_RESULTS_CHANNEL.send(f":white_check_mark: Raid: Successfully completed the hatched raid.")
    except Exception:
        raise ValueError(f"Error during raid integration-tests")


async def _run_raid_train(bot, ctx):
    """Run the tests for a raid train channel, for example ?raid sneasel train"""
    try:
        time = format_as_hhmm(datetime.now() + timedelta(minutes=2))
        channel_name = "sneasel_train"
        updated_name = "weavile_train"

        await _invoke_raid_command(bot, ctx, "Sneasel", "train")
        await _check_created_rows_in_database(ctx)
        await _check_created_channel(ctx, channel_name)

        await _invoke_update_command(bot, ctx, channel_name, time)

        await _invoke_close_command(bot, ctx, updated_name)
        await _check_deleted_rows_from_database()

        await constants.TEST_RESULTS_CHANNEL.send(f":white_check_mark: Raid: Successfully completed the raid train.")
    except Exception:
        raise ValueError(f"Error during raid integration-tests")


async def _invoke_raid_command(bot, ctx, *args):
    try:
        raid_command = bot.get_command("raid")
        await ctx.invoke(raid_command, *args)
    except Exception as e:
        traceback.print_exc()
        await constants.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during raid invocation: {e}")
        raise ValueError(f"Error during raid invocation")


async def _check_created_rows_in_database(ctx):
    try:
        active_channel_dict = execute_statement(create_select_query(tables.ACTIVE_RAID_CHANNEL_OWNERS)).all(as_dict=True)
        assert(len(active_channel_dict) == 1)
        assert(any(channel.get("reporter_id") == ctx.author.id for channel in active_channel_dict))

        schedule_raid_channel_dict = execute_statement(create_select_query(tables.SCHEDULE_RAID)).all(as_dict=True)
        assert (3 >= len(schedule_raid_channel_dict) >= 1)
        assert (any(channel.get("reporter_id") in constants.DEVELOPERS for channel in schedule_raid_channel_dict))
    except Exception as e:
        traceback.print_exc()
        await constants.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during raid checking database: {e}")
        raise ValueError(f"Error during raid checking database for new rows")


async def _check_deleted_rows_from_database():
    try:
        active_channel_dict = execute_statement(create_select_query(tables.ACTIVE_RAID_CHANNEL_OWNERS)).all(as_dict=True)
        assert(len(active_channel_dict) == 0)

        schedule_raid_channel_dict = execute_statement(create_select_query(tables.SCHEDULE_RAID)).all(as_dict=True)
        assert (len(schedule_raid_channel_dict) == 0)
    except Exception as e:
        traceback.print_exc()
        await constants.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during raid checking database: {e}")
        raise ValueError(f"Error during raid checking database, possibly rows not removed")


async def _check_created_channel(ctx, channel_name):
    try:
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if channel is None:
            raise ValueError(f"Error with creating raid channel, can't find the created channel")

        history = [log async for log in channel.history()]
        assert(len(history) == 1)
        assert(len(history[0].embeds) == 1)
        assert(channel.category.name == f"{ctx.channel.category} raids")

        await constants.TEST_RESULTS_CHANNEL.send(f":white_check_mark: Raid: "
                                               f"Verified that the channel created exists!")
    except Exception as e:
        traceback.print_exc()
        await constants.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during raid create channel: {e}")
        raise ValueError(f"Error during raid create_channel, can't find the created channel")


async def _invoke_update_command(bot, ctx, channel_name: str, time: str):
    try:
        raid_channel = discord.utils.get(ctx.guild.channels, name=channel_name)

        update_command = bot.get_command("update pokemon")
        await ctx.invoke(update_command, "weavile", channel_id=raid_channel.id)

        update_command = bot.get_command("update gym")
        await ctx.invoke(update_command, "adam och eva", channel_id=raid_channel.id)

        update_command = bot.get_command("update hatch")
        await ctx.invoke(update_command, time, channel_id=raid_channel.id)

        update_command = bot.get_command("update despawn")
        await ctx.invoke(update_command, "1", channel_id=raid_channel.id)
    except Exception as e:
        traceback.print_exc()
        await constants.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during close invocation: {e}")
        raise ValueError(f"Error during raid invocation")


async def _invoke_close_command(bot, ctx, channel_name):
    try:
        raid_channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        close_command = bot.get_command("close")
        await ctx.invoke(close_command, raid_channel.id)
    except Exception as e:
        traceback.print_exc()
        await constants.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during close invocation: {e}")
        raise ValueError(f"Error during raid invocation")


def _assert_embed_field(embed, field_key, expected_value):
    for field in embed.fields:
        if field.name == field_key:
            assert(field.value == expected_value)
    return AssertionError("Could not find that field")


async def run_tests(bot, ctx):
    await call_raid_tests(bot, ctx)
