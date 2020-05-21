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

"""
File exclusive to the head quarters building which is a little bit different than others
"""

from typing import Tuple

from buildings.base_buildings import Building
from common.cards import Upgrade, MAX_LEVEL
from common.card_categories import BUILDINGS
from common.resources import ResourcePacket, resourcepackets
from common.resources import Resources as R


class HQ(Building):
    base_building = None
    upgrade_costs = [
        ResourcePacket(
            R.Goods(goods_cost),
            R.Gold(gold_cost),
            R.VIP(vip_gain),
            )
        for goods_cost, gold_cost, vip_gain in [
            (-0, -0, 0),  # level 0 -> 1
            (-400, -800, 20),  # level 1 -> 2
            (-1700, -4800, 30),
            (-11000, -27200, 40),
            (-33000, -81000, 100),
            (-107000, -267000, 400),
            (-267000, -670000, 700),
            (-700000, -1480000, 800),
            (-900000, -2200000, 900),
            (-1300000, -3190000, 1000),
            (-1500000, -5700000, 1100),  # level 10 -> 11
            (-2600000, -10670000, 1200),
            (-4200000, -18660000, 1300),
            (-7200000, -32940000, 1400),
            (-11800000, -56400000, 1500),
            (-20000000, -98000000, 1600),  # level 15 -> 16
            (-37200000, -173990000, 1700),
            (-66600000, -310220000, 1800),
            (-117800000, -546510000, 1900),
            (-212300000, -983100000, 2000),  # level 19 -> 20
            (-373100000, -1884440000, 2100),
            (-628000000, -3142000000, 2200),
            (-1077300000, -5358770000, 2300),
            (-1789700000, -8837130000, 2400),
            (-3001700000, -14765080000, 2500),
            (-5074500000, -2495741000, 2600),  # level 25 -> 26
            (-8558100000, -42086880000, 2700),
            (-13196900000, -64896100000, 2800),
            (-18485600000, -90900890000, 2900),
            (-25904700000, -127380690000, 3000),  # level 29 -> 30
            ]
        ]

    # At this point, other buildings classes don't exist yet, so we just store their names in this temporary attribute,
    # and later, this list will be converted and stored into upgrade_requirements.
    # Note: It doesn't seem necessary to include previous headquarter level in requirements as other requirements will
    #       already include it when resolving full dependency, but I include it in case this is used without resolving
    #       all dependancies.
    _upgrade_requirements_str = [
        (),  # level 0 -> 1
        ('HQ', ),  # level 1 -> 2
        ('HQ', "Camp", "Academy"),
        ('HQ', "Tavern", "Garage"),
        ('HQ', "WorkShop", "Weaponsmith"),
        ('HQ', "Mill", "Camp", "Academy"),
        ('HQ', "TransportStation", "Laboratory", "Tavern"),
        ('HQ', "Mill", "Camp", "WorkShop"),
        ('HQ', "TransportStation", "WorkShop", "Garage"),
        ('HQ', "Tavern", "Academy", "Weaponsmith"),
        ('HQ', "Mill", "Camp", "Weaponsmith"),  # level 10 -> 11
        ('HQ', "TransportStation", "Laboratory", "Tavern"),
        ('HQ', "Mill", "Camp", "WorkShop"),
        ('HQ', "TransportStation", "Weaponsmith", "Garage"),
        ('HQ', "Tavern", "Academy", "WorkShop"),
        ('HQ', "Mill", "Camp", "Weaponsmith"),
        ('HQ', "TransportStation", "Laboratory", "Tavern"),  # level 16 -> 17
        ('HQ', "Mill", "Camp", "WorkShop"),
        ('HQ', "TransportStation", "Weaponsmith", "Garage"),
        ('HQ', "Tavern", "Academy", "WorkShop"),
        ('HQ', "Tavern", "Academy", "WorkShop"),  # level 19 -> 20
        ('HQ', "Mill", "Weaponsmith", "Camp"),
        ('HQ', "TransportStation", "Laboratory", "Tavern"),
        ('HQ', "Camp", "Mill", "WorkShop"),
        ('HQ', "Weaponsmith", "TransportStation", "Garage"),
        ('HQ', "Tavern", "Academy", "WorkShop"),
        ('HQ', "Mill", "Weaponsmith", "Camp"),
        ('HQ', "TransportStation", "Laboratory", "Tavern"),
        ('HQ', "WorkShop", "TransportStation", "Garage"),
        ('HQ', "Camp", "Weaponsmith", "Laboratory"),
        ('HQ', "Academy", "TransportStation", "Mill"),
        ]
    """List the buildings needed for upgrading the HQ. Here requirements are stored as strings, you will probably
    be more interested in the attribute <upgrade_requirements> which is the same but with classes instead."""
    upgrade_requirements = None  # This attribute will be defined later, once other building classes will be initialized
    """List the buildings needed for upgrading the HQ. 
    upgrade_requirements[n] store the requirement for upgrading from level n+1 to n+2
    (Warning: be aware that this attribute is set to None, until 
    other buildings classes are defined, a.k.a after buildings/buildings.py is imported for the first time)"""

    @classmethod
    def _get_upgrade(cls, level: int):
        # Special case for the HQ which have multiple changing requirements

        assert 0 <= level < MAX_LEVEL, "Level should be in range [0;{}[, you can't upgrade from level {}".format(MAX_LEVEL, level)
        assert level < len(cls.upgrade_costs), "{} upgrade_costs attribute is not implemented for level {}".format(cls.__name__, level)
        assert level < len(cls.upgrade_requirements), "{} upgrade_requirements  is not implemented for level {}".format(cls.__name__, level)

        return Upgrade(cls.upgrade_costs[level], cls.upgrade_requirements[level])

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


# Now that HQ is initialized, set it as base_building in Building
Building.base_building = HQ

# Register all defined cards
BUILDINGS.register_cards_in_module(Building, __name__)
