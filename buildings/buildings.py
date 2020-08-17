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
from common.resources import Resources as R
from utils.utils import get_index_greather_than

_MILL_TRANSPORTSTATION_HOURLY_INCOMES = (
    0,  # should be None level 0 doesn't exist
    300, 525, 1500, 2250, 3750,
    6000, 7500, 12000, 18000, 25500,
    35000, 55000, 85000, 130000, 200000,
    320000, 510000, 815000, 1280000, 2050000,
    3200000, 4800000, 7360000, 10880000, 16320000,
    24640000, 37120000, 51200000, 64000000, 80000000,
    )


class Mill(Building):
    upgrade_costs = resourcepackets_gold(
        0,  # should be None level 0 doesn't exist
        -510, -3400, -19400, -58000, -191000,                     # 1 -> 6
        -437000, -930000, -1300000, -1900000, -3670000,          # 6 -> 11
        -6860000, -12000000, -21170000, -36260000, -63000000,    # 11 -> 16
        -111850000, -199430000, -351330000, -631990000, -1211430000,
        -2019860000, -3444920000, -5681010000, -9491840000, -16044050000,
        -27055850000, -41718920000, -58436290000, -81887590000,
        )
    bihourly_incomes = resourcepackets_goods(*(x * 2 for x in _MILL_TRANSPORTSTATION_HOURLY_INCOMES))
    # MEMORY SAVING possible here if necessary
    storage_limits = [x * 8 for x in _MILL_TRANSPORTSTATION_HOURLY_INCOMES]


class TransportStation(Building):
    upgrade_costs = resourcepackets_goods(
        0,  # should be None level 0 doesn't exist
        -500, -2100, -13000, -36000, -119000,                   # 1 -> 6
        -297000, -700000, -1000000, -1400000, -1700000,         # 6 -> 11
        -2900000, -4700000, -7900000, -13100000, -22200000,     # 11 -> 16
        -41300000, -74000000, -130800000, -235800000, -414500000,
        -697700000, -1197000000, -1988600000, -3335200000, -5638300000,
        -9509000000, -14663200000, -20539500000, -28782900000,
        )
    # MEMORY SAVING possible here if necessary
    bihourly_incomes = resourcepackets_gold(*(x * 2 for x in _MILL_TRANSPORTSTATION_HOURLY_INCOMES))
    # MEMORY SAVING possible here if necessary
    storage_limits = Mill.storage_limits
del _MILL_TRANSPORTSTATION_HOURLY_INCOMES


class Bank(Building):
    upgrade_costs = resourcepackets(
        (0, 0),  # should be None level 0 doesn't exist
        (-300, -0),
        (-1300, -0),
        (-8000, -0),
        (-22000, -0),
        (-83000, -0),
        (-208000, -0),
        (-500000, -0),
        (-700000, -0),
        (-1000000, -0),  # 9 -> 10
        (-1200000, -1200000),
        (-2000000, -2300000),
        (-3300000, -4000000),
        (-5600000, -7100000),
        (-9200000, -12100000),
        (-15600000, -21000000),
        (-28900000, -37300000),
        (-51800000, -66500000),
        (-91600000, -117100000),
        (-165100000, -210700000),
        (-290200000, -404000000),
        (-488400000, -673000000),
        (-837900000, -1148000000),
        (-1392000000, -1894000000),
        (-2334600000, -3164000000),
        (-3946800000, -5348000000),
        (-6656300000, -9019000000),
        (-10264300000, -13906000000),
        (-14377700000, -19479000000),
        (-20148100000, -27296000000),  # 29 -> 30
        )

    storage_limits = (
        0,  # should be None level 0 doesn't exist
        10000, 20000, 60000, 150000, 490000,
        1090000, 1790000, 2790000, 3590000, 5990000,
        10990000, 19990000, 34990000, 59990000, 109990000,
        199990000, 349990003, 599980000, 1099990000, 2499990000,
        3999990000, 5999990000, 9999990000, 16999990000, 27999990000,
        44999990000, 65999990000, 94999990000, 129999990000, 139999990000,
        )


