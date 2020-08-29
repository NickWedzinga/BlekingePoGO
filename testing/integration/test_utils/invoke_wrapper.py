import common


# TODO: remove source, just use command for source
async def invoke_event_now(bot, ctx, command: str, source: str, *args):
    cmd = bot.get_command(command)
    await ctx.invoke(cmd, *args)
    await common.TEST_RESULTS_CHANNEL.send(f":white_check_mark: {source.capitalize()}: Successfully invoked the {command} command.")
