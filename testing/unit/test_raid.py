import json
import os
import unittest
from datetime import datetime, timedelta

from spellchecker import SpellChecker

import common_instances
from sneaselcommands.raids.raid import _validate_report, valid_time_hhmm, _find_pokemon_and_gym, \
    filter_pokemon_leftovers_from_gym, _remove_found_pokemon_from_report
from utils.pokemon_collection import _parse_jsons_as_pokedex

common_instances.POKEDEX = _parse_jsons_as_pokedex(
    pokedex_json=json.load(open(os.path.dirname(os.path.abspath(__file__)) + "/test_pokedex.json")),
    extras_json={"response": []})

common_instances.SPELLCHECKER = SpellChecker(distance=2)
common_instances.SPELLCHECKER.word_frequency.remove_words(common_instances.SPELLCHECKER.word_frequency.words())
common_instances.SPELLCHECKER.word_frequency.load_words(common_instances.POKEDEX.pokedict.keys())


class TestRaid(unittest.TestCase):

    def test_valid_time(self):
        """Testing valid time formatting"""
        self.assertTrue(valid_time_hhmm("18:15"))
        self.assertTrue(valid_time_hhmm("00:00"))
        self.assertTrue(valid_time_hhmm("18.15"))
        self.assertTrue(valid_time_hhmm("1815"))

    def test_invalid_time(self):
        """Testing invalid time formatting"""
        self.assertFalse(valid_time_hhmm("18:15:23"))
        self.assertFalse(valid_time_hhmm("01"))
        self.assertFalse(valid_time_hhmm("24:01"))

    def test_valid_report(self):
        """Testing valid report formatting"""
        self.assertEqual(
            first="",
            second=_validate_report(None, "Sneasel", "Momos", "Home", '{:%H:%M}'.format(datetime.now() + timedelta(minutes=2)))
        )

    def test_invalid_hatch_time_too_early(self):
        """Testing valid report formatting"""
        self.assertEqual(
            first=f"A raid that hatched at **{'{:%H:%M}'.format(datetime.now() - timedelta(hours=2))}** should have already despawned by now",
            second=_validate_report(None, "Sneasel", "Momos", "Home", '{:%H:%M}'.format(datetime.now() - timedelta(hours=2)))
        )

    def test_invalid_report_missing_args(self):
        """Testing invalid report formatting, missing time"""
        self.assertEqual(
            first="Missing information, please provide name and gym. Type *?help raid* for help",
            second=_validate_report("Sneasel")
        )

    def test_pokemon_extraction_single_word(self):
        """Testing that a basic search of Charizard can be found in the Pokédex"""
        self.assertEqual(
            first=("CHARIZARD", "Bleke"),
            second=_find_pokemon_and_gym("Charizard", "Bleke"))

    def test_pokemon_extraction_single_word_lowercase(self):
        """Testing that a lowercase search of Blastoise can be found in the Pokédex"""
        self.assertEqual(
            first=("BLASTOISE", "Bleke"),
            second=_find_pokemon_and_gym("blastoise", "bleke"))

    def test_pokemon_extraction_single_word_uppercase(self):
        """Testing that a uppercase search of Venusaur can be found in the Pokédex"""
        self.assertEqual(
            first=("VENUSAUR", "Bleke"),
            second=_find_pokemon_and_gym("VENUSAUR", "BLEKE"))

    def test_pokemon_extraction_gym_with_multiple_words(self):
        """Testing that a multi-word gym is returned correctly"""
        self.assertEqual(
            first=("CHARIZARD", "Adam Och Eva"),
            second=_find_pokemon_and_gym("charizard", "adam", "och", "eva"))

    def test_pokemon_extraction_pokemon_with_multiple_words(self):
        """Testing that a multi-word pokemon is returned correctly"""
        self.assertEqual(
            first=("CHARIZARD MEGA X", "Bleke"),
            second=_find_pokemon_and_gym("mega", "charizard", "x", "Bleke"))

    def test_pokemon_extraction_shorter_mega(self):
        """Testing that a mega venusaur is returned correctly"""
        self.assertEqual(
            first=("VENUSAUR MEGA", "Adam Och Eva"),
            second=_find_pokemon_and_gym("mega", "venusaur", "adam", "och", "eva"))

    def test_pokemon_extraction_mega_charizard(self):
        """Testing that a mega charizard is returned correctly"""
        self.assertEqual(
            first=("MEGA", "Charizard Adam Och Eva"),
            second=_find_pokemon_and_gym("mega", "charizard", "adam", "och", "eva"))

    def test_pokemon_extraction_mega_egg(self):
        """Testing that just the word mega means an unhatched mega egg"""
        self.assertEqual(
            first=("MEGA", "Adam Och Eva"),
            second=_find_pokemon_and_gym("mega", "adam", "och", "eva"))

    def test_pokemon_extraction_yanmega(self):
        """Testing that a yanmega is not broken because of megas"""
        self.assertEqual(
            first=("YANMEGA", "Adam Och Eva"),
            second=_find_pokemon_and_gym("yanmega", "adam", "och", "eva"))

    def test_pokemon_extraction_filter_form(self):
        """Testing filter for form"""
        self.assertEqual(
            first=("DEOXYS DEFENSE", "Adam Och Eva"),
            second=_find_pokemon_and_gym("deoxys", "defense", "form", "adam", "och", "eva"))

    def test_pokemon_extraction_galarian(self):
        """Testing galarian raids"""
        self.assertEqual(
            first=("DARMANITAN GALARIAN ZEN", "Adam Och Eva"),
            second=_find_pokemon_and_gym("galarian", "darmanitan", "zen", "adam", "och", "eva"))

    def test_pokemon_extraction_shortest_if_no_exact_match(self):
        """Testing darmanitan raids"""
        self.assertEqual(
            first=("DARMANITAN ZEN", "Adam Och Eva"),
            second=_find_pokemon_and_gym("darmanitan", "adam", "och", "eva"))

    def test_pokemon_extraction_no_match(self):
        """Testing no match"""
        self.assertEqual(
            first=("THISISNOPOKEMON", "Adam Och Eva"),
            second=_find_pokemon_and_gym("thisisnopokemon", "adam", "och", "eva"))

    def test_pokemon_extraction_egg_variants(self):
        """Testing no match"""
        self.assertEqual(
            first=("T5", "Adam Och Eva"),
            second=_find_pokemon_and_gym("t5", "adam", "och", "eva"))

    def test_pokemon_incorrect_spelling(self):
        """Basic test for a Pokémon with incorrect spelling"""
        self.assertEqual(
            first=("CHARIZARD", "Adam Och Eva"),
            second=_find_pokemon_and_gym("charirzard", "adam", "och", "eva"))

    def test_pokemon_scrambled_order(self):
        """Test for a scrambled Pokémon"""
        self.assertEqual(
            first=("CHARIZARD MEGA X", "Adam Och Eva"),
            second=_find_pokemon_and_gym("mega", "charizard", "x", "adam", "och", "eva"))

    def test_pokemon_scrambled_order_and_incorrect_spelling(self):
        """Test for a scrambled and incorrectly spelled Pokémon"""
        self.assertEqual(
            first=("CHARIZARD MEGA X", "Adam Och Eva"),
            second=_find_pokemon_and_gym("mega", "charirzard", "x", "adam", "och", "eva"))

    def test_prioritize_egg_hatch(self):
        """Tests that egg types are priorites"""
        self.assertEqual(
            first=("T5", "Ankaret Från 1777"),
            second=_find_pokemon_and_gym("t5", "ankaret", "från", "1777"))

    def test_prioritize_egg_hatch_simple(self):
        """Tests that egg types are priorites"""
        self.assertEqual(
            first=("MEGA", "Mewtwo"),
            second=_find_pokemon_and_gym("mega", "mewtwo"))

    def test_prioritize_egg_hatch_spellcheck_1(self):
        """Tests that egg types are priorites"""
        self.assertEqual(
            first=("T3", "Charzirard"),
            second=_find_pokemon_and_gym("t3", "charzirard"))

    def test_prioritize_egg_hatch_spellcheck_2(self):
        """Tests that egg types are priorites"""
        self.assertEqual(
            first=("CHARRRRZIRARD", "Från"),
            second=_find_pokemon_and_gym("charrrrzirard", "från"))

    def test_filter_pokemon_leftovers_from_gym(self):
        """Testing filters for gym"""
        self.assertEqual(
            first=(["adam", "och", "eva"]),
            second=filter_pokemon_leftovers_from_gym(["form", "adam", "och", "eva"]))

    def test_extract_gym_from_report(self):
        """Testing extraction for gym"""
        self.assertEqual(
            first="Adam Och Eva",
            second=_remove_found_pokemon_from_report(["mega", "charizard", "x", "adam", "och", "eva"], "mega charizard x"))

    def test_extract_gym_from_report_gym_and_pokemon_same_name(self):
        """Testing extraction for gym where pokemon and gym same name"""
        self.assertEqual(
            first="Sneasel",
            second=_remove_found_pokemon_from_report(["sneasel", "sneasel"], "sneasel"))


if __name__ == '__main__':
    unittest.main()