class Storage(Building):
    upgrade_costs = resourcepackets_gold(
        0,  # should be None level 0 doesn't exist
        -510, -3400, -23300, -69000, -229000,  # 1 -> 6
        -525000, -1110000, -1560000, -2280000, -2900000,  # 6 -> 11
        -5300000, -9300000, -16500000, -28200000, -49000000,  # 11 -> 16
        -87000000, -155100000, -273300000, -491600000, -942000000,
        -1571000000, -2679000000, -4419000000, -7383000000, -12479000000,
        -21043000000, -32448000000, -45450000000, -63690000000,
        )
    storage_limits = (
        0,  # should be None level 0 doesn't exist
        10000, 20000, 40000, 80000, 230000,
        530000, 830000, 1090000, 1390000, 1790000,
        2990000, 4990000, 7990000, 12990000, 21990000,
        39990000, 69990000, 129990000, 249990000, 499990000,
        799990000, 1399990000, 1999990000, 3499990000, 5999990000,
        8999990000, 14999990000, 19999990000, 29999990000, 39999990000,
        )


class Laboratory(Building):
    upgrade_costs = resourcepackets_gold(
        0,  # should be None level 0 doesn't exist
        -210, -1400, -7800, -23000, -77000,                  # 1 -> 6
        -175000, -370000, -520000, -760000, -1360000,        # 6 -> 11
        -2540000, -4450000, -7850000, -13430000, -23340000,  # 11 -> 16
        -41430000, -73870000, -130130000, -234080000, -448680000,
        -748100000, -1275900000, -2104080000, -3515500000, -5942240000,
        -10020690000, -15451460000, -21643070000, -30328740000,
        )


class Tavern(Building):
    upgrade_costs = resourcepackets_gold(
        0,  # FIXME should be None level 0 doesn't exist
        -690, -4600, -26400, -79000, -259000,   # 1 -> 6
        -595000, -1260000, -1770000, -2580000, -5160000,  # 6 -> 11
        -9150000, -16000000, -28230000, -48350000, -84000000,  # 11 -> 16
        -149140000, -265910000, -468440000, -842660000, -1615230000,
        -2693150000, -4593230000, -7574680000, -12655790000, -21392070000,
        -36074470000, -55625230000, -77915050000, -109183450000,
        )

    @property
    def bandit_power(self):
        # TODO optimization, if necessary to get multiple time this value while level isn't changing it would be more
        #   lighter to compute this value once in __init__ and store it under <bandit_power> attribute. or memoize it
        return (
            25                                  # base (in theory at level 0)
            + 15 * min(self.level, 15)          # from level 1 to 15, you get 15 power per level
            + 30 * max(self.level - 15, 0)      # from level 16 to 30, you get 30 power per level
            )


class Camp(Building):
    upgrade_costs = resourcepackets_gold(
        0,  # should be None level 0 doesn't exist
        -650, -4400, -25700, -76000, -259000,  # 1 -> 6
        -630000, -1410000, -2020000, -3110000, -5430000,  # 6 -> 11
        -10160000, -17770000, -31370000, -53720000, -93330000,  # 11 -> 16
        -165710000, -295450000, -520490000, -936290000, -1794700000,
        -2992380000, -5103590000, -8416310000, -14061980000, -23768960000,
        -40082740000, -61805810000, -86572280000, -121314940000,
        )


class Academy(Building):
    upgrade_costs = resourcepackets_gold(
        0,  # should be None level 0 doesn't exist
        -410, -2700, -15500, -46000, -153000,  # 1 -> 6
        -350000, -740000, -1040000, -1520000, -3400000,  # 6 -> 11
        -6350000, -11110000, -19610000, -33580000, -58330000,  # 11 -> 16
        -103570000, -184660000, -325310000, -585180000, -1121690000,
        -1870240000, -3189740000, -5260200000, -8788740000, -14855600000,
        -25051720000, -38628630000, -54107680000, -75821840000,
        )


class Weaponsmith(Building):
    upgrade_costs = resourcepackets(
        (-0, -0),  # should be None level 0 doesn't exist
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
        (-99500000, -897350000),
        (-167500000, -1496190000),
        (-287300000, -2551800000),
        (-477300000, -4208160000),
        (-800500000, -7030990000),
        (-1353200000, -11884480000),
        (-2282200000, -20041370000),
        (-3519200000, -30902910000),
        (-4929500000, -43286140000),
        (-6907900000, -60657470000),
        )


