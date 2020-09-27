from typing import Optional

import discord
from discord.ext import commands
from spellchecker import SpellChecker

import common_instances
from sneasel_types.pokemon import Pokemon
from utils import pokemon_collection
from utils.exception_wrapper import pm_dev_error
from utils.pokemon_corrector import check_scrumbled_pokemon_name, check_scrumbled_and_spelling_pokemon, \
    check_spelling_pokemon_name


def _find_possible_matches(name: str, list_of_names: list) -> list:
    possible_list = []
    for pkmn_name in list_of_names:
        if name in pkmn_name:
            possible_list.append(pkmn_name)
    return possible_list


def _find_containing_matches(pokemon_name: str) -> list:
    """Takes a name and checks for each word in name if a Pokémon contains that word"""
    possible_matches = []
    for sub_name in pokemon_name.split(" "):
        sub_matches = _find_possible_matches(sub_name.upper(), common_instances.POKEDEX.pokedict.keys())
        if len(sub_matches) < 10:
            [possible_matches.append(sub_match) for sub_match in sub_matches if sub_match not in possible_matches]
    return possible_matches


def create_no_matches_info_message(ctx, pokemon_name: str):
    pokemon_spelling_candidates = common_instances.SPELLCHECKER.candidates(pokemon_name)
    pokemon_containing_matches = _find_containing_matches(pokemon_name=pokemon_name)

    info_message = f"Could not find any matches for {pokemon_name} {ctx.author.mention}"

    if len(pokemon_spelling_candidates) > 1 or (pokemon_spelling_candidates and pokemon_name not in pokemon_spelling_candidates):
        info_message += f"\nSimilarly spelled alternatives: {', '.join(list(map(str.title, pokemon_spelling_candidates)))}"
    if pokemon_containing_matches:
        info_message += f"\nPokémon containing parts of {pokemon_name}: {', '.join(list(map(str.title, pokemon_containing_matches)))}"
    return info_message


def create_found_correction_info_message(ctx, corrected_name: str, incorrect_name: str) -> str:
    """Creates a str that lists the corrected Pokémon and attempts to give spelling alternatives"""
    info_message = f"Showing result for **{corrected_name.title()}**, did not find **{incorrect_name.title()}** {ctx.author.mention}"

    candidates = common_instances.SPELLCHECKER.candidates(incorrect_name)
    if len(candidates) > 1:
        info_message += f"\nOther spelling options: {', '.join(list(map(str.title, candidates)))}"
    return info_message


async def find_corrected_pokemon(ctx, pokemon_name: list) -> Optional[Pokemon]:
    """Attempts to scamble and spell-check to find the correct Pokémon"""
    pkmn_scrambled_checked = check_scrumbled_pokemon_name(list(pokemon_name))
    if pkmn_scrambled_checked is not None:
        return pkmn_scrambled_checked

    pkmn_spell_checked = check_spelling_pokemon_name(" ".join(pokemon_name))
    if pkmn_spell_checked is not None:
        return pkmn_spell_checked

    await ctx.send("This may take some time..")
    pkmn_spell_and_scrambled_checked = check_scrumbled_and_spelling_pokemon(pokemon_name)
    if pkmn_spell_and_scrambled_checked:
        return pkmn_spell_and_scrambled_checked
    return None


class Dex(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot
        common_instances.POKEDEX = pokemon_collection.create_pokedex_from_file_or_rest(
            pokedex_file_path=common_instances.POKEDEX_FILE_PATH, pokedex_url=common_instances.POKEDEX_URL,
            extras_file_path=common_instances.SHINY_FILE_PATH, extras_url=common_instances.SHINY_URL
        )
        common_instances.SPELLCHECKER = SpellChecker(distance=2)
        common_instances.SPELLCHECKER.word_frequency.remove_words(common_instances.SPELLCHECKER.word_frequency.words())
        common_instances.SPELLCHECKER.word_frequency.load_words(common_instances.POKEDEX.pokedict.keys())

    @commands.command(name="dex")
    async def dex(self, ctx, *pokemon_name):
        """
        Used to look a Pokémon up in the Pokédex, type ?dex <pokemon>

        Usage: ?dex sneasel
        """
        if not pokemon_name:
            await ctx.send("No Pokémon provided, usage is *?dex POKEMON_NAME*")
            return

        pokemon_name_concat = " ".join(pokemon_name)
        pkmn = common_instances.POKEDEX.lookup(pokemon_name_concat)

        if pkmn is None:
            maybe_found_pokemon = await find_corrected_pokemon(ctx, list(pokemon_name))
            if maybe_found_pokemon is not None:
                await ctx.send(create_found_correction_info_message(ctx, maybe_found_pokemon.name, " ".join(pokemon_name)))
                await maybe_found_pokemon.send_embed(ctx)
            else:
                await ctx.send(create_no_matches_info_message(ctx, " ".join(pokemon_name)))
        else:
            await pkmn.send_embed(ctx)

    @dex.error
    async def dex_on_error(self, _, error):
        """Catches errors with dex command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="dex")

    @commands.command(name="update_pokedex", hidden=True)
    @commands.is_owner()
    async def update_pokedex(self, ctx):
        """Updates the Pokédex"""
        common_instances.POKEDEX = pokemon_collection.update_pokedex(
            pokedex_file_path=common_instances.POKEDEX_FILE_PATH,
            pokedex_url=common_instances.POKEDEX_URL,
            extras_file_path=common_instances.SHINY_FILE_PATH,
            extras_url=common_instances.SHINY_URL
        )
        await ctx.send(f"Updated Pokédex!")

    @update_pokedex.error
    async def update_pokedex_on_error(self, _, error):
        """Catches errors with update_pokedex command"""

        await pm_dev_error(bot=self.bot, error_message=error, source="update_pokedex")


def setup(bot):
    bot.add_cog(Dex(bot))
