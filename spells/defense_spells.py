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


from common.alignment import Alignment
from common.card_categories import CONVOY_BOOSTS
from common.rarity import Rarity
from spells.common_spell import Spell
from units.vehicles import Vehicle
from units.modules import ModuleWeapon


class ConvoyBoost(Spell):
    alignment = Alignment.DEFENDER
    def _effect_factor(self) -> float:
        assert self.level > 0, "Spell at level 0 aren't unlocked yet, you shouldn't need their _effect_factor yet"

        if self.rarity is Rarity.Common:
            return 1.038 + 0.002 * self.level
        elif self.rarity is Rarity.Rare:
            if self.level <= 15:
                return 1.077 + 0.003 * self.level
            else:
                return 1.092 + 0.002 * self.level
        elif self.rarity is Rarity.Epic:
            if self.level <= 15:
                return 1.1 + 0.005 * self.level
            else:
                return 1.175 + 0.003 * self.level


class AttackSpeedBoost(ConvoyBoost):
    rarity = Rarity.Rare


class AttackBoost(ConvoyBoost):
    rarity = Rarity.Common


class LifeBoost(ConvoyBoost):
    rarity = Rarity.Common


class SpeedBoost(ConvoyBoost):
    rarity = Rarity.Rare


class VehicleArmor(ConvoyBoost):
    rarity = Rarity.Epic
    apply_to = Vehicle


class ModuleBoost(ConvoyBoost):
    rarity = Rarity.Epic
    apply_to = ModuleWeapon


# Register all defined cards
CONVOY_BOOSTS.register_cards_in_module(ConvoyBoost, __name__)
