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

from common.cards import Card
from common.rarity import Rarity
from common.resources import resourcepackets_gold
from utils.class_property import classproperty


class AbstractSpell(Card):
    # TODO move gem and gold cost from rarity class to unit class, refactor to store_gem/gold_cost and return ResQty
    @classproperty
    def gem_cost(cls):
        return cls.rarity.spell_gem_cost

    @classmethod
    def gold_cost(cls, ligue: 'Ligue'):
        return cls.rarity.spell_gold_cost(ligue)

    _upgrade_costs = {
        Rarity.Common: resourcepackets_gold(
            0,  # 0 -> 1
            None, None, None, None, None,  # 1 -> 6
            None, None, None, None, None,  # 6 -> 11
            -271000, -474000, -836000, -1433000, -2489000,  # 11 -> 16
            -4419000,
            ),
        Rarity.Rare: resourcepackets_gold(
            0,  # 0 -> 1
            None, None, None, None, None,  # 1 -> 6
            None, None, None, None, None,  # 6 -> 11
            -407000, -711000, -1255000, -2149000, -3734000,  # 11 -> 16
            -4429000,
            ),
        Rarity.Epic: resourcepackets_gold(
            0,  # 0 -> 1
            None, None, None, None, None,  # 1 -> 6
            None, None, None, None, None,  # 6 -> 11
            -542000, -948000, -1673000, -2865000, -4978000,  # 11 -> 16
            -8838000,
            )
        }

    @classproperty
    def upgrade_costs(cls):
        return cls._upgrade_costs[cls.rarity]
