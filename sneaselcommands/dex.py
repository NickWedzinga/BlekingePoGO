import discord
from discord.ext import commands

from utils import pokemon_collection
from utils.exception_wrapper import pm_dev_error


def _find_possible_matches(name: str, list_of_names: list):
    possible_list = []
    for pkmn_name in list_of_names:
        if name in pkmn_name:
            possible_list.append(pkmn_name)
    return possible_list


def _create_info_message(name: str, possible_matches: list):
    info_message = ""
    if possible_matches:
        if len(possible_matches) > 10:
            info_message += f"\t:question: Too many Pokémon containing: **{name}**\n"
        else:
            info_message += f"\t:grey_question: Pokémon found containing **{name}**: *{', '.join(possible_matches)}*\n"
    else:
        info_message += f"\t:question: Could not find any Pokémon containing: **{name}**\n"
    return info_message


class Dex(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot):
        self.pokedex_file_path = "textfiles/pokedex.json"
        self.pokedex_url = "https://fight.pokebattler.com/pokemon"
        self.shiny_file_path = "textfiles/shiny.json"
        self.shiny_url = "https://p337.info/pokemongo/pokedex/?show=shiny&hide=unreleased"
        self.dex = pokemon_collection.create_pokedex_from_file_or_rest(
            pokedex_file_path=self.pokedex_file_path, pokedex_url=self.pokedex_url,
            extras_file_path=self.shiny_file_path, extras_url=self.shiny_url
        )
        self.bot = bot

    @commands.command(name="dex")
    async def dex(self, ctx, *pokemon_name):
        """
        Used to look a Pokémon up in the Pokédex, type ?dex <pokemon>

        Usage: ?dex sneasel
        """
        if not pokemon_name:
            await ctx.send("No Pokémon provided, usage is *?dex POKEMON_NAME*")
            return

        pokemon_name_list = [name.replace(",", "") for name in pokemon_name]
        pokemon_name_concat = " ".join(map(str, pokemon_name_list))
        pkmn = self.dex.lookup(pokemon_name_concat.upper())

        if pkmn is None:
            info_message = f"Could not find **{pokemon_name_concat.capitalize()}** in Pokédex, similar results:\n"

            for sub_name in pokemon_name_list:
                possible_matches = _find_possible_matches(sub_name.upper(), self.dex.pokedict.keys())
                info_message += _create_info_message(name=sub_name.capitalize(), possible_matches=possible_matches)
            await ctx.send(info_message)
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
        self.dex = pokemon_collection.update_pokedex(
            pokedex_file_path=self.pokedex_file_path,
            pokedex_url=self.pokedex_url,
            extras_file_path=self.shiny_file_path,
            extras_url=self.shiny_url
        )
        await ctx.send(f"Updated Pokédex!")

    @update_pokedex.error
    async def update_pokedex_on_error(self, _, error):
        """Catches errors with update_pokedex command"""

        await pm_dev_error(bot=self.bot, error_message=error, source="update_pokedex")


def setup(bot):
    bot.add_cog(Dex(bot))