class Garage(Building):
    upgrade_costs = resourcepackets(
        (-0, -0),  # 0 -> 1, should be None level 0 doesn't exist
        (-100, -250),
        (-500, -1600),
        (-3000, -9300),
        (-8000, -28000),
        (-24000, -115000),  # 5 -> 6
        (-60000, -263000),
        (-200000, -560000),
        (-200000, -780000),
        (-300000, -1140000),
        (-400000, -2450000),  # 10 -> 11
        (-600000, -4580000),
        (-1000000, -8000000),
        (-1600000, -14120000),
        (-2700000, -24180000),
        (-5400000, -42000000),  # 15 -> 16
        (-8300000, -74570000),
        (-14800000, -132960000),
        (-26200000, -234220000),
        (-47200000, -421330000),
        (-82900000, -807620000),
        (-139600000, -1346580000),
        (-239400000, -2296620000),
        (-397800000, -3787340000),
        (-667100000, -6327900000),
        (-1127700000, -10696040000),
        (-1901800000, -18037240000),
        (-2932700000, -27812620000),
        (-4107900000, -38957530000),
        (-5756600000, -54591730000),
        )


class WorkShop(Building):
    upgrade_costs = resourcepackets_gold(
        0,  # should be None level 0 doesn't exist
        -610, -4100, -23300, -79000, -259000,  # 1 -> 6
        -630000, -1410000, -2080000, -3190000, -5160000,  # 6 -> 11
        -9660000, -16880000, -29800000, -51030000, -88670000,  # 11 -> 16
        -157420000, -280680000, -494470000, -889470000, -1704970000,
        -2842770000, -4848410000, -7995490000, -13358880000, -22580880000,
        -38078610000, -58715520000, -82243660000, -115249190000,
        )
    
    @property
    def tower_power(self):
        # CPU SAVING, if necessary to get multiple time this value while level isn't changing it would be more
        #   lighter to compute this value once in __init__ and store it under <tower_power> attribute.
        return 350 + 100 * self.level - 50 * min(max(0, self.level - 5), 10)


class Forge(Building):
    base_building_level = 8
    upgrade_costs = resourcepackets_gold(
        0,
        -707000, -1088500, -1900500, -3556500, -6219500,
        -10979500, -18802000, -32665500, -57998500, -103407500,
        -182171500, -327701500, -628145000, -1047333000, -1786256500,
        -2945708500, -3921693000, -8319136000, -14028959000, -21632033500,
        -30300298000, -42460229000,
        )


class HeroTemple(Building):
    base_building_level = 8
    upgrade_costs = Forge.upgrade_costs
    #upgrade_costs = resourcepackets_gold(
    #    0,  # 0 -> 1
    #    -707000, 1088500, -1900500, -3556500, -6219500,  # 1 -> 6
    #    -10979500, -18802000, -32665500, -57998500, -103407500,  # 6 -> 11
    #    -182171500, -327701500, None, None, None,  # 11 -> 16
    #    )
    ambush_xp_incomes = [
        Resources.HeroExperience(xp_qty)
        if xp_qty is not None else None  # FIXME: remove this line as soon as all None values are replaced
        for xp_qty in (
            0,  # level 0
            50, 60, 70, 80, 150,
            201, 231, 266, 306, 352,
            405, 465, 535, 615, 708,
            814, 920, 1026,
            )
        ]


class Altar(Building):
    base_building_level = 6
    upgrade_costs = resourcepackets_gold( 
        0,  # 0 -> 1
        -740000, -1040000, -1520000, -1520000, -2720000,  # 1 -> 6
        -5080000, -8900000, -15700000, -26860000, -46680000,  # 6 -> 11
        -82860000, -147740000, -260260000, -468160000, -897360000,
        -1496200000, -2551800000, -4208160000, -7031000000, -11884480000,
        -20041380000, -30902920000, -43286140000,
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
        buildings_dict[str_requirement](upgrade_from_level)
        for str_requirement in str_requirements
        ) + [
        Bank(get_index_greather_than(abs(HQ.upgrade_costs[upgrade_from_level][R.Gold]), Bank.storage_limits)),
        Storage(get_index_greather_than(abs(HQ.upgrade_costs[upgrade_from_level][R.Goods]), Storage.storage_limits)),
        ]
    for upgrade_from_level, str_requirements in enumerate(HQ._upgrade_requirements_str)
    ]
del buildings_dict
