import json
import os
from typing import Dict

import requests

from sneasel_types import pokemon, pokedex


def _filter_form_for_pokemondb(name: str):
    """Filters shadow forms and converts other forms, handles edge-cases such as DEOXYS NORMAL"""
    if any(key_words in name for key_words in ["SHADOW", "PURIFIED", "20"]):
        name = None
    elif any(key_words == name for key_words in ["BASCULIN", "KELDEO"]):
        name = None
    elif name == "DEOXYS":
        name = "DEOXYS NORMAL"
    elif name == "MEWTWO_A_FORM":
        name = "MEWTWO ARMORED"
    elif name == "CHERRIM_SUNNY_FORM":
        name = "CHERRIM SUNSHINE"
    elif name == "DARMANITAN":
        name = "DARMANITAN STANDARD"
    elif name == "BURMY":
        name = "BURMY PLANT"
    elif "_MALE" in name:
        name = name.replace("_MALE", " M")
    elif "_FEMALE" in name:
        name = name.replace("_FEMALE", " F")
    elif "_SEA_FORM" in name:
        name = name.replace("_SEA_FORM", "")
    elif "_ALOLA_FORM" in name:
        name = name.replace("_ALOLA_FORM", " ALOLAN")

    if name is not None and "_FORM" in name:
        name = name.replace("_FORM", "")
    return None if name is None else name.replace("_", " ")


def _filter_for_p337(name: str):
    if "ALOLAN" in name:
        name = "ALOLAN " + name.replace(" ALOLAN", "")
    elif "GALARIAN" in name:
        return "GALARIAN " + name.replace(" GALARIAN", "")
    for pkmn in ["CHERRIM", "CASTFORM", "SHELLOS", "GASTRODON", "BASCULIN"]:
        if pkmn in name:
            name = pkmn
    return name


def _parse_jsons_as_pokedex(pokedex_json: dict, extras_json: dict) -> pokedex.Pokedex:
    """Returns a dictionary with [str, pokemon]"""
    pokedex_dict: Dict[str, pokemon.Pokemon] = {}
    extras_dict: Dict[str, str] = {}

    for pkmn in extras_json["response"]:
        name = pkmn.get("name")
        extras_dict[name] = pkmn

    for pkmn in pokedex_json["pokemon"]:
        pkmn_name = _filter_form_for_pokemondb(pkmn.get("pokemonId"))
        if pkmn_name is not None:
            pkmn["pokemonId"] = _filter_form_for_pokemondb(pkmn["pokemonId"])
            pokedex_dict[pkmn_name] = pokemon.Pokemon(pokemon_dict=pkmn, extras_dict=extras_dict.get(_filter_for_p337(pkmn_name)))

    return pokedex.Pokedex(pokedex_dict)


def _populate_extras_json(extras_file_path, extras_url, update=False):
    """Fetch currently released shinies from p337"""
    if update or not os.path.isfile(extras_file_path) or os.path.getsize(extras_file_path) == 0:
        shinies = str(requests.get(extras_url).content)
        pokemon_list = shinies.rsplit('var pokemon = ', 1)[1].rsplit(";\\n\\t\\tvar current_sort", 1)[0]
        decoded_list = pokemon_list.replace("\\n", "").replace("\\xc2\\xa0", " ").replace("\\xc3\\x89", "e")

        with open(extras_file_path, 'w', encoding='utf-8') as file:
            json.dump(eval(decoded_list), file, ensure_ascii=False, indent=4)

    return json.load(open(extras_file_path))


def _populate_pokedex_json(pokedex_file_path, pokedex_url, update=False) -> json:
    """
    Populates the cached Pokédex.
    If [update] is True or if the locally stored Pokédex is empty this method will REST lookup the Pokédex and store it locally.
    If [update] is False and there is a previously locally stored Pokédex we read from that.
    """
    if update or not os.path.isfile(pokedex_file_path) or os.path.getsize(pokedex_file_path) == 0:
        json_data = requests.get(pokedex_url)
        with open(pokedex_file_path, 'w', encoding='utf-8') as file:
            json.dump(json_data.json(), file, ensure_ascii=False, indent=4)

    return json.load(open(pokedex_file_path))


def create_pokedex_from_file_or_rest(pokedex_file_path, pokedex_url, extras_file_path, extras_url) -> pokedex.Pokedex:
    """Creates the Pokédex from file if it's populated, otherwise it populates the file by REST requesting and parses"""
    raw_pokedex_json = _populate_pokedex_json(pokedex_file_path=pokedex_file_path, pokedex_url=pokedex_url)
    raw_extras_json = _populate_extras_json(extras_file_path, extras_url)
    return _parse_jsons_as_pokedex(pokedex_json=raw_pokedex_json, extras_json=raw_extras_json)


def update_pokedex(pokedex_file_path, pokedex_url, extras_file_path, extras_url) -> pokedex.Pokedex:
    """Updates the current locally stored Pokédex by REST requesting a new one and parsing"""
    raw_pokedex_json = _populate_pokedex_json(pokedex_file_path=pokedex_file_path, pokedex_url=pokedex_url, update=True)
    raw_extras_json = _populate_extras_json(extras_file_path, extras_url, update=True)
    return _parse_jsons_as_pokedex(pokedex_json=raw_pokedex_json, extras_json=raw_extras_json)
