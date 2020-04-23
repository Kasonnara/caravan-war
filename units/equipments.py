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

from buildings.buildings import Forge
from common.cards import Card


class Equipement(Card):
    base_building_level = Forge
    def __init__(self, level=1, effects: Tuple[object] = ()):
        self.effects = effects
        self.level = level

    @property
    def bonus_factor(self):
        return 0.05 * 1.15 ** (self.level-1)


class Weapon(Equipement):
    pass


class Armor(Equipement):
    pass

