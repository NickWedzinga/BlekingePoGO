from typing import Dict

from sneasel_types import pokemon


class Pokedex:
    def __init__(self, pokedict: Dict[str, pokemon.Pokemon]):
        self.pokedict = pokedict

    def lookup(self, pokemon_name: str):
        return self.pokedict.get(pokemon_name.upper())
