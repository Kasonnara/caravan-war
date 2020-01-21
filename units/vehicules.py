from typing import List

from cards import Rarity
from units.base_units import MovableUnit, register_unit_type, BaseUnitType
from target_types import TargetType


class Vehicule(MovableUnit):
    move_speed = 1.2
    weapon_slot = 1


@register_unit_type('Vehicules')
class Charrette(Vehicule):
    hp_base = 2280
    # _u_hp = {5: 3987}
    shooted_as = TargetType.GROUND
    armor = 3
    cost = 8
    rarity = Rarity.Common


@register_unit_type('Vehicules')
class Chariot(Vehicule):
    hp_base = 1710
    # _u_hp = {1: 1710, 2: 1967, 3: 2262, 4: 2601, 5: 2991}
    shooted_as = TargetType.GROUND
    armor = 3
    cost = 8
    move_speed = 1.8
    rarity = Rarity.Rare


@register_unit_type('Vehicules')
class Dirigeable(Vehicule):
    hp_base = 3705
    # _u_hp = {5: 6480}
    shooted_as = TargetType.AIR
    armor = 3
    cost = 6
    effect_range = 7
    rarity = Rarity.Legendary


@register_unit_type('Vehicules')
class Train(Vehicule):
    hp_base = 4251
    # _u_hp = {1: 4251, 2: 4889, 3: 5622, 4: 6465, 5: 7435, 6: 8550}
    shooted_as = TargetType.GROUND
    armor = 8
    cost = 10
    weapon_slot = 2
    rarity = Rarity.Legendary

    @classmethod
    def hp_ratio(cls, attackers: List[BaseUnitType], defenser_level: int = 1):
        # Multiply hp_ratio by 2 (maybe by 3) because the train reflect 50% of the damage taken
        return super().hp_ratio(attackers, defenser_level=defenser_level) * 2.5


@register_unit_type('Vehicules')
class Helicopter(Vehicule):
    hp_base = 2444
    # _u_hp = {1: 2444, 2: 2811, 3: 3233, 4: 3718, 5: 4276, 6: 4917}
    shooted_as = TargetType.AIR
    armor = 0
    cost = 6
    rarity = Rarity.Epic


@register_unit_type('Vehicules')
class Wagon(Vehicule):
    hp_base = 3250
    # _u_hp = {1: 3250}
    shooted_as = TargetType.GROUND
    armor = 5
    cost = 8  # TODO check cost
    rarity = Rarity.Epic



