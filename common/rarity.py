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

from lang.languages import TranslatableString, Language
from utils.prettifying import Displayable


class Rarity(Displayable, Enum):
    Legendary = 2400, None, None, None, None, TranslatableString("Legendary", french="Legendaire")
    Epic = 390, 8, None, 4/20, None, TranslatableString("Epic", french="Épique")
    Rare = None, 4, 1, 2/20, 6, TranslatableString("Rare", french="Rare")
    Common = None, 2, None, 1/20, 2, TranslatableString("Common", french="Commune")

    def __init__(self, gem_cost, spell_gem_cost, gold_cost, spell_gold_cost, recycle_value, translations=None):
        self.gem_cost = gem_cost
        """Cost of weapons, vehicules, guardians and bandits cards when purchased with gems (may be None of the card is not purchasable with gem)"""
        self.spell_gem_cost = spell_gem_cost
        """Cost of spell cards when purchased with gems (may be None of the spell is not purchasable with gem)"""
        self._gold_cost_base = gold_cost
        self._spell_gold_cost_base = spell_gold_cost
        self.recycle_value = recycle_value
        """Value of the card if it is recycled"""
        self._display_name = translations or TranslatableString(self.name)

    def gold_cost(self, ligue: 'Ligue') -> Optional[int]:
        """
        Cost of weapons, vehicules, guardians and bandits cards when purchased with gold
        :param ligue: The ligue rank you have when the store was reset.
        :return: int (or None of the card is not purchasable with gold)
        """
        if self._gold_cost_base is None:
            return None
        return ligue.traiding_base * self._gold_cost_base

    def spell_gold_cost(self, ligue: 'Ligue') -> Optional[int]:
        """
        Cost of spell cards when purchased with gold
        :param ligue: The ligue rank you have when the store was reset.
        :return: int (or None of the spell is not purchasable with gold)
        """
        if self._spell_gold_cost_base is None:
            return None
        return ligue.traiding_base * self._spell_gold_cost_base

    def display_name(self, language=Language.ENGLISH):
        return self._display_name.translated_into(language)
