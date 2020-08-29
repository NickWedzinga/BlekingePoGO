from utils import exception_wrapper


async def message_channel(bot, channel, message: str, source="unspecified"):
    """
    Sends a single message in a channel.
    """
    await exception_wrapper.catch_with_pm(bot, channel.send, source, message)


async def message_user(bot, user, message: str, source: str = "unspecified"):
    """
    Sends a single message to a user.
    """
    await exception_wrapper.catch_with_pm(bot, user.send, source, message)


async def delete_message(bot, message, source="unspecified"):
    """
    Deletes a single provided message from its channel.
    """
    await exception_wrapper.catch_with_pm(bot, message.delete, source)
