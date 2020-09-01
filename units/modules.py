#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This is a personal project to understand and improve my knowledge/tactics in the game Caravan War.
# Copyright (C) 2019  Kasonnara <kasonnara@laposte.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from buildings.buildings import Weaponsmith
from common.alignment import Alignment
from common.card_categories import MODULES
from common.rarity import Rarity
from common.resources import resourcepackets_gold
from lang.languages import TranslatableString
from units.base_units import AOE, COE, BaseUnit, reincarnation, MovableUnit
from common.target_types import TargetType
from units.towers import Tower


class ModuleWeapon(BaseUnit):
    base_building = Weaponsmith
    cost = 1
    alignment = Alignment.DEFENDER

    def __init__(self, level: int, stars=0):
        super().__init__(level, stars, None)

    __display_name = TranslatableString("Addon", french="Module")


class Balista(ModuleWeapon):
    attack_base = 53
    hit_frequency = 2
    range = 7
    armor_piercing = 0
    shoot_to = TargetType.AIR_GROUND
    rarity = Rarity.Common
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -190, -900, -3500, -7000, -14000,  # 1 -> 6
        -32000, -68000, -90000, -140000, -250000,  # 6 -> 11
        -460000, -810000, -1430000, -2440000, -4240000,  # 11 -> 16
        -7530000, -13430000, -23660000, -42560000, -81580000,  # 16 -> 21
        -136020000, -231980000, -382560000, -639180000, -1080410000,  # 21 -> 26
        -1821940000, -2809350000, -3935100000, -5514320000,
        )
    __display_name = TranslatableString("Ballista", french="Baliste")


class Mortar(AOE, ModuleWeapon):
    attack_base = 115
    hit_frequency = 0.4
    range = 8
    armor_piercing = 0
    shoot_to = TargetType.GROUND
    rarity = Rarity.Rare
    aoe_radius = 1
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -370, -1900, -7100, -14000, -28000,  # 1 -> 6
        -64000, -135000, -190000, -280000, -490000,  # 6 -> 11
        -920000, -1620000, -2850000, -4880000, -8480000,  # 11 -> 16
        -15060000, -26860000, -47320000, -85120000, -163150000,  # 16 -> 21
        -272030000, -463960000, -765120000, -1278360000, -2160810000,  # 21 -> 26
        -3643890000, -5618710000, -7870210000, -11028630000,
        )
    __display_name = TranslatableString("Mortar", french="Mortier")


class Shotgun(COE, ModuleWeapon):
    attack_base = 77
    hit_frequency = 0.8
    range = 6
    armor_piercing = 0
    shoot_to = TargetType.AIR
    rarity = Rarity.Rare
    aoe_radius=0.5
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -330, -1700, -6300, -12000, -25000,  # 1 -> 6
        -57000, -122000, -170000, -250000, -450000,  # 6 -> 11
        -830000, -1450000, -2570000, -4400000, -7640000,  # 11 -> 16
        -13560000, -24170000, -42590000, -76610000, -146840000,  # 16 -> 21
        -244830000, -417570000, -688610000, -1150530000, -1944730000,  # 21 -> 26
        -3279500000, -5056840000, -7083190000, -9925770000,
        )
    __display_name = TranslatableString("Scatter Gun", french="Fusil à dispersion")


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
        -570, -2900, -10900, -21000, -43000,  # 1 -> 6
        -99000, -210000, -290000, -430000, -770000,  # 6 -> 11
        -1430000, -2500000, -4420000, -7570000, -13150000,  # 11 -> 16
        -23350000, -41630000, -73340000, -131930000, -252890000,  # 16 -> 21
        -421650000, -719140000, -1185940000, -1981460000, -3349260000,  # 21 -> 26
        -5648202000, -8709000000, -12198820000, -17094380000,
        )

    def damage_formule(self, target: MovableUnit, target_index=0, hit_combo=0):
        dmg = super().damage_formule(target, target_index=target_index)
        if dmg is None:
            return None
        return dmg * (1 if target.shooted_as is TargetType.GROUND else self.anti_air_bonus)  # Damage boost against air unit

    __display_name = TranslatableString("Machine Gun", french="Mitrailleuse")


