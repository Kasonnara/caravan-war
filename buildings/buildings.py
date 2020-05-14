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

from buildings.base_buildings import Building
from buildings.headquarters import HQ

from common.card_categories import BUILDINGS
from common.resources import resourcepackets_gold, resourcepackets_goods, ResourcePacket, Resources, resourcepackets


class Mill(Building):
    upgrade_costs = [ResourcePacket(Resources.Goods(-50))] \
        + resourcepackets_gold(
        -510, -3400, -19400, -58000, -191000,                     # 1 -> 6
        -437000, -930000, -1300000, -1900000, -3670000,          # 6 -> 11
        -6860000, -12000000, -21170000, -36260000, -63000000,    # 11 -> 16
        )
    hourly_incomes = resourcepackets_goods(
        0,  # level 0
        300, 525, 1500, 2250, 3750,
        6000, 7500, 12000, 18000, 25500,
        35000, 55000, 85000, 130000, 200000,
        320000, 510000, 815000, 1280000, 2050000,
        )
    storage_limits = None  # TODO


class TransportStation(Building):
    upgrade_costs = resourcepackets_goods(
        -50,  # 0 -> 1
        -500, -2100, -13000, -36000, -119000,                   # 1 -> 6
        -297000, -700000, -1000000, -1400000, -1700000,         # 6 -> 11
        -2900000, -4700000, -7900000, -13100000, -22200000,     # 11 -> 16
        -41300000, -74000000, -130800000, -235800000,
        )
    hourly_incomes = resourcepackets_gold(
        0,  # level 0
        600, 1050, 3000, 4500, 7500,
        None, 15000, 24000, 36000, 47000,
        70000, 110000, 170000, 260000, 400000,
        640000, 1020000, 1630001,
        )
    storage_limits = None  # TODO


class Bank(Building):
    storage_limits = (
        0,  # level 0
        30000, 40000, 80000, 170000, 500000,
        1100000, 1800000, 2800000, 3600000, 6000000,
        10990000, 19990000, 34990000, 59990000, 109990000,
        199990000, 349990003, 600000000, 1100000000, 2500000000,
        )


class Storage(Building):
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -510, -3400, -19400, -58000, -191000,  # 1 -> 6
        -437000, -930000, -1300000, -1900000, -3670000,  # 6 -> 11
        -6860000, -12000000, -21170000, -36260000, -63000000,  # 11 -> 16
        )
    storage_limits = (
        0,  # level 0
        30000, 40000, 60000, 100000, 250000,
        550000, 850000, 1100000, 1400000, 1800000,
        2990000, 4990000, 7990000, 12990000, 21990000,
        39990000, 69990000, 129990000, 250000000, 500000000,
        )


class Laboratory(Building):
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -210, -1400, -7800, -23000, -77000,                  # 1 -> 6
        -175000, -370000, -520000, -760000, -1360000,        # 6 -> 11
        -2540000, -4450000, -7850000, -13430000, -23340000,  # 11 -> 16
        -41430000, -73870000, -130130000, -234080000,
        )


class Tavern(Building):
    upgrade_costs = [ResourcePacket(-500, 0)] + resourcepackets_gold(
        -690, -4600, -26400, -79000, -259000,   # 1 -> 6
        -595000, -1260000, -1770000, -2580000, -5160000,  # 6 -> 11
        -9150000, -16000000, -28230000, -48350000, -84000000,  # 11 -> 16
        -149140000, -265910000, -468440000, -842660000,
        )

    @property
    def bandit_power(self):
        # TODO optimization, if necessary to get multiple time this value while level isn't changing it would be more
        #   lighter to compute this value once in __init__ and store it under <bandit_power> attribute.
        return (
            25                                  # base (in theory at level 0)
            + 15 * min(self.level, 15)          # from level 1 to 15, you get 15 power per level
            + 20 * max(self.level - 15, 0)      # from level 16 to ?, you get 20 power per level
            )


class Camp(Building):
    upgrade_costs = resourcepackets_gold(
        -100,  # 0 -> 1
        -650, -4400, -25700, -76000, -259000,  # 1 -> 6
        -630000, -1410000, -2020000, -3110000, -5430000,  # 6 -> 11
        -10160000, -17770000, -31370000, -53720000, -93330000,  # 11 -> 16
        -165710000, -295450000, -520490000, -936290000,
        )


