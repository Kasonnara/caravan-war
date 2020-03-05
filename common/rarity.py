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
from enum import Enum
from typing import Optional


class Rarity(Enum):
    #  name   = gem card cost, gem spell card cost, ratio between 10km exchange and the cost in gold of the card, the same for spells, the value of the card when recycled
    Legendary = 2400, None, None, None, None
    Epic = 390, 8, None, 4/20, None
    Rare = None, 4, 1, 2/20, 6
    Common = None, 2, None, 1/20, 2

    def __init__(self, gem_cost, spell_gem_cost, gold_cost, spell_gold_cost, recycle_value):
        self.gem_cost = gem_cost
        """Cost of weapons, vehicules, guardians and bandits cards when purchased with gems (may be None of the card is not purchasable with gem)"""
        self.spell_gem_cost = spell_gem_cost
        """Cost of spell cards when purchased with gems (may be None of the spell is not purchasable with gem)"""
        self._gold_cost_base = gold_cost
        self._spell_gold_cost_base = spell_gold_cost
        self.recycle_value = recycle_value
        """Value of the card if it is recycled"""

    def gold_cost(self, ligue: 'Ligue') -> Optional[int]:
        """
        Cost of weapons, vehicules, guardians and bandits cards when purchased with gold
        :param ligue: The ligue rank you have when the store was reset.
        :return: int (or None of the card is not purchasable with gold)
        """
        if self._gold_cost_base is None:
            return None
        return ligue.ex10km_goods_cost * self._gold_cost_base

    def spell_gold_cost(self, ligue: 'Ligue') -> Optional[int]:
        """
        Cost of spell cards when purchased with gold
        :param ligue: The ligue rank you have when the store was reset.
        :return: int (or None of the spell is not purchasable with gold)
        """
        if self._spell_gold_cost_base is None:
            return None
        return ligue.ex10km_goods_cost * self._spell_gold_cost_base
