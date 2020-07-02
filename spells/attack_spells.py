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

from common.card_categories import SPELLS
from common.rarity import Rarity
from spells.common_spell import Spell


class AmbushSpell(Spell):
    pass


class Arrow(AmbushSpell):
    rarity = Rarity.Common


class Landmine(AmbushSpell):
    rarity = Rarity.Common


class Storm(AmbushSpell):
    rarity = Rarity.Epic


class Ice(AmbushSpell):
    rarity = Rarity.Epic


class Poison(AmbushSpell):
    rarity = Rarity.Rare


class Meteor(AmbushSpell):
    rarity = Rarity.Rare


# Register all defined cards
SPELLS.register_cards_in_module(AmbushSpell, __name__)
