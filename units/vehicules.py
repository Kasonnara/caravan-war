from typing import List

from cards import Rarity
from units.base_units import MovableUnit, register_unit_type, BaseUnitType
from target_types import TargetType
from units.equipments import Armor


class Vehicule(MovableUnit):
    move_speed = 1.2
    weapon_slot = 1


@register_unit_type('Vehicules')
class Charrette(Vehicule):
    hp_base = 2280
    shooted_as = TargetType.GROUND
    armor = 3
    cost = 8
    rarity = Rarity.Common


@register_unit_type('Vehicules')
class Chariot(Vehicule):
    hp_base = 1710
    shooted_as = TargetType.GROUND
    armor = 3
    cost = 8
    move_speed = 1.8
    rarity = Rarity.Rare


@register_unit_type('Vehicules')
class Dirigeable(Vehicule):
    hp_base = 3705
    shooted_as = TargetType.AIR
    armor = 3
    cost = 6
    effect_range = 7
    rarity = Rarity.Legendary


@register_unit_type('Vehicules')
class Train(Vehicule):
    hp_base = 4251
    shooted_as = TargetType.GROUND
    armor = 8
    cost = 10
    weapon_slot = 2
    rarity = Rarity.Legendary

    @classmethod
    def hp_ratio(cls, *args, **kwargs):
        # Multiply hp_ratio by 2 (maybe by 3) because the train reflect 50% of the damage taken
        return super().hp_ratio(*args, **kwargs) * 2.5


@register_unit_type('Vehicules')
class Helicopter(Vehicule):
    hp_base = 2444
    shooted_as = TargetType.AIR
    armor = 0
    cost = 6
    rarity = Rarity.Epic


@register_unit_type('Vehicules')
class Wagon(Vehicule):
    hp_base = 3250
    shooted_as = TargetType.GROUND
    armor = 5
    cost = 8  # TODO check cost
    rarity = Rarity.Epic


@register_unit_type('Vehicules')
class Buggy(Vehicule):
    hp_base = 3000
    move_speed = 1.8
    armor = 4
    rarity = Rarity.Epic
    cost = 6
    # TODO spell
