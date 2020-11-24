from typing import Dict

from common.constants import CPM_VALUES


class Stats:
    def __init__(self, stats_dict: Dict[str, int] = {}):
        self.base_attack = stats_dict.get("baseAttack")
        self.base_defense = stats_dict.get("baseDefense")
        self.base_stamina = stats_dict.get("baseStamina")

    def __str__(self):
        return f"Base attack: {self.base_attack}, base defense: {self.base_defense}, base hp: {self.base_stamina}"

    def calculate_cp_at_level(self, level: int, iv_atk: int = 15, iv_def: int = 15, iv_hp: int = 15):
        """Calculates the cp for a given [level] using the object's base stats with the provided iv's. FLoor set at 10."""
        return max(int(((self.base_attack + iv_atk) * (self.base_defense + iv_def) ** 0.5 *
                    (self.base_stamina + iv_hp) ** 0.5 * CPM_VALUES[level] ** 2) / 10), 10)

    # TODO: tried to move around [calculate_cp_at_level] function to create this, but something is missing. This gets close, but not right
    # def calculate_level_from_cp(cp: float, base_atk: float, base_def: float, base_hp: float, iv_atk: float, iv_def: float, iv_hp: float):
    #     cpm_raised_2 = 10 * cp / ((base_atk + iv_atk) * (base_def + iv_def)**0.5 * (base_hp+iv_hp)**0.5)
    #     return CPM_VALUES.keys()[CPM_VALUES.values().index(sqrt(cpm_raised_2))]

