from typing import Dict, Optional

from sneasel_types.pokemon import Pokemon


class Pokedex:
    def __init__(self, pokedict: Dict[str, Pokemon]):
        self.pokedict = pokedict

    def lookup(self, pokemon_name: str) -> Optional[Pokemon]:
        return self.pokedict.get(pokemon_name.upper())
