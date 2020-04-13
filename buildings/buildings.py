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
from buildings.base_buildings import Building
from buildings.headquarters import HQ

from common.card_categories import BUILDINGS


class Mill(Building):
    upgrade_cost = [
        (0, gold) for gold in [
            510,  # 1 -> 2
            3400,
            19400,
            58000,
            191000,
            437000,
            930000,
            1300000,
            1900000,
            3670000,
            6860000,  # 11 -> 12
            12000000,
            21170000,
            36260000,
            ]
        ]


class TransportStation(Building):
    pass


class Bank(Building):
    pass


class Storage(Building):
    pass


class Laboratory(Building):
    upgrade_cost = [
        (0, gold) for gold in [
            210, # lvl 1 -> 2
            1400,
            7800,
            23000,
            77000,
            175000,
            370000,
            520000,
            760000,
            1360000,
            2540000, # lvl 11 -> 12
            4450000,
            7850000,
            13430000,
            23340000,
            41430000,
            73870000,
            130130000,
            ]
        ]


class Tavern(Building):
    @property
    def bandit_power(self):
        # TODO optimization, if necessary to get multiple time this value while level isn't changing it would be more
        #   economical to compute this value once in __init__ and store it under <bandit_power> attribute.
        return (
            25                                  # base (in theory at level 0)
            + 15 * min(self.level, 15)          # from level 1 to 15, you get 15 power per level
            + 20 * max(self.level - 15, 0)      # from level 16 to ?, you get 20 power per level
        )


class Camp(Building):
    pass


class Academy(Building):
    pass


class Weaponsmith(Building):
    pass


class Garage(Building):
    pass


class WorkShop(Building):
    pass


class Forge(Building):
    pass


class HeroTemple(Building):
    pass


class Altar(Building):
    pass


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
    [HQ(level)]
    + list(
        buildings_dict[str_requirement](level)
        for str_requirement in str_requirements
        )
    for level, str_requirements in enumerate(HQ._upgrade_requirements_str, 1)
    ]
del buildings_dict
