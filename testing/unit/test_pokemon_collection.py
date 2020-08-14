import unittest

from sneasel_types import pokedex
from utils import pokemon_collection


class TestPokemonCollection(unittest.TestCase):
    def test__pokedex_json_parsing(self):
        """Tests init"""
        test_pokedex = pokemon_collection._parse_jsons_as_pokedex(_pokemon_json(), _extras_json())
        self.assertIsInstance(test_pokedex, pokedex.Pokedex)

    # region pokemondb filtering
    def test__pokemondb_filter_shadow(self):
        """Tests shadow forms are filtered"""
        self.assertIsNone(pokemon_collection._filter_form_for_pokemondb("TEST_SHADOW_FORM"))

    def test__pokemondb_filter_purified(self):
        """Tests purified forms are filtered"""
        self.assertIsNone(pokemon_collection._filter_form_for_pokemondb("TEST_PURIFIED_FORM"))

    def test__pokemondb_filter_costumes(self):
        """Tests costumes are filtered"""
        self.assertIsNone(pokemon_collection._filter_form_for_pokemondb("PIKACHU_COSTUME_2020_FORM"))

    def test__pokemondb_filter_deoxys(self):
        """Tests all deoxys forms"""
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("DEOXYS"), "DEOXYS NORMAL")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("DEOXYS_DEFENSE_FORM"), "DEOXYS DEFENSE")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("DEOXYS_ATTACK_FORM"), "DEOXYS ATTACK")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("DEOXYS_SPEED_FORM"), "DEOXYS SPEED")

    def test__pokemondb_filter_mewtwo_armored(self):
        """Tests mewtwo_a_form is changed to mewtwo armored"""
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("MEWTWO"), "MEWTWO")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("MEWTWO_A_FORM"), "MEWTWO ARMORED")

    def test__pokemondb_filter_genders(self):
        """Tests nidoran/frillish/jellicent genders suffix with m or f"""
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("NIDORAN_MALE"), "NIDORAN M")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("NIDORAN_FEMALE"), "NIDORAN F")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("FRILLISH"), "FRILLISH")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("FRILLISH_FEMALE_FORM"), "FRILLISH F")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("FRILLISH_MALE_FORM"), "FRILLISH M")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("JELLICENT"), "JELLICENT")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("JELLICENT_FEMALE_FORM"), "JELLICENT F")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("JELLICENT_MALE_FORM"), "JELLICENT M")

    def test__pokemondb_filter_darmanitan(self):
        """Tests darmanitan standard and zen modes"""
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("DARMANITAN_STANDARD"), "DARMANITAN STANDARD")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("DARMANITAN_ZEN"), "DARMANITAN ZEN")

    def test__pokemondb_filter_cherrim(self):
        """Tests cherrim overcast and sunshine forms"""
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("CHERRIM"), "CHERRIM")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("CHERRIM_OVERCAST_FORM"), "CHERRIM OVERCAST")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("CHERRIM_SUNNY_FORM"), "CHERRIM SUNSHINE")

    def test__pokemondb_filter_castform(self):
        """Tests cherrim overcast and sunshine forms"""
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("CASTFORM"), "CASTFORM")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("CASTFORM_SUNNY_FORM"), "CASTFORM SUNNY")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("CASTFORM_RAINY_FORM"), "CASTFORM RAINY")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("CASTFORM_SNOWY_FORM"), "CASTFORM SNOWY")

    def test__pokemondb_filter_burmy(self):
        """Tests burmy plant, trash and sandy forms"""
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("BURMY"), "BURMY PLANT")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("BURMY_TRASH_FORM"), "BURMY TRASH")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("BURMY_SANDY_FORM"), "BURMY SANDY")

    def test__pokemondb_filter_wormadam(self):
        """Tests wormadam plant, trash and sandy forms"""
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("WORMADAM"), "WORMADAM")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("WORMADAM_PLANT_FORM"), "WORMADAM PLANT")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("WORMADAM_TRASH_FORM"), "WORMADAM TRASH")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("WORMADAM_SANDY_FORM"), "WORMADAM SANDY")

    def test__pokemondb_filter_sea_forms(self):
        """Tests shellos and gastrodon west sea and east sea forms"""
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("SHELLOS"), "SHELLOS")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("SHELLOS_WEST_SEA_FORM"), "SHELLOS WEST")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("SHELLOS_EAST_SEA_FORM"), "SHELLOS EAST")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("GASTRODON"), "GASTRODON")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("GASTRODON_WEST_SEA_FORM"), "GASTRODON WEST")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("GASTRODON_EAST_SEA_FORM"), "GASTRODON EAST")

    def test__pokemondb_filter_alola(self):
        """Tests alolan forms"""
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("MEOWTH_ALOLA_FORM"), "MEOWTH ALOLAN")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("PERSIAN_ALOLA_FORM"), "PERSIAN ALOLAN")

    def test__pokemondb_filter_galarian(self):
        """Tests galarian forms"""
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("DARMANITAN_STANDARD_GALARIAN_FORM"), "DARMANITAN STANDARD GALARIAN")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("DARMANITAN_ZEN_GALARIAN_FORM"), "DARMANITAN ZEN GALARIAN")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("STUNFISK_GALARIAN_FORM"), "STUNFISK GALARIAN")

    def test__pokemondb_filter_gen8(self):
        """Tests new gen8 Pokémon"""
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("PERRSERKER"), "PERRSERKER")
        self.assertEqual(pokemon_collection._filter_form_for_pokemondb("OBSTAGOON"), "OBSTAGOON")
    # endregion

    # region pokemondb filtering
    def test__p337_filter_castform(self):
        """Tests all castform forms defaulting to castform"""
        self.assertEqual(pokemon_collection._filter_for_p337("CASTFORM"), "CASTFORM")
        self.assertEqual(pokemon_collection._filter_for_p337("CASTFORM SUNNY"), "CASTFORM")
        self.assertEqual(pokemon_collection._filter_for_p337("CASTFORM RAINY"), "CASTFORM")
        self.assertEqual(pokemon_collection._filter_for_p337("CASTFORM SNOWY"), "CASTFORM")

    def test__p337_filter_cherrim(self):
        """Tests all cherrim forms defaulting to cherrim"""
        self.assertEqual(pokemon_collection._filter_for_p337("CHERRIM"), "CHERRIM")
        self.assertEqual(pokemon_collection._filter_for_p337("CHERRIM OVERCAST"), "CHERRIM")
        self.assertEqual(pokemon_collection._filter_for_p337("CHERRIM SUNNY"), "CHERRIM")

    def test__p337_filter_shellos(self):
        """Tests all shellos forms defaulting to shellos"""
        self.assertEqual(pokemon_collection._filter_for_p337("SHELLOS"), "SHELLOS")
        self.assertEqual(pokemon_collection._filter_for_p337("SHELLOS WEST"), "SHELLOS")
        self.assertEqual(pokemon_collection._filter_for_p337("SHELLOS EAST"), "SHELLOS")

    def test__p337_filter_gastrodon(self):
        """Tests all gastrodon forms defaulting to gastrodon"""
        self.assertEqual(pokemon_collection._filter_for_p337("GASTRODON"), "GASTRODON")
        self.assertEqual(pokemon_collection._filter_for_p337("GASTRODON WEST"), "GASTRODON")
        self.assertEqual(pokemon_collection._filter_for_p337("GASTRODON EAST"), "GASTRODON")

    def test__p337_filter_basculin(self):
        """Tests all basculin forms defaulting to basculin"""
        self.assertEqual(pokemon_collection._filter_for_p337("BASCULIN"), "BASCULIN")
        self.assertEqual(pokemon_collection._filter_for_p337("BASCULIN RED STRIPED"), "BASCULIN")
        self.assertEqual(pokemon_collection._filter_for_p337("BASCULIN BLUE STRIPED"), "BASCULIN")

    def test__p337_filter_alolan(self):
        """Tests all alolan forms"""
        self.assertEqual(pokemon_collection._filter_for_p337("MEOWTH ALOLAN"), "ALOLAN MEOWTH")

    def test__p337_filter_galarian(self):
        """Tests all galarian forms"""
        self.assertEqual(pokemon_collection._filter_for_p337("MEOWTH GALARIAN"), "GALARIAN MEOWTH")
    # endregion


