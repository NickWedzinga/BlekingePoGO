from typing import Optional

import common
import common_instances
from sneasel_types.pokemon import Pokemon


def check_scrumbled_pokemon_name(scrumbled_pokemon_name: list) -> Optional[Pokemon]:
    """
    Attempts to scramble the Pokémon name around and find any existing Pokémon that match.
    Will return the Pokémon if found, otherwise it will return None
    """
    scrumbled_pokemon_name = list(map(str.upper, scrumbled_pokemon_name))
    pokemon = None
    proper_matches = []
    backup_matches = []

    # Check scrumbled names
    for key in common_instances.POKEDEX.pokedict.keys():
        set_key = set(key.split(" "))
        if set_key.issubset(set(scrumbled_pokemon_name)):
            proper_matches.append(key)

        # if no good match can be found, checks if first word in pokemon equals a word in multiple word pokemon name
        # will match things like DARMANITAN  -> DARMANITAN ZEN and DEOXYS -> DEOXYS NORMAL
        if any(scrumbled_pokemon_name[0].upper() == word for word in key.split(" ")):
            backup_matches.append(key)

    # If scrumbling found some Pokémon matches, return longest match
    if proper_matches:
        pokemon = common_instances.POKEDEX.lookup(max(proper_matches, key=len))
    elif backup_matches and scrumbled_pokemon_name[0] not in common.RAID_EGG_TYPES:
        pokemon = common_instances.POKEDEX.lookup(min(backup_matches, key=len))

    return pokemon


def check_spelling_pokemon_name(pokemon_misspelled: str) -> Optional[Pokemon]:
    """
    Attempts to solve the incorrect spelling and look up the corrected Pokémon.

    Returns the Pokémon if found, otherwise it will return None
    """
    if pokemon_misspelled.upper() in common.RAID_EGG_TYPES:
        return None
    pokemon_spell_checked = common_instances.SPELLCHECKER.correction(pokemon_misspelled)
    return common_instances.POKEDEX.lookup(pokemon_spell_checked)


def check_scrumbled_and_spelling_pokemon(incorrect_pokemon_list: list) -> Optional[Pokemon]:
    """
    Checks spelling for each word in Pokémon name and tries to correct it.
    This is expensive and should be last resort.

    Will then also check if the name is scrambled and attempt to correct that.

    Returns the Pokémon if found, otherwise it will return None
    """
    maybe_correctly_spelled_pokemon: list = []
    for pokemon_sub_name in incorrect_pokemon_list:
        if pokemon_sub_name.upper() not in common.RAID_EGG_TYPES:
            maybe_correctly_spelled_pokemon.append(common_instances.SPELLCHECKER.correction(pokemon_sub_name))
        else:
            maybe_correctly_spelled_pokemon.append(pokemon_sub_name)

    return check_scrumbled_pokemon_name(maybe_correctly_spelled_pokemon)
