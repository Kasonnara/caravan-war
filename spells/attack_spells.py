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
from common.card_categories import SPELLS
from common.rarity import Rarity
from common.target_types import TargetType
from spells.common_spell import Spell


class AmbushSpell(Spell):
    cooldown = None
    shoot_to = None
    cast_delay = 0
    alignment = Alignment.ATTACKER



class Arrow(AmbushSpell):
    rarity = Rarity.Common
    attack_base = 315
    radius = 4
    cooldown = 10
    cast_delay = 1
    shoot_to = TargetType.AIR_GROUND


class Landmine(AmbushSpell):
    rarity = Rarity.Common
    attack_base = 423
    cooldown = 12
    cast_delay = 4
    radius = 2
    shoot_to = TargetType.GROUND


class Storm(AmbushSpell):
    rarity = Rarity.Epic
    attack_base = 550
    cooldown = 40
    duration = 5
    stun_duration = 1
    shoot_to = TargetType.AIR_GROUND


class Ice(AmbushSpell):
    rarity = Rarity.Epic
    cooldown = 35
    shoot_to = TargetType.AIR_GROUND
    radius = 3
    def duration(self):
        if self.level <= 15:
            return 2.8 + 0.2 * self.level
        else:
            return 4.3 + 0.1 * self.level


class Poison(AmbushSpell):
    rarity = Rarity.Rare
    cooldown = 20
    shoot_to = TargetType.GROUND
    duration = 4
    radius = 3
    attack_base = 150


class Meteor(AmbushSpell):
    rarity = Rarity.Rare
    attack_base = 650
    radius = 3
    cast_delay = 0.5
    cooldown = 22
    shoot_to = TargetType.AIR_GROUND


# Register all defined cards
SPELLS.register_cards_in_module(AmbushSpell, __name__)