def _pokemon_json():
    return {
        "pokemon": [
            {
                "pokemonId": "SNEASEL",
                "type": "POKEMON_TYPE_DARK",
                "type2": "POKEMON_TYPE_ICE",
                "stats": {
                    "baseStamina": 146,
                    "baseAttack": 189,
                    "baseDefense": 146
                },
                "quickMoves": [
                    "ICE_SHARD_FAST",
                    "FEINT_ATTACK_FAST"
                ],
                "cinematicMoves": [
                    "ICE_PUNCH",
                    "AVALANCHE",
                    "FOUL_PLAY"
                ],
                "pokedexHeightM": 0.89,
                "pokedexWeightKg": 28.0,
                "heightStdDev": 0.11125,
                "weightStdDev": 3.5,
                "familyId": "FAMILY_SNEASEL",
                "thirdMove": {
                    "stardustToUnlock": 50000,
                    "candyToUnlock": 50
                },
                "movesets": [
                    {
                        "quickMove": "ICE_SHARD_FAST",
                        "cinematicMove": "ICE_PUNCH"
                    },
                    {
                        "quickMove": "ICE_SHARD_FAST",
                        "cinematicMove": "AVALANCHE"
                    },
                    {
                        "quickMove": "ICE_SHARD_FAST",
                        "cinematicMove": "FOUL_PLAY"
                    },
                    {
                        "quickMove": "FEINT_ATTACK_FAST",
                        "cinematicMove": "ICE_PUNCH"
                    },
                    {
                        "quickMove": "FEINT_ATTACK_FAST",
                        "cinematicMove": "AVALANCHE"
                    },
                    {
                        "quickMove": "FEINT_ATTACK_FAST",
                        "cinematicMove": "FOUL_PLAY"
                    }
                ],
                "pokedex": {
                    "pokemonId": "SNEASEL",
                    "pokemonNum": 215,
                    "gen": "GEN_2"
                },
                "tmMovesets": [
                    {
                        "quickMove": "ICE_SHARD_FAST",
                        "cinematicMove": "ICE_PUNCH"
                    },
                    {
                        "quickMove": "ICE_SHARD_FAST",
                        "cinematicMove": "AVALANCHE"
                    },
                    {
                        "quickMove": "ICE_SHARD_FAST",
                        "cinematicMove": "FOUL_PLAY"
                    },
                    {
                        "quickMove": "FEINT_ATTACK_FAST",
                        "cinematicMove": "ICE_PUNCH"
                    },
                    {
                        "quickMove": "FEINT_ATTACK_FAST",
                        "cinematicMove": "AVALANCHE"
                    },
                    {
                        "quickMove": "FEINT_ATTACK_FAST",
                        "cinematicMove": "FOUL_PLAY"
                    }
                ],
                "currentMovesets": [
                    {
                        "quickMove": "ICE_SHARD_FAST",
                        "cinematicMove": "ICE_PUNCH"
                    },
                    {
                        "quickMove": "ICE_SHARD_FAST",
                        "cinematicMove": "AVALANCHE"
                    },
                    {
                        "quickMove": "ICE_SHARD_FAST",
                        "cinematicMove": "FOUL_PLAY"
                    },
                    {
                        "quickMove": "FEINT_ATTACK_FAST",
                        "cinematicMove": "ICE_PUNCH"
                    },
                    {
                        "quickMove": "FEINT_ATTACK_FAST",
                        "cinematicMove": "AVALANCHE"
                    },
                    {
                        "quickMove": "FEINT_ATTACK_FAST",
                        "cinematicMove": "FOUL_PLAY"
                    }
                ]
            }
        ]
    }


