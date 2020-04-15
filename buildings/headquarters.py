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
from typing import Tuple

from buildings.base_buildings import Building
from common.cards import Upgrade
from common.card_categories import BUILDINGS
from common.resources import ResourcePacket, resourcepackets


class HQ(Building):
    base_building = None
    upgrade_costs = resourcepackets(
        (400, 800),  # level 1 -> 2
        (1700, 4800),
        (11000, 27200),
        (33000, 81000),
        (107000, 267000),
        (267000, 670000),
        (700000, 1480000),
        (900000, 2200000),
        (1300000, 3190000),
        (1500000, 5700000),  # level 10 -> 11
        (2600000, 10670000),
        (4200000, 18660000),
        (7200000, 32940000),
        (11800000, 56400000),
        (20000000, 98000000),  # level 15 -> 16
        (37200000, 173990000),
        (66600000, 310220000),
        (117800000, 546510000),
        (212300000, 983100000),
        )

    # At this point, other buildings classes don't exist yet, so we just store their names in this temporary attribute,
    # and later, this list will be converted and stored into upgrade_requirements.
    _upgrade_requirements_str = [
        (),  # level 1 -> 2
        ("Camp", "Academy"),
        ("Tavern", "Garage"),
        ("WorkShop", "Weaponsmith"),
        ("Mill", "Camp", "Academy"),
        ("TransportStation", "Laboratory", "Tavern"),
        ("Mill", "Camp", "WorkShop"),
        ("TransportStation", "WorkShop", "Garage"),
        ("Tavern", "Academy", "Weaponsmith"),
        ("Mill", "Camp", "Weaponsmith"), # level 10 -> 11
        ("TransportStation", "Laboratory", "Tavern"),
        ("Mill", "Camp", "WorkShop"),
        ("TransportStation", "Weaponsmith", "Garage"),
        ("Tavern", "Academy", "WorkShop"),
        ("Mill", "Camp", "Weaponsmith"),
        ("TransportStation", "Laboratory", "Tavern"),  # level 16 -> 17
        ("Mill", "Camp", "WorkShop"),
        ("TransportStation", "Weaponsmith", "Garage"),
        ("Tavern", "Academy", "WorkShop"),
        ("Tavern", "Academy", "WorkShop"),  # level 19 -> 20
        ]
    """List the buildings needed for upgrading the HQ. Here requirements are stored as strings, you will probably
    be more interested in the attribute <upgrade_requirements> which is the same but with classes instead."""
    upgrade_requirements = None  # This attribute will be defined later, once other building classes will be initialized
    """List the buildings needed for upgrading the HQ. 
    upgrade_requirements[n] store the requirement for upgrading from level n+1 to n+2
    (Warning: be aware that this attribute is set to None, until 
    other buildings classes are defined, a.k.a after buildings/buildings.py is imported for the first time)"""

    def get_upgrade(self):
        # Special case for the HQ which have multiple changing requirements

        assert self.level > 0, "level should be a strictly positive integer"
        assert self.level <= len(self.upgrade_costs), "{} get_upgrade attribute is not implemented for level {}".format(cls.__name__, level)
        assert self.level <= len(self.upgrade_requirements), "{} upgrade_requirements  is not implemented for level {}".format(type(self).__name__, self.level)

        if self.level == 1:
            # Nothing is necessary for level 1
            return Upgrade(ResourcePacket(), [])
        else:
            # It doesn't seem necessary to include previous headquarter level in requirements as other requirements will
            #   already include it when resolving full dependency.
            return Upgrade(self.upgrade_costs[self.level - 1], self.upgrade_requirements[self.level - 1])

    @property
    def wave_number(self) -> Tuple[float, float]:
        return (
            min(5, (self.level + 1) * 0.5),             # first convoy
            max(0, min(5, (self.level - 15) * 0.5)),    # second convoy
        )

    @property
    def wave_lenght(self):
        return max(10, min(15, self.level))

    @property
    def guardian_power(self):
        return 6 * self.wave_lenght * sum(self.wave_number) # FIXME verify formulas for level > 15. Does the 2nd convoy follow the same rules?


# Register all defined cards
BUILDINGS.register_cards_in_module(Building, __name__)
