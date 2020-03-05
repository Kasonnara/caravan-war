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
from common.cards import register_card_type


@register_card_type('Building')
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


@register_card_type('Building')
class TransportStation(Building):
    pass


@register_card_type('Building')
class Bank(Building):
    pass


@register_card_type('Building')
class Storage(Building):
    pass


@register_card_type('Building')
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


@register_card_type('Building')
class Tavern(Building):
    pass


@register_card_type('Building')
class Camp(Building):
    pass


@register_card_type('Building')
class Academy(Building):
    pass


@register_card_type('Building')
class Weaponsmith(Building):
    pass


@register_card_type('Building')
class Garage(Building):
    pass


@register_card_type('Building')
class WorkShop(Building):
    pass


@register_card_type('Building')
class Forge(Building):
    pass


@register_card_type('Building')
class HeroTemple(Building):
    pass


@register_card_type('Building')
class Altar(Building):
    pass