def _extras_json():
    return {
        "response": [
            {
                "name": "SNEASEL",
                "row": "215",
                "id": "215",
                "fam": "1101215215",
                "img": "215",
                "POS": "64",
                "Gen": "2",
                "Typ1": "dark",
                "Typ2": "ice",
                "W1": "Fog",
                "W2": "Snow",
                "CP1": "2051",
                "CP2": "2022",
                "A": "189",
                "D": "146",
                "S": "146",
                "TOT": "481",
                "N": "1",
                "ALO": "0",
                "SPA": "1",
                "CRO": "1",
                "FUT": "1",
                "SHI": "1",
                "SHT": "20:41",
                "SHD": "25-Jul-19",
                "SHTS": "43671",
                "SHN": "1",
                "SHE": "Team Rocket Release",
                "REG": "0",
                "RAI": "0",
                "NEW": "0",
                "EGG": "5",
                "TEM": "0",
                "ERK": "1",
                "FEV": "1",
                "AQU": "010",
                "RELD": "16-Feb-17",
                "RELTS": "22:00",
                "RELTXT": "Johto Update",
                "RELID": "42782_0.917",
                "FOR": "0",
                "DIT": "0",
                "L": "0"
            }
        ]
    }


if __name__ == '__main__':
    unittest.main()
