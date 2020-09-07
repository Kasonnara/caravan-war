#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This is a personal project to understand and improve my knowledge/tactics in the game Caravan War.
# Copyright (C) 2019  Kasonnara <wins@kasonnara.fr>
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
from common.alignment import TargetCategory, Alignment
from common.cards import Card
from common.rarity import Rarity
from common.resources import resourcepackets_gold
from utils.class_property import classproperty


class Spell(Card):
    # TODO move gem and gold cost from rarity class to unit class, refactor to store_gem/gold_cost and return ResQty

    apply_to: TargetCategory = Alignment.DEFENDER

    @classproperty
    def gem_cost(cls):
        return cls.rarity.spell_gem_cost

    @classmethod
    def gold_cost(cls, ligue: 'Ligue'):
        return cls.rarity.spell_gold_cost(ligue)

    _upgrade_costs = {
        Rarity.Common: resourcepackets_gold(
            0,  # 0 -> 1
            -70, -370, -1400, -4100, -10000,  # 1 -> 6
            -23000, -49000, -69000, -101000, -145000,  # 6 -> 11
            -271000, -474000, -836000, -1433000, -2489000,  # 11 -> 16
            -4419000, -7879000, -13880000, -24968000, -47859000,  # 16 -> 21
            -79797000, -136096000, -224435000, -374986000, -633839000,  # 21 -> 26
            -1068873000, -1648155000, -2308594000, -3235065000,
            ),
        Rarity.Rare: resourcepackets_gold(
            0,  # 0 -> 1
            -110, -550, -2100, -6200, -15000,  # 1 -> 6
            -35000, -74000, -104000, -152000, -218000,  # 6 -> 11
            -407000, -711000, -1255000, -2149000, -3734000,  # 11 -> 16
            -6629000, -11818000, -20820000, -37452000, -71788000,  # 16 -> 21
            -119696000, -204144000, -336653000, -562480000, -950759000,  # 21 -> 26
            -1603310000, -2472233000, -3462891000, -4852598000,
            ),
        Rarity.Epic: resourcepackets_gold(
            # TODO: Almost exactly equal to 2x common values. There is probably a formula to compute all this.
            0,  # 0 -> 1
            -140, -730, -2800, -8300, -20000,  # 1 -> 6
            -47000, -99000, -139000, -203000, -290000,  # 6 -> 11
            -542000, -948000, -1673000, -2865000, -4978000,  # 11 -> 16
            -8838000, -15757000, -27759000, -49935000, -95717000,  # 16 -> 21
            -159594000, -272191000, -448870000, -749973000, -1267678000,  # 21 -> 26
            -2137747000, -3296310000, -4167188000, -6470130000,
            ),
        }

    @classproperty
    def upgrade_costs(cls):
        return cls._upgrade_costs[cls.rarity]
