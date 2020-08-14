import datetime

import discord
from discord.utils import get

from sneasel_types import moves, stats, extras


class Pokemon:
    # TODO send more interesting stuff through constructor
    def __init__(self, pokemon_dict: dict, extras_dict):
        self.pokemon_dict = pokemon_dict
        self.extras_dict = extras_dict

        self.name = None
        self.number = None
        self.type1 = None
        self.type2 = None
        self.extras: extras.Extras = extras.Extras()
        self.stats: stats.Stats = stats.Stats()
        self.movepool: moves.Moves = moves.Moves()

        # updates the Pokemon´s values
        self.__parse_dict_as_pokemon()

    def __parse_dict_as_pokemon(self):
        self.name = self.pokemon_dict.get("pokemonId")
        self.number = self.pokemon_dict.get("pokedex").get("pokemonNum")
        self.type1 = self.pokemon_dict.get("type").replace("POKEMON_TYPE_", "")
        self.type2 = None if self.pokemon_dict.get("type2") is None else self.pokemon_dict.get("type2").replace("POKEMON_TYPE_", "")
        self.extras = extras.Extras(self.extras_dict)
        self.stats = stats.Stats(self.pokemon_dict.get("stats"))
        self.movepool = moves.Moves(fast_moves=self.pokemon_dict.get("quickMoves"), charge_moves=self.pokemon_dict.get("cinematicMoves"))

    async def send_embed(self, ctx):
        pokebattler_url_name = self.name.replace(" ", "_") + "_FORM" if " " in self.name else self.name
        pokemondb_url_name = self.name.replace(" ", "-")

        pokebattler_url = f"https://www.pokebattler.com/pokemon/names/{pokebattler_url_name.upper()}/levels/40/opponents/levels/40/strategies/DODGE_SPECIALS/DEFENSE_RANDOM_MC?sort=OVERALL&weatherCondition=NO_WEATHER&view=GROUPED&dodgeStrategy=DODGE_REACTION_TIME"
        pokemondb_sprite_url = f"https://img.pokemondb.net/sprites/go/normal/{pokemondb_url_name.lower()}.png"

        level_15 = self.stats.calculate_cp_at_level(level=15)
        level_20 = self.stats.calculate_cp_at_level(level=20)
        level_25 = self.stats.calculate_cp_at_level(level=25)
        level_40 = self.stats.calculate_cp_at_level(level=40)

        emoji_type1 = get(ctx.message.guild.emojis, name=f"{self.type1.lower()}_type")
        typing_str = f"{emoji_type1} {self.type1}"

        if self.type2 is not None:
            emoji_type2 = get(ctx.message.guild.emojis, name=f"{self.type2.lower()}_type")
            type2_str = f"{emoji_type2} {self.type2}"
            typing_str = f"{typing_str}\n{type2_str}"

        embed = discord.Embed(title=f"Pokédex #{self.number} - {self.name}",
                              color=0xff9900,
                              url=f"{pokebattler_url}",
                              description=f"Released: {':grey_question:' if self.extras.release_date is None else self.extras.release_date}",
                              timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=pokemondb_sprite_url)
        embed.set_footer(text="Sprite: https://pokemondb.net/sprites • Shiny info: https://p337.info", icon_url=pokemondb_sprite_url)
        embed.add_field(name="Type: ", value=typing_str, inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="Shiny", value=(":no_entry:" if self.extras.shiny_date is None else f":white_check_mark: {self.extras.shiny_date}"), inline=True)
        embed.add_field(name="Max CP:", value=f"Research: **{level_15}**, Raid/Egg: **{level_20}**, \nRaid (weather boost): **{level_25}**, Max:  **{level_40}**", inline=False)
        embed.add_field(name="Fast moves:", value=" ".join(self.movepool.fast_moves), inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="Charge moves:", value=" ".join(self.movepool.charge_moves), inline=True)
        await ctx.send(embed=embed)