import unittest

from sneasel_types import extras


class TestExtra(unittest.TestCase):
    def test__init_default(self):
        """Tests default init"""
        self.assertIsNone(extras.Extras().extras_dict)
        self.assertIsNone(extras.Extras().release_date)
        self.assertIsNone(extras.Extras().shiny_date)

    def test__extraction(self):
        """Tests init and __set_dates function by providing value for extras dict"""
        test_extras = extras.Extras(_extras_json())

        self.assertEqual(test_extras.release_date, "16-Feb-2017")
        self.assertEqual(test_extras.shiny_date, "25-Jul-2019")


def _extras_json():
    return {
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


if __name__ == '__main__':
    unittest.main()
