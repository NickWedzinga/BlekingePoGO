import traceback

import discord
from datetime import datetime, timedelta

import common
from utils.database_connector import execute_statement, create_select_query


async def call_raid_tests(bot, ctx):
    try:
        await _run_not_hatched_raid(bot, ctx)
        await _run_hatched_raid(bot, ctx)
        await _run_raid_train(bot, ctx)

        await common.TEST_RESULTS_CHANNEL.send(f":white_check_mark: Raid: Successfully completed the Raid commands.")
    except Exception:
        raise ValueError(f"Error during raid integration-tests")


async def _run_not_hatched_raid(bot, ctx):
    """Run the tests for a non-hatched raid, for example ?raid heatran klockstapeln 18:15"""
    try:
        time = '{:%H:%M}'.format(datetime.now() + timedelta(minutes=2))
        channel_name = f"sneasel_momos-hem_{time.replace(':', '')}"
        await _invoke_raid_command(bot, ctx, "Sneasel", "Momos", "hem", time)
        await _check_created_rows_in_database(ctx)
        await _check_created_channel(ctx, channel_name)

        await _invoke_close_command(bot, ctx, channel_name)
        await _check_deleted_rows_from_database()

        await common.TEST_RESULTS_CHANNEL.send(f":white_check_mark: Raid: Successfully completed non-hatched raid.")
    except Exception:
        raise ValueError(f"Error during raid integration-tests")


async def _run_hatched_raid(bot, ctx):
    """Run the tests for a hatched-raid, for example ?raid heatran klockstapeln"""
    try:
        channel_name = "sneasel_momos-hem"
        await _invoke_raid_command(bot, ctx, "Sneasel", "Momos", "hem")
        await _check_created_rows_in_database(ctx)
        await _check_created_channel(ctx, channel_name)

        await _invoke_close_command(bot, ctx, channel_name)
        await _check_deleted_rows_from_database()

        await common.TEST_RESULTS_CHANNEL.send(f":white_check_mark: Raid: Successfully completed the hatched raid.")
    except Exception:
        raise ValueError(f"Error during raid integration-tests")


async def _run_raid_train(bot, ctx):
    """"""
    try:
        channel_name = "sneasel_train"
        await _invoke_raid_command(bot, ctx, "Sneasel", "train")
        await _check_created_rows_in_database(ctx)
        await _check_created_channel(ctx, channel_name)

        await _invoke_close_command(bot, ctx, channel_name)
        await _check_deleted_rows_from_database()

        await common.TEST_RESULTS_CHANNEL.send(f":white_check_mark: Raid: Successfully completed the raid train.")
    except Exception:
        raise ValueError(f"Error during raid integration-tests")


async def _invoke_raid_command(bot, ctx, *args):
    try:
        raid_command = bot.get_command("raid")
        await ctx.invoke(raid_command, *args)
    except Exception as e:
        traceback.print_exc()
        await common.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during raid invocation: {e}")
        raise ValueError(f"Error during raid invocation")


async def _check_created_rows_in_database(ctx):
    try:
        active_channel_dict = execute_statement(create_select_query(common.ACTIVE_RAID_CHANNEL_OWNERS)).all(as_dict=True)
        assert(len(active_channel_dict) == 1)
        assert(any(channel.get("reporter_id") == ctx.author.id for channel in active_channel_dict))

        schedule_raid_channel_dict = execute_statement(create_select_query(common.SCHEDULE_RAID)).all(as_dict=True)
        assert (3 >= len(schedule_raid_channel_dict) >= 1)
        assert (any(channel.get("reporter_id") in common.DEVELOPERS for channel in schedule_raid_channel_dict))
    except Exception as e:
        traceback.print_exc()
        await common.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during raid checking database: {e}")
        raise ValueError(f"Error during raid checking database for new rows")


async def _check_deleted_rows_from_database():
    try:
        active_channel_dict = execute_statement(create_select_query(common.ACTIVE_RAID_CHANNEL_OWNERS)).all(as_dict=True)
        assert(len(active_channel_dict) == 0)

        schedule_raid_channel_dict = execute_statement(create_select_query(common.SCHEDULE_RAID)).all(as_dict=True)
        assert (len(schedule_raid_channel_dict) == 0)
    except Exception as e:
        traceback.print_exc()
        await common.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during raid checking database: {e}")
        raise ValueError(f"Error during raid checking database, possibly rows not removed")


async def _check_created_channel(ctx, channel_name):
    try:
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if channel is None:
            raise ValueError(f"Error with creating raid channel, can't find the created channel")

        history = await channel.history().flatten()
        assert(len(history) == 1)
        assert(len(history[0].embeds) == 1)

        await common.TEST_RESULTS_CHANNEL.send(f":white_check_mark: Raid: "
                                               f"Verified that the channel created exists!")
    except Exception as e:
        traceback.print_exc()
        await common.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during raid create channel: {e}")
        raise ValueError(f"Error during raid create_channel, can't find the created channel")


async def _invoke_close_command(bot, ctx, channel_name):
    try:
        raid_channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        close_command = bot.get_command("close")
        await ctx.invoke(close_command, raid_channel.id)
    except Exception as e:
        traceback.print_exc()
        await common.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during close invocation: {e}")
        raise ValueError(f"Error during raid invocation")


def _assert_embed_field(embed, field_key, expected_value):
    for field in embed.fields:
        if field.name == field_key:
            assert(field.value == expected_value)
    return AssertionError("Could not find that field")


async def run_tests(bot, ctx):
    await call_raid_tests(bot, ctx)