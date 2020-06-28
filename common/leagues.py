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

from enum import Enum
from typing import Optional

from common.resources import ResourcePacket
from common.resources import Resources as R


class Rank(Enum):
    # TODO make it inherit from Upgradeable?
    # name = (index, required trophy, 10km trading cost, goods bonus in raid (can be omitted if not irregular))
    NONE =         (-1,     -1,         1,  None,  None, None)
    """Special value used when computing rewards without a specific rank in mind. If this rank is used the returned 
    value of gold and goods represent the corresponding number of 10km convoy"""
    Dunkey1 =      ( 0,      0,      2000,   500,  2000, None)
    Dunkey2 =      ( 1,     80,      2600,   700,  2100, None)
    Dunkey3 =      ( 2,    110,      3200,   800,  2200, None)
    Wolf1 =        ( 3,    150,      4000,  1000,  2300, None)
    Wolf2 =        ( 4,    240,      4900,  1200,  2400, None)
    Wolf3 =        ( 5,    330,      5800,  1500,  2500, None)
    Horse1 =       ( 6,    450,      7000,  1800,  2600, None)
    Horse2 =       ( 7,    615,      8500,  2100,  2700, None)
    Horse3 =       ( 8,    780,     10000,  2500,  2800, None)
    Camel1 =       ( 9,   1000,     12000,  3000,  2900, None)
    Camel2 =       (10,   1270,     14400,  3600,  3000, None)
    Camel3 =       (11,   1540,     16800,  4200,  3200, None)
    Buffalo1 =     (12,   1900,     20000,  5000,  3400, None)
    Buffalo2 =     (13,   2320,     24200,  6100,  3600, None)
    Buffalo3 =     (14,   2740,     28400,  7100,  3800, None)
    Rinoceros1 =   (15,   3300,     34000,  8500,  4000, None)
    Rinoceros2 =   (16,   3960,     41200, 11900,  4200, None)
    Rinoceros3 =   (17,   4620,     48400, 16000,  4400, None)
    Elephant1 =    (18,   5500,     58000, 22000,  4600, None)
    Elephant2 =    (19,   6400,     70600, 31100,  4800, None)
    Elephant3 =    (20,   7300,     83200,  None,  5000, None)
    Dragon1 =      (21,   8500,    100000,  None,  5300, None)
    Dragon2 =      (22,  10000,    125000,  None,  5600, None)
    Dragon3 =      (23,  11500,    160000,  None,  5900, 1522200)
    RedDragon1 =   (24,  13500,    100000,  None,  6200, None)
    RedDragon2 =   (25,  15500,    200000,  None,  6500, 2444000)
    RedDragon3 =   (26,  17500,    320000,  None,  6800, 3066800)
    BlackDragon1 = (27,  20000,    400000,  None,  7100, 3784300)
    BlackDragon2 = (28,  22500,    500000,  None,  7500, 4185000)
    BlackDragon3 = (29,  25000,    630000,  None,  7900, 6659700)
    Phenix1 =      (30,  29000,   1000000,  None,  8300, 10682100)
    Phenix2 =      (31,  34000,   1600000,  None,  8700, 17090400)
    Phenix3 =      (32,  40000,   2550000,  None,  9100, 26544700)
    IcePhenix1 =   (33,  47000,   4000000,  None,  9600, 42585600)
    IcePhenix2 =   (34,  55000,   6400000,  None, 10100, None)
    IcePhenix3 =   (35,  64000,  10000000,  None, 10600, 100265400)
    Kraken1 =      (36,  74000,  15000000,  None, 11100, None)
    Kraken2 =      (37,  85000,  23000000,  None, 11700, None)
    Kraken3 =      (38,  98000,  34000000,  None, 12300, None)
    RedKraken1 =   (39, 113000,  51000000,  None, 12900, 515045400)
    RedKraken2 =   (40, 130000,  77000000,  None, 13500, 771970500)
    RedKraken3 =   (41, 150000, 116000000,  None, 14200, None)
    Leviathan1 =   (42, 173000, 160000000,  None, 14900, None)
    Leviathan2 =   (43, 199000, 200000000,  None, 15600, None)
    Leviathan3 =   (44, 229000, 250000000,  None, 16400, None)

    def __init__(self, rank: int, required_trophy: int, trading_base: int, raid_goods_bonus: Optional[int],
                 clan_war_goods_bounty: Optional[int], clan_war_gold_bounty: Optional[int]):
        self.rank = rank
        self.required_trophy = required_trophy
        self.traiding_base = trading_base
        self.raid_goods_bonus: int = raid_goods_bonus or (trading_base / 2)
        self.clan_war_goods_bounty = clan_war_goods_bounty
        self.clan_war_gold_bounty = clan_war_gold_bounty or (10*trading_base)


Rank.upgrade_costs = [
    # TODO trophy requirement (they are special as we don't lose them)
    ResourcePacket(R.Goods(goods_reward), R.Gold(gold_reward), R.Gem(gem_reward), R.VIP(vip_points_reward))
    for goods_reward, gold_reward, gem_reward, vip_points_reward in [
        # (None, None, None, None),  # Irrelevant for the rank NONE
        # goods,    gold, gem,  vip
        (500,          0,   0,    0),
        (  0,       3000,  20,   50),
        (  0,       3000,  20,   50),
        (  0,       6000,  30,  100),
        (  0,       6500,  30,  150),
        (  0,       6500,  30,  150),
        (  0,      13000,  40,  350),
        (  0,      22500,  40,  500),
        (  0,      22500,  40,  600),
        (  0,      45000,  50,  650),
        (  0,      52500,  50,  700),
        (  0,      52500,  50,  750),
        (  0,     105000,  60,  800),
        (  0,     105000,  70,  900),
        (  0,     105000,  70,  950),
        (  0,     210000,  80, 1000),
        (  0,     229500, 100, 1050),
        (  0,     229500, 100, 1100),
        (  0,     600000, 140, 1200),
        (  0,     650000, 150, 1250),
        (  0,     700000, 150, 1300),
        (  0,    1000000, 200, 1350),
        (  0,    1100000, 220, 1400),
        (  0,    1100000, 220, 1500),
        (  0,    1200000, 250, 1550),
        (  0,    1500000, 250, 1600),
        (  0,    1920000, 250, 1650),
        (  0,    2400000, 250, 1700),
        (  0,    3000000, 250, 1800),
        (  0,    3780000, 250, 1850),
        (  0,    6000000, 250, 1900),
        (  0,    9600000, 250, 1950),
        (  0,   15300000, 250, 2000),
        (  0,   24000000, 250, 2100),
        (  0,   38400000, 250, 2150),
        (  0,   60000000, 250, 3700),
        (  0,   90000000, 250, 3750),
        (  0,  138000000, 250, 3800),
        (  0,  204000000, 250, 3900),
        (  0,  306000000, 250, 3950),
        (  0,  462000000, 250, 4000),
        (  0,  696000000, 250, 4050),
        (  0,  960000000, 250, 4100),
        (  0, 1200000000, 250, 4200),
        (  0, 1500000000, 250, 4250),
        ]
    ]


if __name__ == '__main__':
    l = list(Rank.__members__.values())
    print(l)
    for k in range(len(l)-1):
        print(l[k+1].value[1] / l[k].value[1])
