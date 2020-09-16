import asyncio
from typing import Optional

import discord

from utils import exception_wrapper


async def delete_channel_messages(channel, number=None, should_delay_between_deletes=True):
    """Deletes [number] messages from [channel]"""
    async for message in channel.history(limit=number):
        await message.delete()
        if should_delay_between_deletes:
            await asyncio.sleep(1.2)


async def purge_channel(bot, channel, number: int = None, source: str = None):
    """Purges a given channel and wraps it with the exception wrapper to alert the developer of any issues"""
    await exception_wrapper.catch_with_pm(bot, delete_channel_messages, source, channel, number)


async def create_channel(bot, guild, name: str, category: discord.CategoryChannel = None, source: str = None):
    """Creates a channel with the specified [name] under an optionally specified [category]"""
    await exception_wrapper.catch_with_pm(
        bot,
        guild.create_text_channel,
        source,
        name=name,
        category=category
    )


async def delete_channel(bot, channel, source: str = None):
    """Deletes a channel with the specified [channel_id]"""
    await exception_wrapper.catch_with_pm(
        bot,
        channel.delete,
        source
    )


async def find_embed_in_channel(bot, channel: Optional[discord.TextChannel], source: str, should_pm: bool = True) -> Optional[discord.Message]:
    """
    Returns the first message containing an embed in the provided channel
    If the channel/embed doesn't exist, will pm_dev_error and return None
    """
    if channel is not None:
        async for message in channel.history(oldest_first=True):
            if message.embeds:
                return message

    if should_pm:
        await exception_wrapper.pm_dev_error(
            bot=bot,
            error_message="Unable to find embed channel" if channel is None else "Unable to find embed in channel",
            source=source)
    return None
