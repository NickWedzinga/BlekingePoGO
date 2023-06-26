import re
from datetime import datetime, timedelta

import discord
import requests
from discord.ext import commands

from common import instances, constants, tables
from sneaselcommands.raids.utils.raid_scheduler import schedule_edit_embed, schedule_reminding_task, \
    schedule_delete_channel_at, update_raids_channel
from sneaselcommands.raids.utils.raid_stats import insert_into_stats
from utils.database_connector import execute_statement, create_insert_query, create_select_query
from utils.exception_wrapper import pm_dev_error
from utils.global_error_manager import in_channel_list
from utils.pokemon_corrector import check_scrumbled_pokemon_name, check_spelling_pokemon_name, \
    check_scrumbled_and_spelling_pokemon
from utils.time_wrapper import valid_time_hhmm, valid_time_mm, format_as_hhmm


def _remove_illegal_characters(args: list) -> list:
    """Removes illegal varchar characters in preparation for database"""
    illegal_characters = "['#%]"
    return [re.sub(illegal_characters, "", word) for word in args]


def _validate_report(args: list) -> str:
    """Validates the format of the report."""
    if len(args) < 2:
        return f"Missing information, please provide name and gym. Type *?help raid* for help"

    hatch_time = valid_time_hhmm(args[-1])
    earliest_possible_hatch_time = (datetime.now() - timedelta(minutes=45))
    if hatch_time is not None and hatch_time.time() < earliest_possible_hatch_time.time():
        return f"A raid that hatched at **{args[-1]}** should have already despawned by now"

    latest_possible_hatch_time = (datetime.now() + timedelta(hours=1))
    if hatch_time is not None and hatch_time.time() > latest_possible_hatch_time.time():
        return f"A raid that hatches at **{args[-1]}** can not have spawned yet"

    despawn_time = valid_time_mm(args[-1])
    if despawn_time is not None and (despawn_time.minute <= 0 or despawn_time.minute > 45):
        return f"Incorrect despawn time of **{despawn_time.minute}** minutes, should be between 1 and 45 minutes"
    return ""


def maybe_replace_time(*report) -> list:
    """Replaces the time """
    report = list(report)

    maybe_valid_time_hhmm = valid_time_hhmm(report[-1])
    maybe_valid_time_mm = valid_time_mm(report[-1])
    if maybe_valid_time_hhmm is not None:
        report[-1] = format_as_hhmm(maybe_valid_time_hhmm)
    elif maybe_valid_time_mm is not None:
        report[-1] = format_as_hhmm(datetime.now() - timedelta(minutes=45-maybe_valid_time_mm.minute))
    return report


async def _send_embed(bot, ctx, channel, pokemon_name: str, gym: str, hatch_time: str):
    """Creates the embed to be posted in the new raid channel"""
    embed = create_raid_embed(ctx, ctx.author.mention, pokemon_name, gym, hatch_time)
    await channel.send(embed=embed)

    maybe_valid_time = valid_time_hhmm(hatch_time)
    if maybe_valid_time is not None:
        if maybe_valid_time.time() > datetime.now().time():
            schedule_edit_embed(bot, ctx=ctx, channel=channel, at_time=format_as_hhmm(maybe_valid_time))
    return embed


