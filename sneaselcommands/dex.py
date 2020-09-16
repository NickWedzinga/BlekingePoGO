import discord
from discord.ext import commands

import common_instances
from utils import pokemon_collection
from utils.exception_wrapper import pm_dev_error
from spellchecker import SpellChecker


def _find_possible_matches(name: str, list_of_names: list) -> list:
    possible_list = []
    for pkmn_name in list_of_names:
        if name in pkmn_name:
            possible_list.append(pkmn_name)
    return possible_list


def _find_containing_matches(ctx, pokemon_name: str) -> list:
    """Takes a name and checks for each word in name if a Pokémon contains that word"""
    possible_matches = []
    for sub_name in pokemon_name.split(" "):
        sub_matches = _find_possible_matches(sub_name.upper(), common_instances.POKEDEX.pokedict.keys())
        if len(sub_matches) < 10:
            [possible_matches.append(sub_match) for sub_match in sub_matches if sub_match not in possible_matches]
    return possible_matches


def create_info_message(ctx, pokemon_name: str):
    pokemon_spelling_candidates = common_instances.SPELLCHECKER.candidates(pokemon_name)
    pokemon_containing_matches = _find_containing_matches(ctx=ctx, pokemon_name=pokemon_name)

    info_message = f"Could not find any matches for {pokemon_name} {ctx.author.mention}"

    if len(pokemon_spelling_candidates) > 1 or (pokemon_spelling_candidates and pokemon_name not in pokemon_spelling_candidates):
        info_message += f"\nSimilarly spelled alternatives: {', '.join(list(map(str.title, pokemon_spelling_candidates)))}"
    if pokemon_containing_matches:
        info_message += f"\nPokémon containing parts of {pokemon_name}: {', '.join(list(map(str.title, pokemon_containing_matches)))}"
    return info_message


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
            # TODO: implement the subset lookup that raid has

            pkmn_spell_checked = common_instances.POKEDEX.lookup(common_instances.SPELLCHECKER.correction(pokemon_name_concat))
            if pkmn_spell_checked is not None:
                await pkmn_spell_checked.send_embed(ctx)
                info_message = f"Showing result for **{pkmn_spell_checked.name.title()}**, did not find **{pokemon_name_concat.title()}**"

                candidates = common_instances.SPELLCHECKER.candidates(pokemon_name_concat)
                if len(candidates) > 1:
                    info_message += f"\nOther options: {', '.join(list(map(str.title, candidates)))}"
                await ctx.send(info_message)
            else:
                await ctx.send(create_info_message(ctx, pokemon_name_concat))
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
