from utils import exception_wrapper


async def message_channel(bot, channel, message: str, source="unspecified", error_message: str = None):
    """
    Sends a single message in a channel.
    """
    await exception_wrapper.catch_with_pm(bot=bot, function_to_try=await channel.send(message), source=source,
                                          error_message=error_message)


# TODO: untested
async def message_user(bot, user, message: str):
    """
    Sends a single message to a user.
    """
    await exception_wrapper.catch_with_pm(bot=bot, function_to_try=await user.send(message))


async def delete_message(bot, message, source="unspecified", error_message: str = None):
    """
    Deletes a single provided message from its channel.
    """
    await exception_wrapper.catch_with_pm(bot=bot, function_to_try=await message.delete(), source=source,
                                          error_message=error_message)
