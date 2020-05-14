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

from common.resources import ResourcePacket
from common.resources import Resources as R


class Rank(Enum):
    # TODO make it inherit from Upgradeable?
    # name = (index, required trophy, 10km trading cost, goods bonus in raid (can be omitted if not irregular))
    NONE =         (-1, -1,       1,)
    """Special value used when computing rewards without a specific rank in mind. If this rank is used the returned 
    value of gold and goods represent the corresponding number of 10km convoy"""
    Dunkey1 =      ( 0, 0,       2000,   500)
    Dunkey2 =      ( 1, 80,      2600,   700)
    Dunkey3 =      ( 2, 110,      3200,   800)
    Wolf1 =        ( 3, 150,      4000,  1000)
    Wolf2 =        ( 4, 240,      4900,  1200)
    Wolf3 =        ( 5, 330,      5800,  1500)
    Horse1 =       ( 6, 450,      7000,  1800)
    Horse2 =       ( 7, 615,      8500,  2100)
    Horse3 =       ( 8, 780,     10000,  2500)
    Camel1 =       ( 9, 1000,     12000,  3000)
    Camel2 =       (10, 1270,     14400,  3600)
    Camel3 =       (11, 1540,     16800,  4200)
    Buffalo1 =     (12, 1900,     20000,  5000)
    Buffalo2 =     (13, 2320,     24200,  6100)
    Buffalo3 =     (14, 2740,     28400,  7100)
    Rinoceros1 =   (15, 3300,     34000,  8500)
    Rinoceros2 =   (16, 3960,     41200, 11900)
    Rinoceros3 =   (17, 4620,     48400, 16000)
    Elephant1 =    (18, 5500,     58000, 22000)
    Elephant2 =    (19, 6400,     70600, 31100)
    Elephant3 =    (20, 7300,     83200,)
    Dragon1 =      (21, 8500,    100000,)
    Dragon2 =      (22, 10000,    125000,)
    Dragon3 =      (23, 11500,    160000,)
    RedDragon1 =   (24, 13500,    100000,)
    RedDragon2 =   (25, 15500,    200000,)
    RedDragon3 =   (26, 17500,    320000,)
    BlackDragon1 = (27, 20000,    400000,)
    BlackDragon2 = (28, 22500,    500000,)
    BlackDragon3 = (29, 25000,    630000,)
    Phenix1 =      (30, 29000,   1000000,)
    Phenix2 =      (31, 34000,   1600000,)
    Phenix3 =      (32, 40000,   2550000,)
    IcePhenix1 =   (33, 47000,   4000000,)
    IcePhenix2 =   (34, 55000,   6400000,)
    IcePhenix3 =   (35, 64000,  10000000,)
    Kraken1 =      (36, 74000,  15000000,)
    Kraken2 =      (37, 85000,  23000000,)
    Kraken3 =      (38, 98000,  34000000,)
    RedKraken1 =   (39, 113000,  51000000,)
    RedKraken2 =   (40, 130000,  77000000,)
    RedKraken3 =   (41, 150000, 116000000,)
    Leviathan1 =   (42, 173000, 160000000,)
    Leviathan2 =   (43, 199000, 200000000,)
    Leviathan3 =   (44, 229000, 250000000,)

    def __init__(self, rank: int, required_trophy: int, traiding_base: int, raid_goods_bonus: int = None):
        self.rank = rank
        self.traiding_base = traiding_base
        self.raid_goods_bonus = raid_goods_bonus or (traiding_base / 2)


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
