import inspect
import logging
import traceback
from typing import Union

from discord import Client
from discord.ext import commands
from discord.ext.commands import Bot

from common import constants


def _formatted_error_log(source: str = "unspecified", error_message: str = None):
    """
    Returns a formatted error log containing the function that raised the Exception
    as well as the stacktrace.
    """
    return f"""-------------------------------------------------------------------------------------------
    **Error[{source}]:**
    **Additional info: {error_message}\n**
    {traceback.format_exc()}-------------------------------------------------------------------------------------------
    """


async def catch_with_logging(function_to_try, source: str, *args, **kwargs):
    try:
        if inspect.iscoroutinefunction(function_to_try):
            await function_to_try(*args, **kwargs)
        else:
            function_to_try(*args, **kwargs)
    except (Exception,):
        logging.exception(f'Error occurred in source: [{source}]')


async def catch_with_pm(bot, function_to_try, source: str, *args, **kwargs):
    try:
        if inspect.iscoroutinefunction(function_to_try):
            await function_to_try(*args, **kwargs)
        else:
            function_to_try(*args, **kwargs)
    except (Exception,):
        await pm_dev_error(bot, source=source)


async def catch_with_channel_message(function_to_try, channel, catch_message, should_throw: bool, source: str, *args):
    try:
        if inspect.iscoroutinefunction(function_to_try):
            await function_to_try(*args[:-1], args[-1])
        else:
            function_to_try(*args[:-1], args[-1])
    except Exception as e:
        await channel.send(f"{catch_message} {e}")
        if should_throw:
            raise ValueError(f"Error when called from {source}")


async def catch_with_pm_and_channel_message(bot, function_to_try, channel, catch_message, source: str, *args):
    try:
        if inspect.iscoroutinefunction(function_to_try):
            await function_to_try(*args[:-1], args[-1])
        else:
            function_to_try(*args[:-1], args[-1])
    except (Exception,):
        await channel.send(f"{catch_message}")
        await pm_dev_error(bot, source=source)


async def channel_send_error(ctx, error_message=None, source="unspecified"):
    if not isinstance(error_message, commands.errors.CheckFailure):
        await ctx.send(_formatted_error_log(source=source, error_message=error_message)[:1999])


async def pm_dev_error(client: Union[Client, Bot], error_message=None, source="unspecified"):
    if not isinstance(error_message, commands.errors.CheckFailure):
        for dev in constants.DEVELOPERS:
            user = client.get_user(dev)
            if user:
                await user.send(_formatted_error_log(source=source, error_message=error_message)[:1999])
            else:
                logging.exception(f'Error: could not find developer user to DM')