@reincarnation
class ChaingunLeg(Chaingun):
    multiple_target_limit = 2
    # FIXME the 2nd target must be at less than 1m
    anti_air_bonus = 1.6

    def damage_formule(self, target: MovableUnit, target_index=0, hit_combo=0):
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
        -560, -2800, -10600, -21000, -42000,  # 1 -> 6
        -95000, -203000, -280000, -410000, -740000,  # 6 -> 11
        -1390000, -2420000, -4280000, -7330000, -12730000,  # 11 -> 16
        -22600000, -40290000, -70980000, -127680000, -244730000,  # 16 -> 21
        -408050000, -695940000, -1147680000, -1917540000, -3241220000,  # 21 -> 26
        -5465830000, -8428060000, -11805310000, -16542950000,
        )
    __display_name = "Laser"


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
        -590, -3000, -11300, -22000, -44000,  # 1 -> 6
        -102000, -216000, -300000, -440000, -790000,  # 6 -> 11
        -1480000, -2590000, -4560000, -7810000, -13570000,  # 11 -> 16
        -24100000, -42980000, -75710000, -136190000, -261050000,  # 16 -> 21
        -435260000, -742340000, -1224190000, -2045380000, -3457300000,  # 21 -> 26
        -5830220000, -8989940000, -12592330000, -17645810000,
        )
    __display_name = TranslatableString("Flame", french="Lance-flamme")


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
        -740, -3700, -14100, -27000, -56000,  # 1 -> 6
        -127000, -271000, -380000, -550000, -990000,  # 6 -> 11
        -1850000, -3230000, -5700000, -9770000, -16970000,  # 11 -> 16
        -30130000, -53720000, -94640000, -170230000, -326310000,  # 16 -> 21
        -544070000, -927920000, -1530240000, -2556720000, -4321630000,  # 21 -> 26
        -7287770000, -11237420000, -15740420000, -22057260000,
        )

    def damage_formule(self, target: MovableUnit, target_index=0, hit_combo=0):
        dmg = super().damage_formule(target, target_index=target_index)
        if dmg is None:
            return None
        return (
            dmg
            #* (0.25 * max(0, 4 - target_index)  # FIXME: Do lightning damage reduction apply to tesla?
            * (1.7 if target.is_summoned else 1)  # Damage boost against summoned targets
            )

    __display_name = "Tesla"


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
        -690, -3400, -13100, -25000, -51000,  # 1 -> 6
        -118000, -250000, -350000, -510000, -910000,  # 6 -> 11
        -1710000, -2990000, -5280000, -9040000, -15700000,  # 11 -> 16
        -27870000, -49690000, -87540000, -157470000, -301840000,  # 16 -> 21
        -503260000, -858330000, -1415470000, -2364970000, -3997510000,  # 21 -> 26
        -6741190000, -10394610000, -14559880000, -20402970000,
        )
    __display_name = TranslatableString("Barrier", french="Barrière")


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
        -700, -3500, -13400, -26000, -53000,  # 1 -> 6
        -121000, -257000, -360000, -530000, -940000,  # 6 -> 11
        -1750000, -3070000, -5420000, -9280000, -16120000,  # 11 -> 16
        -28620000, -51030000, -89900000, -161720000, -309990000,  # 16 -> 21
        -516870000, -881530000, -1453730000, -2428890000, -4105550000,  # 21 -> 26
        -6923380000, -10675550000, -14953400000, -20954400000,
        )
    __display_name = TranslatableString("Harpoon", french="Harpon")


class Cryomancer(ModuleWeapon):
    attack_base = 310
    hit_frequency = 0.5
    range = 8
    armor_piercing = 3
    shoot_to = TargetType.AIR_GROUND
    rarity = Rarity.Legendary

    froze_chance = 0.25
    froze_duration = 2

    tower_froze_chance = 0.6
    # TODO: test if it's 60% chance on each hit, or 60% on successful froze hit
    tower_froze_radius = 6
    tower_froze_duration = 6

    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -690, -3400, -13100, -25000, -51000,  # 1 -> 6
        -118000, -250000, -350000, -510000, -910000,  # 6 -> 11
        -1710000, -2990000, -5280000, -9040000, -15700000,  # 11 -> 16
        -27870000,
        )
    __display_name = TranslatableString("Cryomancer", french="Cryomancien")


class Archidruid(ModuleWeapon):
    attack_base = 250
    hit_frequency = 0.8
    range = 8
    armor_piercing = 0
    shoot_to = TargetType.AIR_GROUND
    rarity = Rarity.Legendary

    slow_factor = 0.3
    slow_duration = None  # TODO

    slow_ower_radius = 10
    slow_tower_factor = 0.3

    upgrade_costs = Cryomancer.upgrade_costs  # new modules seem to have the same costs

    __display_name = TranslatableString("Arch Druid", french="Archidruide")


class ShieldInvoker(ModuleWeapon):
    attack_base = 150
    hit_frequency = 0.5
    range = 8
    armor_piercing = 0
    shoot_to = TargetType.AIR_GROUND
    rarity = Rarity.Legendary

    shield_radius = 5
    shield_miss_factor = 0.5

    upgrade_costs = Cryomancer.upgrade_costs  # new modules seem to have the same costs

    __display_name = TranslatableString("Shield Caster", french="Invocatrice de bouclier")


class MirrorWizard(ModuleWeapon):
    attack_base = 175
    hit_frequency = 0.4
    range = 8
    armor_piercing = 0
    shoot_to = TargetType.AIR_GROUND
    rarity = Rarity.Legendary

    def damage_reduction_factor(self, attacker: BaseUnit):
        if isinstance(attacker, Tower):
            return 0.5 - (0.5 * max(0, attacker.level - self.level))
            # TODO damage are reflected to a nearby bandits
        else:
            return 1.0

    __display_name = TranslatableString("Mirror Mage", french="Mage miroir")


# Register all defined cards
MODULES.register_cards_in_module(ModuleWeapon, __name__)
