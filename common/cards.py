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
from collections import namedtuple, defaultdict
from typing import Union, Optional, List, Tuple, Type

from common.rarity import Rarity
from utils.class_property import classproperty

Upgrade = namedtuple('Upgrade', 'goods_cost gold_cost requirements')

MAX_LEVEL = 30


class Upgradable:
    upgrade_cost: List[Tuple[int, int]] = None
    # FIXME: fill <upgrade_cost> for all unit and all level, or find an approximation formula
    #        to predict it (cf economy/analyse_costs.py)
    base_building: 'Type[Building]' = None
    base_building_level = 1
    category: str = None

    def __init__(self, level=1):
        assert 0 < level <= MAX_LEVEL, "Level should be in range [1;{}], {} is forbidden".format(MAX_LEVEL, level)
        self.level = level

    def get_upgrade(self):
        """
        Return an Upgrade named tuple containing the costs and requirement for upgrading from (level-1) to (level)
        :param level: int, to level to upgrade to
        :return: named tuple Upgrade{goods_cost: int, gold_cost: int, requirements: List[Upgradable]}
        """
        assert self.level > 0, "level should be a strictly positive integer"
        assert self.upgrade_cost is None, "{} upgrade_cost attribute is not implemented".format(type(self).__name__)
        assert self.level <= len(self.upgrade_cost), "{} upgrade_cost attribute is not implemented for level {}".format(type(self).__name__, self.level)

        # Note: this function apply to any upgradable item, except the HeadQuarters that re-implement the function.

        if self.level == 1:
            return Upgrade(                                                 # for the first level we only need
                0, 0,                                                           # - it's free
                [self.base_building(self.base_building_level)])                 # - the base building to exist

        return Upgrade(                                                     # for next levels, we need:
            *self.upgrade_cost[self.level - 2],                                 #  - paying gold and goods costs
            [type(self)(self.level - 1),                                        #  - previous level
             self.base_building(self.level - 1 + self.base_building_level)])    #  - the base building of the same level


class Card(Upgradable):
    rarity: Rarity = None

    def __init__(self, level=1):
        super().__init__(level)
        self._repr = None

    @classproperty
    def gem_cost(cls):
        return cls.rarity.gem_cost

    @classmethod
    def gold_cost(cls, ligue: 'Ligue'):
        return cls.rarity.gold_cost(ligue)


CARD_DICTIONNARY = defaultdict(list)


def register_card_type(category: str):
    def register_card_type_aux(cls: Type[Upgradable]):
        cls.category = category
        CARD_DICTIONNARY[category].append(cls)
        return cls
    return register_card_type_aux
