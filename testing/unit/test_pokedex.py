import unittest

from sneasel_types import pokedex
from utils import pokemon_collection


class TestPokedex(unittest.TestCase):
    def test__pokedex_init(self):
        """Tests init"""
        test_pokedex = pokemon_collection._parse_jsons_as_pokedex(_pokemon_json(), _extras_json())
        self.assertIsInstance(test_pokedex, pokedex.Pokedex)

    def test__pokedex_lookup_regular(self):
        """Tests lookup function"""
        test_pokedex = pokemon_collection._parse_jsons_as_pokedex(_pokemon_json(), _extras_json())
        test_pokemon = test_pokedex.lookup("SNEASEL")

        self.assertEqual(test_pokemon.name, "SNEASEL")
        self.assertEqual(test_pokemon.number, 215)
        self.assertEqual(test_pokemon.type1, "DARK")
        self.assertEqual(test_pokemon.type2, "ICE")
        self.assertEqual(test_pokemon.extras.release_date, "16-Feb-2017")
        self.assertEqual(test_pokemon.extras.shiny_date, "25-Jul-2019")
        self.assertEqual(test_pokemon.stats.base_attack, 189)
        self.assertEqual(test_pokemon.stats.base_defense, 146)
        self.assertEqual(test_pokemon.stats.base_stamina, 146)
        self.assertEqual(test_pokemon.movepool.fast_moves, ["ICE SHARD\n", "FEINT ATTACK\n"])
        self.assertEqual(test_pokemon.movepool.charge_moves, ["ICE PUNCH\n", "AVALANCHE\n", "FOUL PLAY\n"])

    def test__pokedex_lookup(self):
        """Tests lookup function"""
        test_pokedex = pokemon_collection._parse_jsons_as_pokedex(_pokemon_json(), _extras_json())
        test_pokemon = test_pokedex.lookup("SNEASEL")

        self.assertEqual(test_pokemon.name, "SNEASEL")
        self.assertEqual(test_pokemon.number, 215)
        self.assertEqual(test_pokemon.type1, "DARK")
        self.assertEqual(test_pokemon.type2, "ICE")
        self.assertEqual(test_pokemon.extras.release_date, "16-Feb-2017")
        self.assertEqual(test_pokemon.extras.shiny_date, "25-Jul-2019")
        self.assertEqual(test_pokemon.stats.base_attack, 189)
        self.assertEqual(test_pokemon.stats.base_defense, 146)
        self.assertEqual(test_pokemon.stats.base_stamina, 146)
        self.assertEqual(test_pokemon.movepool.fast_moves, ["ICE SHARD\n", "FEINT ATTACK\n"])
        self.assertEqual(test_pokemon.movepool.charge_moves, ["ICE PUNCH\n", "AVALANCHE\n", "FOUL PLAY\n"])


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
