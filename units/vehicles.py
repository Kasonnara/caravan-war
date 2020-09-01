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

from buildings.buildings import Garage
from common.alignment import Alignment
from common.card_categories import VEHICLES
from common.rarity import Rarity
from common.resources import resourcepackets_gold
from lang.languages import TranslatableString
from units.base_units import MovableUnit, reincarnation
from common.target_types import TargetType


class Vehicle(MovableUnit):
    base_building = Garage
    alignment = Alignment.DEFENDER
    move_speed = 1.2
    weapon_slot = 1
    __display_name = TranslatableString("Vehicle", french="Véhicule")


class Charrette(Vehicle):
    hp_base = 2280
    shooted_as = TargetType.GROUND
    armor = 3
    cost = 8
    rarity = Rarity.Common
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -200, -1100, -4100, -9000, -24000,  # 1 -> 6
        -56000, -119000, -170000, -240000, -430000,  # 6 -> 11
        -810000, -1420000, -2500000, -4290000, -7450000,  # 11 -> 16
        -13220000, -23570000, -41530000, -74700000, -143190000,  # 16 -> 21
        -238750000, -407200000, -671510000, -1121970000, -1896460000,  # 21 -> 26
        -3198090000, -4931310000, -6907360000, -9679380000,
        )
    __display_name = TranslatableString("Cart", french="Charrette")


class Chariot(Vehicle):
    hp_base = 1710
    shooted_as = TargetType.GROUND
    armor = 3
    cost = 8
    move_speed = 1.8
    rarity = Rarity.Rare
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -200, -1000, -3700, -8000, -22000,  # 1 -> 6
        -50000, -107000, -150000, -220000, -390000,  # 6 -> 11
        -730000, -1280000, -2250000, -3860000, -6700000,  # 11 -> 16
        -11900000, -21220000, -37380000, -67230000, -128880000,  # 16 -> 21
        -214880000, -366480000, -604360000, -1009770000, -1706810000,  # 21 -> 26
        -2878280000, -4438180000, -6216630000, -8711450000,
        )
    __display_name = "Chariot"


class Dirigeable(Vehicle):
    hp_base = 3705
    shooted_as = TargetType.AIR
    armor = 3
    cost = 6
    effect_range = 7
    rarity = Rarity.Legendary
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -400, -2200, -8300, -19000, -49000,  # 1 -> 6
        -112000, -237000, -330000, -490000, -870000,  # 6 -> 11
        -1620000, -2840000, -5010000, -8570000, -14890000,  # 11 -> 16
        -26440000, -47150000, -83060000, -149410000, -286390000,  # 16 -> 21
        -477510000, -814400000, -1343030000, -2243930000, -3792920000,  # 21 -> 26
        -6396180000, -9862630000, -13814730000, -19358770000,
        )
    __display_name = TranslatableString("Air Ship", french="Dirigeable")


class Speeder(Vehicle):
    hp_base = 3800
    shooted_as = TargetType.AIR
    armor = 5
    cost = 8
    effect_range = 4  # Fixme verify value
    effect_speed_boost = 1.3
    rarity = Rarity.Legendary
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -500, -2300, -8700, -19000, -51000,  # 1 -> 6
        -117000, -249000, -350000, -510000, -910000,  # 6 -> 11
        -1700000, -2980000, -5260000, -9000000, -15640000,  # 11 -> 16
        -27770000, -49500000, -87210000, -156880000, -300710000,  # 16 -> 21
        -501380000, -855120000, -1410180000, -2356130000, -3982570000,  # 21 -> 26
        -6715990000, -10355760000, -14505460000, -20326710000,
        )
    __display_name = "Speeder"


class Train(Vehicle):
    hp_base = 4251
    shooted_as = TargetType.GROUND
    armor = 8
    cost = 10
    weapon_slot = 2
    rarity = Rarity.Legendary
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -500, -2400, -9300, -21000, -55000,  # 1 -> 6
        -126000, -267000, -370000, -550000, -980000,  # 6 -> 11
        -1820000, -3190000, -5630000, -9650000, -16750000,  # 11 -> 16
        -29750000, -53040000, -93440000, -168080000, -322190000,  # 16 -> 21
        -537200000, -916200000, -1510910000, -2524430000, -4267030000,  # 21 -> 26
        -7195710000, -11095460000, -15541570000, -21778610000,
        )
    __display_name = TranslatableString("Steam Van", french="Fourgon à vapeur")

    def hp_score(self, *args, **kwargs):
        return (
            super().hp_score(*args, **kwargs)
            * 2.5  # Multiply hp_score by 2 (maybe by 3) because the train reflect 50% of the damage taken
            )


class Helicopter(Vehicle):
    hp_base = 2444
    shooted_as = TargetType.AIR
    armor = 0
    cost = 6
    rarity = Rarity.Epic
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -300, -1600, -6200, -14000, -37000,  # 1 -> 6
        -84000, -178000, -250000, -360000, -650000,  # 6 -> 11
        -1220000, -2130000, -3760000, -6430000, -11170000,  # 11 -> 16
        -19830000, -35360000, -62290000, -112060000, -214790000,  # 16 -> 21
        -358130000, -610800000, -1007270000, -1682950000, -2844690000,  # 21 -> 26
        -4797140000, -7396970000, -10361050000, -14519080000,
        )
    __display_name = "Helicopter"


@reincarnation
class HelicopterLeg(Helicopter):
    pass


class Wagon(Vehicle):
    hp_base = 3250
    shooted_as = TargetType.GROUND
    armor = 5
    cost = 8  # TODO check cost
    rarity = Rarity.Epic
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -400, -1900, -7200, -16000, -43000,  # 1 -> 6
        -98000, -208000, -290000, -420000, -760000,  # 6 -> 11
        -1420000, -2480000, -4380000, -7500000, -13030000,  # 11 -> 16
        -23140000, -41250000, -72680000, -130730000, -250590000,  # 16 -> 21
        -417820000, -712600000, -1175150000, -1963440000, -3318800000,  # 21 -> 26
        -5596660000, -8629800000, -12087890000, -16938920000,
        )
    __display_name = "Wagon"


@reincarnation
class WagonLeg(Wagon):
    pass


class Buggy(Vehicle):
    hp_base = 3000
    move_speed = 1.8
    armor = 4
    rarity = Rarity.Epic
    cost = 6
    # TODO spell
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -400, -1800, -6800, -15000, -40000,  # 1 -> 6
        -92000, -196000, -270000, -400000, -720000,  # 6 -> 11
        -1340000, -2340000, -4130000, -7070000, -12290000,  # 11 -> 16
        -21820000, -38900000, -68520000, -123260000, -236270000,  # 16 -> 21
        -393940000, -671880000, -1108000000, -1851250000, -3129160000,  # 21 -> 26
        -5276850000, -8136670000, -11397150000, -15970980000,
        )
    __display_name = "Buggy"


@reincarnation
class BuggyLeg(Buggy):
    pass


# Register all defined cards in CARD_DICTIONNARY
VEHICLES.register_cards_in_module(Vehicle, __name__)
