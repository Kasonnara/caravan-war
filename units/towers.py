#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    This is a personal project to understand and improve my knowledge/tactics in the game Caravan War.
    Copyright (C) 2019  Kasonnara <kasonnara@laposte.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from typing import Union, List, Optional

from utils.class_property import classproperty
from common.target_types import TargetType
from units.base_units import BaseUnit, AOE, Heal
from common.cards import register_card_type


class Tower(BaseUnit):
    parent_tower = None
    _cost = None

    @classproperty
    def cost(cls):
        # FIXME: possible infinite recursive loop
        if cls._cost is None:
            return None
        if cls.parent_tower is None:
            return cls._cost
        else:
            assert issubclass(cls.parent_tower, Tower), "Parent ({}) is not a Tower".format(cls.parent_tower)
            return cls._cost + cls.parent_tower.cost

    @classproperty
    def gem_cost(cls):
        return cls.rarity.spell_gem_cost

    @classmethod
    def gold_cost(cls, ligue: 'Ligue'):
        return cls.rarity.spell_gold_cost(ligue)


@register_card_type('Towers')
class Sentinelle(Tower):
    attack_base = 72
    hit_frequency = 1.6
    range = 9
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = 150
    parent_tower = None


@register_card_type('Towers')
class Arbalete(Tower):
    attack_base = 100
    hit_frequency = 1.6
    range = 11
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = 160
    parent_tower = Sentinelle
    multiple_target_limit = 2


@register_card_type('Towers')
class Eolance(Tower):
    attack_base = 535
    hit_frequency = 0.6
    range = 11
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = None
    parent_tower = Arbalete


@register_card_type('Towers')
class Sniper(Tower):
    attack_base = 330
    hit_frequency = 0.5
    range = 13
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = None
    parent_tower = Sentinelle


@register_card_type('Towers')
class HeavySniper(Tower):
    attack_base = 200
    hit_frequency = 1.5
    range = 13
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = None
    parent_tower = Sniper
    # TODO special effect
    _upgrade_cost = [570, 3200, 14500, 33000, 71000, 163000, 345000, 485000, 710000, 1030000, 1920000, 3360000]
    # damage, with 4 stars [240, 276, 318, 366, 421, 483, 555, 638, 734, 844, 972, 1117]


@register_card_type('Towers')
class Mage(Tower):
    attack_base = 85
    hit_frequency = 1.2
    range = 8
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 6
    _cost = 150
    parent_tower = None


@register_card_type('Towers')
class Lightning(Tower):
    attack_base = 137
    hit_frequency = 0.8
    range = 8
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 6
    _cost = 175
    parent_tower = Mage
    multiple_target_limit = 8

    def damage_formule(self, target: 'MovableUnit', target_index=0):
        return (
            super().damage_formule(target, target_index=target_index)
            * (0.25 * max(0, 4 - target_index))  # Reduction factor
            )


@register_card_type('Towers')
class Stormspire(Tower, AOE):
    attack_base = 0
    hit_frequency = 0.25
    range = 3.5
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 6
    _cost = 200
    parent_tower = Lightning
    # TODO special effects
    _upgrade_cost = [240, 1300, 6000, 14000, 30000, 68000, 144000, 202000, 300000, 430000, 800000]


@register_card_type('Towers')
class Fire(Tower):
    attack_base = 130
    hit_frequency = 2
    range = 8
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 2
    _cost = 160
    parent_tower = Mage


@register_card_type('Towers')
class Bomber(AOE, Tower):
    attack_base = 88
    hit_frequency = 0.4
    range = 10
    shoot_to = TargetType.GROUND
    armor_piercing = 0
    _cost = 170
    parent_tower = None


@register_card_type('Towers')
class Canon(Tower):
    attack_base = 184
    hit_frequency = 0.5
    range = 10
    shoot_to = TargetType.GROUND
    armor_piercing = 0
    _cost = 120
    parent_tower = Bomber
    multiple_target_limit = 3


@register_card_type('Towers')
class Hydra(Tower):
    attack_base = 200
    hit_frequency = 1
    range = 150
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = 280
    parent_tower = Canon


@register_card_type('Towers')
class MissileLaucher(AOE, Tower):
    attack_base = 240
    hit_frequency = 0.8
    range = 12
    shoot_to = TargetType.AIR
    armor_piercing = 0
    _cost = 80
    parent_tower = Bomber


@register_card_type('Towers')
class Hospital(AOE, Heal, Tower):
    base_heal = 20
    heal_frequency = 1
    range = None
    shoot_to = TargetType.AIR_GROUND
    _cost = 120
    parent_tower = None

    def dps(self, targets: Union['MovableUnit', List['MovableUnit']]) -> Optional[float]:
        return None


@register_card_type('Towers')
class Armory(Hospital):
    _cost = 80
    parent_tower = Hospital


@register_card_type('Towers')
class Tambour(Hospital):
    _cost = 130
    parent_tower = Hospital


@register_card_type('Towers')
class Garnison(Tambour, Armory):
    _cost = 190
    parent_tower = Armory


if __name__ == '__main__':
    print("Heavy sniper upgrade cost ratio =",
          [c2 / c1 for c1, c2 in zip(HeavySniper._upgrade_cost[:-1], HeavySniper._upgrade_cost[1:])])
    print("Heavy Sniper upgrade cost total ratio =",
          [c / HeavySniper._upgrade_cost[0] for c in HeavySniper._upgrade_cost])

    print("Stormspire upgrade cost ratio =",
          [c2 / c1 for c1, c2 in zip(Stormspire._upgrade_cost[:-1], Stormspire._upgrade_cost[1:])])
    print("Stormspire upgrade cost total ratio =", [c / Stormspire._upgrade_cost[0] for c in Stormspire._upgrade_cost])

