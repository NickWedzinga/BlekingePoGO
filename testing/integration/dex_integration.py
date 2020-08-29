import common
from testing.integration.test_utils import invoke_wrapper
from utils.exception_wrapper import catch_with_channel_message
import discord


async def call_dex_tests(bot, ctx):
    """Calls all dex commands"""
    await call_update_dex(bot, ctx)
    await call_dex_pokemon_test(bot, ctx)


async def call_update_dex(bot, ctx):
    """Calls the update dex command to REST call and update all Pokédex info"""
    await catch_with_channel_message(
        invoke_wrapper.invoke_event_now,
        common.TEST_RESULTS_CHANNEL,
        f":no_entry: Error during update_pokedex invocation",
        True,
        "integration/update pokedex",
        bot,
        ctx,
        "update_pokedex",
        "Update Pokedex"
    )


async def call_dex_pokemon_test(bot, ctx):
    """Calls the main dex command"""
    await catch_with_channel_message(
        invoke_wrapper.invoke_event_now,
        common.TEST_RESULTS_CHANNEL,
        f":no_entry: Error during dex invocation",
        True,
        "integration/dex",
        bot,
        ctx,
        "dex",
        "Dex",
        *{"Sneasel"}
    )
    last_message = (await ctx.message.channel.history(limit=1).flatten())[0]
    test_embed: discord.embeds.Embed = last_message.embeds[0]
    assert("SNEASEL" in test_embed.title)
    assert("16-Feb-2017" in test_embed.description)


async def run_tests(bot, ctx):
    await call_dex_tests(bot, ctx)
