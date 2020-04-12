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
from typing import Type

from common.cards import Upgradable


class CardCategories(Enum):
    GUARDIANS = 'Guardian'
    BANDITS = 'Bandits'
    VEHICLES = 'Vehicles'
    MODULES = 'ModulesWeapon'
    SPELLS = 'Spell'
    CONVOY_BOOSTS = 'ConvoyBoost'
    HEROES = 'Hero'
    BUILDINGS = 'Building'
    TOWERS = 'Tower'

    def __init__(self, display_name) -> None:
        self.display_name = display_name
        super().__init__()
        self.category_base_class = None
        # Register the category into CARD_DICTIONARY (as dict key and also as attribute for cleaner static usage)
        self.cards = set()
        """Set of all card type registered in this category"""

    def register_cards_in_module(self, category_base_class: Type[Upgradable], module_name_to_inspect: str):
        # One to one link between the Enum instance and the actual Card base class
        assert (self.category_base_class is None) or self.category_base_class is category_base_class, \
            "Registering units in one category multiple times with different category_base_class"
        self.category_base_class = category_base_class
        category_base_class.category = self

        # Find and register all units in given module that extends from category_base_class
        import sys, inspect
        for name, obj in inspect.getmembers(sys.modules[module_name_to_inspect]):
            if inspect.isclass(obj) and issubclass(obj, category_base_class) and obj is not category_base_class:
                self.cards.add(obj)

    def __iter__(self):
        """Iterating over the set of cards of this cateory"""
        return self.cards.__iter__()

# Set enum elements to module variable to make them accessible by "from card_categories import ..."
GUARDIANS = CardCategories.GUARDIANS
BANDITS = CardCategories.BANDITS
VEHICLES = CardCategories.VEHICLES
MODULES = CardCategories.MODULES
SPELLS = CardCategories.SPELLS
CONVOY_BOOSTS = CardCategories.CONVOY_BOOSTS
HEROES = CardCategories.HEROES
BUILDINGS = CardCategories.BUILDINGS
TOWERS = CardCategories.TOWERS

# Set a dict mapping card categories to their <.cards> attribute for interoperability with MY_CARDS
ALL_CARD_TYPES = {
    card_category: card_category.cards
    for card_category in CardCategories
    }
"""Dictionnary of all registered cards: mapping a CardCategory as key to the set of cards of ths category"""



"""
Add the following snippet at the end of each file containing units to register

from common.card_categories import SELECT_CATEGORY

# Register all defined cards in CARD_DICTIONNARY
SELECT_CATEGORY.register_cards_in_module(SELECT_CATEGORY_BASE_CLASS, __name__)
"""