class Academy(Building):
    upgrade_costs = resourcepackets_gold(
        -250,  # 0 -> 1
        -410, -2700, -15500, -46000, -153000,  # 1 -> 6
        -350000, -740000, -1040000, -1520000, -3400000,  # 6 -> 11
        -6350000, -11110000, -19610000, -33580000, -58330000,  # 11 -> 16
        -103570000, -184660000, -325310000, -585180000,
        )


class Weaponsmith(Building):
    upgrade_costs = resourcepackets(
        (-0, -0),
        (-200, -210),
        (-700, -1600),
        (-4000, -10900),
        (-9000, -32000),
        (-29000, -122000),
        (-72000, -280000),
        (-200000, -670000),
        (-300000, -940000),
        (-400000, -1370000),
        (-400000, -2720000),
        (-700000, -5080000),
        (-1200000, -8890000),
        (-1900000, -15690000),
        (-3200000, -26860000),
        (-7100000, -46670000),
        (-10000000, -82860000),
        (-17800000, -147730000),
        (-31400000, -260250000),
        (-56600000, -468150000),
    )


class Garage(Building):
    upgrade_costs = resourcepackets(
        (-100, -0),  # 0 -> 1
        (-100, -250),
        (-500, -1600),
        (-3000, -9300),
        (-8000, -28000),
        (-24000, -115000),
        (-60000, -263000),
        (-200000, -560000),
        (-200000, -780000),
        (-300000, -1140000),
        (-400000, -2450000),
        (-600000, -4580000),
        (-1000000, -8000000),
        (-1600000, -14120000),
        (-2700000, -24180000),
        (-5400000, -42000000),
        (-8300000, -74570000),
        (-14800000, -132960000),
        (-26200000, -234220000),
        (-47200000, -421330000),
    )


class WorkShop(Building):
    upgrade_costs = [ResourcePacket(-300, 0)] + resourcepackets_gold(
        -610, -4100, -23300, -79000, -259000,  # 1 -> 6
        -630000, -1410000, -2080000, -3190000, -5160000,  # 6 -> 11
        -9660000, -16880000, -29800000, -51030000, -88670000,  # 11 -> 16
        -157420000, -280680000, -494470000, -889470000,
        )
    
    @property
    def tower_power(self):
        # TODO optimization, if necessary to get multiple time this value while level isn't changing it would be more
        #   lighter to compute this value once in __init__ and store it under <tower_power> attribute.
        return 350 + 100 * self.level - 50 * min(max(0, self.level - 5), 10)


class Forge(Building):
    base_building_level = 8
    upgrade_costs = resourcepackets_gold(
        None,
        None, -707000, -1900500, None, None,
        None, None, None, None, None,
        None, None, None, None, None,
        )


class HeroTemple(Building):
    base_building_level = 10
    upgrade_costs = resourcepackets_gold(
        None,  # 0 -> 1
        None, None, -1900500, -3556500, -6219500,
        -10979500, -18802000, None, None, None,
        None, None, None, None, None,
        )
    ambush_xp_incomes = [
        Resources.HeroExperience(xp_qty)
        if xp_qty is not None else None  # FIXME: remove this line as soon as all None values are replaced
        for xp_qty in (
            0,  # level 0
            10, 20, None, 80, None,
            None, 231, 266, None, None,
            None, None, None, None, None,
            )
        ]


class Altar(Building):
    base_building_level = 7
    upgrade_costs = resourcepackets_gold( 
        0,  # 0 -> 1
        -740000, -1040000, -1520000, -1520000, -2720000,  # 1 -> 6
        -5080000, -8900000, -15700000, -26860000, -46680000,  # 6 -> 11
        -82860000, -147740000, -260260000,
        )


# Register all defined cards
BUILDINGS.register_cards_in_module(Building, __name__)


#  Set back the HQ requirement
#  Create a temporary building dict
buildings_dict = {
    building.__name__: building
    for building in BUILDINGS
    }
# Generate the list of requirements
HQ.upgrade_requirements = [
    list(
        buildings_dict[str_requirement](level)
        for str_requirement in str_requirements
        )
    for level, str_requirements in enumerate(HQ._upgrade_requirements_str)
    ]
del buildings_dict
