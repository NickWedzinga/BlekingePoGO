import asyncio

import discord

from utils import exception_wrapper


async def __delete_messages(channel, number):
    """Deletes [number] messages from [channel]"""
    async for message in channel.history(limit=number):
        await message.delete()
        await asyncio.sleep(1.2)


async def purge_channel(bot, channel, number: int = None, source: str = None):
    """Purges a given channel and wraps it with the exception wrapper to alert the developer of any issues"""
    await exception_wrapper.catch_with_pm(bot, __delete_messages, source, channel, number)


async def create_channel(bot, guild, name: str, category: discord.CategoryChannel = None, source: str = None):
    """Creates a channel with the specified [name] under an optionally specified [category]"""
    await exception_wrapper.catch_with_pm(
        bot,
        guild.create_text_channel,
        source,
        name=name,
        category=category
    )


async def delete_channel(bot, channel_id: int, source: str = None):
    """Deletes a channel with the specified [channel_id]"""
    await exception_wrapper.catch_with_pm(
        bot,
        bot.get_channel(channel_id).delete,
        source
    )
