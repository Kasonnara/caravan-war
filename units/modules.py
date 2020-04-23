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
from typing import Union, Type

from buildings.buildings import Weaponsmith
from common.card_categories import MODULES
from common.rarity import Rarity
from common.resources import resourcepackets_gold
from units.base_units import AOE, COE, BaseUnit, reincarnation
from common.target_types import TargetType


class ModuleWeapon(BaseUnit):
    base_building = Weaponsmith
    cost = 1

    def __init__(self, level: int, stars=0):
        super().__init__(level, stars, None)


class Balista(ModuleWeapon):
    attack_base = 53
    hit_frequency = 2
    range = 7
    armor_piercing = 0
    shoot_to = TargetType.AIR_GROUND
    rarity = Rarity.Common
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,  # 1 -> 6
        -32000,
        )


class Mortar(AOE, ModuleWeapon):
    attack_base = 115
    hit_frequency = 0.4
    range = 8
    armor_piercing = 0
    shoot_to = TargetType.GROUND
    rarity = Rarity.Rare
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,  # 1 -> 6
        None, None, None, -280000,
        )


class Shotgun(COE, ModuleWeapon):
    attack_base = 77
    hit_frequency = 0.8
    range = 6
    armor_piercing = 0
    shoot_to = TargetType.AIR
    rarity = Rarity.Rare
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,  # 1 -> 6
        None, -122000,
        )


class Chaingun(ModuleWeapon):
    attack_base = 125
    hit_frequency = 2
    range = 7
    armor_piercing = 3
    shoot_to = TargetType.AIR_GROUND
    rarity = Rarity.Epic
    anti_air_bonus = 1.5
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,  # 1 -> 6
        None, None, None, -430000, None,  # 6 -> 11
        None, None, -4420000, -7570000, -13150000,
        )

    def damage_formule(self, target: 'MovableUnit', target_index=0):
        dmg = super().damage_formule(target, target_index=target_index)
        if dmg is None:
            return None
        return dmg * (1 if target.shooted_as is TargetType.GROUND else self.anti_air_bonus)  # Damage boost against air unit


@reincarnation
class ChaingunLeg(Chaingun):
    multiple_target_limit = 2
    # FIXME the 2nd target must be at less than 1m
    anti_air_bonus = 1.6

    def damage_formule(self, target: 'MovableUnit', target_index=0):
        dmg = super().damage_formule(target, target_index=target_index)
        if dmg is None:
            return None
        return dmg * (1. if target_index == 0 else 0.5)  # Damage reduced on the second target


class Laser(ModuleWeapon):
    attack_base = 86
    hit_frequency = 2
    range = 7
    armor_piercing = 6
    shoot_to = TargetType.AIR_GROUND
    consecutive_hit_attack_boost = 0.4
    max_consecutive_boost = 3.
    rarity = Rarity.Epic
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,  # 1 -> 6
        None, None, None, None, -740000,  # 6 -> 11
        )


@reincarnation
class LaserLeg(Laser):
    consecutive_hit_attack_boost = 0.5
    # TODO: slowdown effect


class FlameTrower(COE, ModuleWeapon):
    attack_base = 43
    hit_frequency = 2
    range = 4
    armor_piercing = 0
    shoot_to = TargetType.AIR_GROUND
    rarity = Rarity.Epic
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,  # 1 -> 6
        None, None, None, None, -790000,  # 6 -> 11
        None, None, -4560000, -7810000, -13570000,
        )


@reincarnation
class FlameTrowerLeg(FlameTrower):
    pass


class Tesla(COE, ModuleWeapon):
    attack_base = 144
    hit_frequency = 1
    range = 7
    armor_piercing = 0
    shoot_to = TargetType.AIR_GROUND
    multiple_target_limit = 4
    rarity = Rarity.Legendary
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,  # 1 -> 6
        None, None, None, None, -990000,  # 6 -> 11
        )

    def damage_formule(self, target: 'MovableUnit', target_index=0):
        dmg = super().damage_formule(target, target_index=target_index)
        if dmg is None:
            return None
        return (
            dmg
            #* (0.25 * max(0, 4 - target_index)  # FIXME: Do lightning damage reduction apply to tesla?
            * (1.7 if target.is_summoned else 1)  # Damage boost against summoned targets
            )


class Barrier(ModuleWeapon):
    attack_base = 300
    hit_frequency = 1
    range = 7
    armor_piercing = 0
    shoot_to = TargetType.AIR_GROUND
    # Todo protective effect
    rarity = Rarity.Legendary
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,  # 1 -> 6
        None, None, None, None, None,  # 6 -> 11
        None, None, -5280000, -9040000, -15700000,
        )


class Harpon(ModuleWeapon):
    attack_base = 639
    hit_frequency = .7
    range = 7
    armor_piercing = 7
    shoot_to = TargetType.AIR_GROUND
    # Todo slow effect
    rarity = Rarity.Legendary
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,               # 1 -> 6
        None, None, None, None, None,               # 6 -> 11
        None, None, -5420000, -9280000, -16120000,  # 11 -> 16
        )


# Register all defined cards
MODULES.register_cards_in_module(ModuleWeapon, __name__)
