from typing import Dict

from sneasel_types import pokemon


class Pokedex:
    def __init__(self, pokedict: Dict[str, pokemon.Pokemon]):
        self.pokedict = pokedict

    # TODO: test some strange cases like Mega form, deoxys defense, sunny castform, cherrim overcast, rotom wash, flabebe, armored mewtwo, nidoran male, empty
    def lookup(self, pokemon_name: str):
        return self.pokedict.get(pokemon_name)
