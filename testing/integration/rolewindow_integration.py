import logging

from common import constants, instances


async def call_rolewindow_test(bot, ctx):
    try:
        await basic_rolewindow_test(bot, ctx)
        await constants.TEST_RESULTS_CHANNEL.send(f":white_check_mark: Rolewindow[Not unique]: Command invocation without error.")
    except Exception as e:
        logging.exception(e)
        await constants.TEST_RESULTS_CHANNEL.send(f":no_entry: Error during rolewindow integration-tests: {e}")
        raise ValueError(f"Error during rolewindow integration-tests")


async def basic_rolewindow_test(bot, ctx):
    rolewindow_command = bot.get_command("rolewindow")
    remove_command = bot.get_command("remove_rolewindow")

    await ctx.invoke(rolewindow_command, "Test", constants.TEST_RESULTS_CHANNEL.id, "false", "karlskrona", "karlskrona")

    embed_message = None
    async for message in constants.TEST_RESULTS_CHANNEL.history(limit=3):
        if message.embeds:
            embed_message = message
            assert(len(message.reactions) == 1)
            assert(message.reactions[0].emoji.name == "karlskrona")
    assert(len(instances.ROLEWINDOWS) == 1)
    assert(instances.ROLEWINDOWS.get(embed_message.id).emoji_to_role_dict.get("karlskrona") == "karlskrona")

    await ctx.invoke(remove_command, constants.TEST_RESULTS_CHANNEL.id, embed_message.id)
    async for message in constants.TEST_RESULTS_CHANNEL.history(limit=3):
        if message.embeds and message.id == embed_message.id:
            raise ValueError("Found the embed despite running remove_rolewindow")
    assert(len(instances.ROLEWINDOWS) == 0)


async def run_tests(bot, ctx):
    await call_rolewindow_test(bot, ctx)
