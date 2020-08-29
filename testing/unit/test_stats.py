import unittest

from sneasel_types import stats


class TestStats(unittest.TestCase):
    def test__init_default(self):
        """Tests default init"""
        self.assertIsNone(stats.Stats().base_attack)
        self.assertIsNone(stats.Stats().base_defense)
        self.assertIsNone(stats.Stats().base_stamina)

    def test__extraction(self):
        """Tests init when provided with value for stats dict"""
        test_dict = {"baseAttack": 10, "baseDefense": 20, "baseStamina": 30}
        test_stats = stats.Stats(test_dict)

        self.assertEqual(test_stats.base_attack, 10)
        self.assertEqual(test_stats.base_defense, 20)
        self.assertEqual(test_stats.base_stamina, 30)

    def test__cp_calc_magikarp_level_1(self):
        """Tests the cp calc function floor at cp 10 with level 1 Magikarp"""
        test_dict_magikarp = {"baseAttack": 29, "baseDefense": 85, "baseStamina": 85}
        test_stats_magikarp = stats.Stats(test_dict_magikarp)

        self.assertEqual(test_stats_magikarp.calculate_cp_at_level(1), 10)

    def test__cp_calc_slaking_level_40(self):
        """Tests the cp calc function highest possible cp with level 40 Slaking"""
        test_dict_slaking = {"baseAttack": 290, "baseDefense": 166, "baseStamina": 284}
        test_stats_slaking = stats.Stats(test_dict_slaking)

        self.assertEqual(test_stats_slaking.calculate_cp_at_level(40), 4431)

    def test__cp_calc_low_stamina_shedinja(self):
        """Tests the cp calc function with base_stamina at 1 with Shedinja"""
        test_dict_shedinja = {"baseAttack": 153, "baseDefense": 73, "baseStamina": 1}
        test_stats_shedinja = stats.Stats(test_dict_shedinja)

        self.assertEqual(test_stats_shedinja.calculate_cp_at_level(1), 10)
        self.assertEqual(test_stats_shedinja.calculate_cp_at_level(30), 337)

    def test__cp_calc_set_ivs_azumarill(self):
        """Tests the cp calc function with set ivs with level 40 Azumarill"""
        test_dict_azumarill = {"baseAttack": 112, "baseDefense": 152, "baseStamina": 225}
        test_stats_azumarill = stats.Stats(test_dict_azumarill)

        self.assertEqual(test_stats_azumarill.calculate_cp_at_level(40, 7, 15, 13), 1481)


if __name__ == '__main__':
    unittest.main()