def create_raid_embed(ctx, reporter, pokemon_name: str, gym_name: str, hatch_time: str) -> discord.Embed:
    maybe_valid_time = valid_time_hhmm(hatch_time)
    if maybe_valid_time is None or maybe_valid_time.time() > datetime.now().time():
        description = f"Reporter: {reporter}\nGym: {gym_name.capitalize()}\nHatch time: {hatch_time}"
    else:
        description = f"Reporter: {reporter}\nGym: {gym_name.capitalize()}\nDespawn time: {format_as_hhmm((maybe_valid_time + timedelta(minutes=45)))}"

    pokemon = instances.POKEDEX.lookup(pokemon_name)
    pokemon_icon = "https://www.pokencyclopedia.info/sprites/misc/spr_substitute/art__substitute.png"
    fast_moves = "N/A"
    charge_moves = "N/A"
    max_cp_20 = "N/A"
    max_cp_25 = "N/A"
    max_cp_40 = "N/A"
    types = "N/A"

    if pokemon_name.upper() in constants.RAID_EGG_TYPES:
        pokemon_name = pokemon_name.upper()
        pokemon_icon = constants.RAID_EGG_ICON_URLS[pokemon_name]
    elif pokemon is not None:
        pokemon_name = pokemon_name.title()
        if requests.get(pokemon.sprite_url).status_code == 200:
            pokemon_icon = pokemon.sprite_url
        fast_moves = " ".join(pokemon.movepool.fast_moves)
        charge_moves = " ".join(pokemon.movepool.charge_moves)
        max_cp_20 = pokemon.stats.calculate_cp_at_level(20)
        max_cp_25 = pokemon.stats.calculate_cp_at_level(25)
        max_cp_40 = pokemon.stats.calculate_cp_at_level(40)

        types = discord.utils.get(ctx.message.guild.emojis, name=f"{pokemon.type1.lower()}_type")
        if pokemon.type2 is not None:
            types = f"{types} {discord.utils.get(ctx.message.guild.emojis, name=f'{pokemon.type2.lower()}_type')}"

    embed = discord.Embed(title=f"Raid - {pokemon_name}",
                          color=0xff9900,
                          description=description,
                          timestamp=datetime.utcnow())
    embed.set_thumbnail(url=pokemon_icon)
    embed.set_footer(text="Sprite: https://pokemondb.net/sprites • Data: https://www.pokebattler.com")
    embed.add_field(name="Type: ", value=types, inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(name="Max CP:",
                    value=f"Raid: **{max_cp_20}**, Raid (weather boost): **{max_cp_25}**, Max: **{max_cp_40}**",
                    inline=False)
    embed.add_field(name="Fast moves:", value=fast_moves, inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(name="Charge moves:", value=charge_moves, inline=True)
    return embed


def filter_pokemon_leftovers_from_gym(report: list) -> list:
    """Removes pokemon leftovers such as 'form' from the gym name"""
    filter_list = ["form"]
    return [word for word in report if word.lower() not in filter_list]


def _remove_found_pokemon_from_report(report: list, pokemon: str) -> str:
    """Attempts to remove the pokemon"""
    report = filter_pokemon_leftovers_from_gym(report)
    pokemon_list = pokemon.upper().split(" ")
    report_list = list(map(str.upper, report))

    [report_list.remove(word) for word in pokemon_list if word in report_list]
    return " ".join(report_list).title()


def _find_originally_misspelled_pokemon(report: list, corrected_pokemon_name: str) -> str:
    """Finds the originally misspelled Pokémon from the report and the corrected pokemon name"""
    original_pokemon_list = []
    for word in report:
        if word.upper() in corrected_pokemon_name.upper():
            original_pokemon_list.append(word)
        elif instances.SPELLCHECKER.correction(word).upper() in corrected_pokemon_name.upper():
            original_pokemon_list.append(word)
    return " ".join(original_pokemon_list)


def _find_pokemon_and_gym(report: list) -> (str, str):
    """Attempts to find the pokemon and gym in a printreport"""
    if valid_time_hhmm(report[-1]) is not None or valid_time_mm(report[-1]):
        report = report[:-1]

    original_pokemon = report[0]
    if original_pokemon.upper() in constants.RAID_EGG_TYPES and original_pokemon.upper() != "MEGA":
        pokemon = original_pokemon
    else:
        pokemon = check_scrumbled_pokemon_name(report)
        if pokemon is not None:
            pokemon = pokemon.name.upper()
            original_pokemon = pokemon

    # Checking len is less than 3 assures that the Pokémon only contains one word
    if pokemon is None and len(report) < 3:
        maybe_spelled_correctly_pokemon = check_spelling_pokemon_name(original_pokemon)
        if maybe_spelled_correctly_pokemon is not None:
            pokemon = maybe_spelled_correctly_pokemon.name

    # check if both the order is wrong and Pokémon is misspelled
    if pokemon is None:
        maybe_correct_spelling_and_scramble_pokemon = check_scrumbled_and_spelling_pokemon(report)
        if maybe_correct_spelling_and_scramble_pokemon is not None:
            pokemon = maybe_correct_spelling_and_scramble_pokemon.name
            original_pokemon = _find_originally_misspelled_pokemon(report, pokemon)

    # Works both for if first word is an egg type or if Pokémon just can't be found
    if pokemon is None:
        pokemon = report[0]
        original_pokemon = pokemon

    return pokemon.upper(), _remove_found_pokemon_from_report(list(map(str.upper, report)), original_pokemon)


def _find_channel_index_by_hatch_time(hatch_time: datetime):
    """Finds the position the channel should be created in by comparing hatch_times"""
    active_raids = execute_statement(create_select_query(table_name=tables.ACTIVE_RAID_CHANNEL_OWNERS)).all(as_dict=True)
    hatch_times = [hatch_time]
    for raid in active_raids:
        hatch_times.append(valid_time_hhmm(raid.get("hatch_time")))
    return sorted(hatch_times).index(hatch_time)


async def _find_raid_category(bot, ctx) -> discord.CategoryChannel:
    """Finds the related raid-category for the reported raid"""
    maybe_category = discord.utils.get(ctx.guild.categories, name=f"{ctx.channel.category.name} raids")

    if maybe_category is None:
        await pm_dev_error(bot=bot,
                           error_message=f"Somehow can't find category: [{ctx.channel.category.name} raids]",
                           source="Create raid channel, finding category")
    return maybe_category if maybe_category is not None else ctx.channel.category


async def _create_channel_and_information(bot, ctx, report: list):
    at_time_or_train = report[-1]
    pokemon, gym = _find_pokemon_and_gym(report)

    if not gym:
        await ctx.send(f"Your raid is missing either a pokemon or gym name {ctx.author.mention}, use *?help raid* for details")
        return

    maybe_valid_hatch_time = valid_time_hhmm(at_time_or_train)
    maybe_valid_despawn_time = valid_time_mm(at_time_or_train)

    category = await _find_raid_category(bot, ctx)

    # TODO: position argument doesn't set channel at that position, temp commented until fixed
    if maybe_valid_despawn_time is not None:
        created_channel = await ctx.guild.create_text_channel(
            name=f"{format_as_hhmm(datetime.now() - timedelta(minutes=45-maybe_valid_despawn_time.minute))}_{pokemon}_{gym}",
            category=category)
            # position=_find_channel_index_by_hatch_time(datetime.now() - timedelta(minutes=45-maybe_valid_despawn_time.minute)) + 1)
    elif maybe_valid_hatch_time is not None:
        created_channel = await ctx.guild.create_text_channel(
            name=f"{at_time_or_train}_{pokemon}_{gym}",
            category=category)
            # position=_find_channel_index_by_hatch_time(maybe_valid_hatch_time) + 1)
    else:
        created_channel = await ctx.guild.create_text_channel(name=f"{pokemon}_{gym}", category=category)

    if maybe_valid_hatch_time is None and maybe_valid_despawn_time is None:
        if at_time_or_train == "train":
            hatch_time = "Train channel, discuss hatch times"
            schedule_reminding_task(bot, ctx, created_channel, f"Do not forget to *?close* this channel when you are done {ctx.author.mention}", "empty", "hourly")
        else:
            hatch_time = "Hatched!"
            schedule_reminding_task(bot, ctx, created_channel, f"This channel will close in 1 minute", format_as_hhmm(datetime.now() + timedelta(minutes=59)), "daily")
            schedule_delete_channel_at(bot, ctx, created_channel, format_as_hhmm(datetime.now() + timedelta(hours=1)))
    elif maybe_valid_hatch_time is not None:
        hatch_time = format_as_hhmm(maybe_valid_hatch_time)
        schedule_reminding_task(bot, ctx, created_channel, f"This channel will close in 1 minute", format_as_hhmm(maybe_valid_hatch_time + timedelta(minutes=59)), "daily")
        schedule_delete_channel_at(bot, ctx, created_channel, format_as_hhmm(maybe_valid_hatch_time + timedelta(hours=1)))
    else:
        calculated_hatch_time = datetime.now() - timedelta(minutes=45-maybe_valid_despawn_time.minute)
        hatch_time = format_as_hhmm(calculated_hatch_time)
        schedule_reminding_task(bot, ctx, created_channel, f"This channel will close in 1 minute", format_as_hhmm(calculated_hatch_time + timedelta(minutes=59)), "daily")
        schedule_delete_channel_at(bot, ctx, created_channel, format_as_hhmm(calculated_hatch_time + timedelta(hours=1)))

    execute_statement(create_insert_query(
        table_name=tables.ACTIVE_RAID_CHANNEL_OWNERS,
        keys="(channel_id, reporter_id, pokemon, gym, hatch_time, last_updated)",
        values=f"('{created_channel.id}', '{ctx.author.id}', '{pokemon}', '{gym}', '{hatch_time}', 'empty')"))

    insert_into_stats(ctx, ctx.author.display_name, ctx.author.id, created_channel.id, pokemon, gym, hatch_time)

    await ctx.send(f"{ctx.author.mention} has created a raid in {created_channel.mention}, why don't you join them?")
    await _send_embed(bot, ctx, created_channel, pokemon, gym, hatch_time)


class Raid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="raid")
    @in_channel_list(constants.RAID_REPORT_CHANNEL_LIST)
    async def raid(self, ctx, *args):
        """
        ?raid <pokemon/egg_type> <gym> [hatch time/minutes to despawn]

        Example (if T5 egg hatches at 18:15): ?raid T5 Klockstapeln 18:15
        Example (if a Mewtwo raid despawns in 33 minutes): ?raid Mewtwo Klockstapeln 33

        Creates a raid channel that will automatically be deleted 15 minutes after the raid despawns
        Egg types: [T1, T3, T5, MEGA]

        When you are in the raid channel..
        Type ?help update, for more information on how to update the raid
        Type ?status, to ask Sneasel to re-send the raid information
        Type ?close, to close the raid channel early
        """
        await ctx.send(f"[?raid, ?raids] commands are temporarily disabled {ctx.author.mention}")
        return

        # args = maybe_replace_time(*args)
        # validated_report = _validate_report(args)
        # legal_args = _remove_illegal_characters(args)
        # if len(validated_report) > 1:
        #     await ctx.send(f"{validated_report} {ctx.author.mention}")
        #     return
        #
        # await _create_channel_and_information(self.bot, ctx, legal_args)
        # await update_raids_channel(self.bot, ctx)

    @raid.error
    async def raid_on_error(self, _, error):
        await pm_dev_error(bot=self.bot, error_message=error, source="Raid")


async def setup(bot):
    await bot.add_cog(Raid(bot))
