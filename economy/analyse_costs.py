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
from buildings.buildings import Mill, Laboratory

"""
The purpose of this script is to plot cost evolution of upgradable object (unit, buildings, etc.) 
to manually identify paterns and realtions.

The main objective is to find a relation that describe cost evolution of everything

Assumptions tested:
- [X] There is a relation between building/unit costs and HQ cost. [results: plots are similar but not identical 
until level 11 where cost grow factor stabilize]
- [X] There is a relation between building/unit upgrade cost and ligue exchange gains. [results: No]
"""

from buildings.headquarters import HQ
from common.ligues import Ligue
from units.towers import HeavySniper, Stormspire

import matplotlib.pyplot as plt

fig = plt.figure()

goods_ax = plt.subplot(2, 1, 1, title="Relative Goods")
gold_ax = plt.subplot(2, 1, 2, title="Relative Gold")
#abs_goods_ax = plt.subplot(2, 2, 2, title="Goods")
#abs_gold_ax = plt.subplot(2, 2, 4, title="Gold")

for upgradable in (HQ, Stormspire, HeavySniper, Mill, Laboratory):
    goods, gold = zip(*upgradable.upgrade_cost)
    relative_goods, relative_gold = tuple([(c2 / c1 if c1 != 0 else 0)  for c1, c2 in zip(l[:-1], l[1:])] for l in (goods, gold))
    #abs_goods, abs_gold = tuple( [(c / l[0] if l[0] != 0 else 0) for c in l] for l in (goods, gold))

    goods_ax.plot(range(2, len(relative_goods) + 2), relative_goods, "+-", label=upgradable.__name__)
    gold_ax.plot(range(2, len(relative_gold) + 2), relative_gold, "+-", label=upgradable.__name__)
    #abs_goods_ax.plot(range(len(abs_goods)), abs_goods, "+-", label=upgradable.__name__)
    #abs_gold_ax.plot(range(len(abs_gold)), abs_gold, "+-", label=upgradable.__name__)

# Test correlation with ligues (Results: Doesn't seem to be correlated)
#ligue_goods = [ligue.ex10km_goods_cost for ligue in Ligue]
#ligue_gold = [ligue.ex10km_gold_reward for ligue in Ligue]
#
#relative_ligue_goods, relative_ligue_gold = tuple([(c2 / c1 if c1 != 0 else 0) for c1, c2 in zip(l[:-1], l[1:])] for l in (ligue_goods, ligue_gold))
#
#goods_ax.plot(range(1, len(relative_ligue_goods) + 1), relative_ligue_goods, "+:", label="Ligue rank")
#gold_ax.plot(range(1, len(relative_ligue_gold) + 1), relative_ligue_gold, "+:", label="Ligue rank")

plt.legend()
plt.show()


