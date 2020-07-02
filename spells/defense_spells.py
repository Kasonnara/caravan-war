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


from common.card_categories import CONVOY_BOOSTS
from common.rarity import Rarity
from spells.common_spell import Spell


class ConvoyBoost(Spell):
    def _effect_factor(self) -> float:
        assert self.level > 0, "Spell at level 0 aren't unlocked yet, you shouldn't need their _effect_factor yet"
        if self.rarity is Rarity.Common:
            return 1.038 + 0.002 * self.level
        elif self.rarity is Rarity.Rare:
            return 1.077 + 0.003 * self.level  # FIXME: expression is not exact at all levels
        elif self.rarity is Rarity.Epic:
            return 1.1 + 0.005 * self.level


class AttackSpeedBoost(ConvoyBoost):
    boost = 8
    rarity = Rarity.Rare
    # upgrade cost : 11->12=407000, 12->13=711000, 14=1255000
    # speed_factor lvl 13 = 11.6


class AttackBoost(ConvoyBoost):
    boost = 4
    rarity = Rarity.Common
    # atk_factor lvl 11=1.06, 12=1.065


class LifeBoost(ConvoyBoost):
    boost = 4
    rarity = Rarity.Common
    # life_factor lvl 11=1.06, 12=1.065


class SpeedBoost(ConvoyBoost):
    boost = 8
    rarity = Rarity.Rare
    # upgrade cost : 12->13=711000, 14=1255000
    # speed_factor lvl 13 = 11.6


class VehicleArmor(ConvoyBoost):
    boost = 15
    rarity = Rarity.Epic
    # hp_boost 11=1.2, 12=1.205


class ModuleBoost(ConvoyBoost):
    boost = 15
    rarity = Rarity.Epic
    # damage_boost 11=1.2, 12=1.205


# Register all defined cards
CONVOY_BOOSTS.register_cards_in_module(ConvoyBoost, __name__)
