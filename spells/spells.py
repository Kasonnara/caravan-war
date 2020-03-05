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
from common.cards import Card
from common.rarity import Rarity
from utils.class_property import classproperty


class Spell(Card):
    category = "Spells"

    def __init__(self, level: int):
        super().__init__(level)

    @classproperty
    def gem_cost(cls):
        return cls.rarity.spell_gem_cost

    @classmethod
    def gold_cost(cls, ligue: 'Ligue'):
        return cls.rarity.spell_gold_cost(ligue)


class Arrow(Spell):
    rarity = Rarity.Common


class Landmine(Spell):
    rarity = Rarity.Common


class Storm(Spell):
    rarity = Rarity.Epic


class Ice(Spell):
    rarity = Rarity.Epic


class Poison(Spell):
    rarity = Rarity.Rare


class Meteor(Spell):
    rarity = Rarity.Rare


class ConvoyBoost(Card):
    category = "ConvoyBoosts"


class AttackSpeedBoost(ConvoyBoost):
    boost = 8
    rarity = Rarity.Rare


class AttackBoost(ConvoyBoost):
    boost = 4
    rarity = Rarity.Common


class LifeBoost(ConvoyBoost):
    boost = 4
    rarity = Rarity.Common


class SpeedBoost(ConvoyBoost):
    boost = 8
    rarity = Rarity.Rare


class VehiculeBoost(ConvoyBoost):
    boost = 15
    rarity = Rarity.Epic


class ModuleBoost(ConvoyBoost):
    boost = 15
    rarity = Rarity.Epic
