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
from common.card_categories import HEROES
from common.target_types import TargetType
from units.base_units import MovableUnit


class Hero(MovableUnit):
    level_grow_factor = 1.018
    ultimate = False
    cost = 1


class HeroSpell:
    def __init__(self, level):
        assert 0 < level <= 5
        self.level = level


class Zora(Hero):
    hp_base = 18000
    attack_base = 3150

    hit_frequency = 0.7
    range = 10
    move_speed = 1.3
    armor = 0
    armor_piercing = 0
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND

    class IceArrow(HeroSpell):
        effect_radius = 5
        slow_factor = 0.5
        slow_duration = 3
        ultimate = True

        @property
        def damage_factor(self):
            return 1.5 + 0.5 * self.level

    class ArrowFlight(HeroSpell):
        arrow_number = 10
        effect_radius = 3
        hit_chance = 0.2

        @property
        def damage_factor(self):
            return 0.55 + 0.05 * self.level

    class FastHand(HeroSpell):
        @property
        def attack_speed_factor(self):
            return 15 + None * self.level

    class PiercingShot(HeroSpell):
        pass

    class BounceArrow(HeroSpell):
        pass

    def __init__(self, level: int, ice_arrow=1, arrow_flight=None, fast_hand=None, percing_shot=None, bounce_arrow=None):
        super().__init__(level, 0, None, None)
        self.spells = [
            self.IceArrow(ice_arrow),
            ]
        if arrow_flight is not None:
            self.spells.append(self.ArrowFlight(arrow_flight))
        if fast_hand is not None:
            self.spells.append(self.FastHand(fast_hand))
        if percing_shot is not None:
            self.spells.append(self.PiercingShot(percing_shot))
        if bounce_arrow is not None:
            self.spells.append(self.BounceArrow(bounce_arrow))


class Dalvir(Hero):
    hp_base = 27000
    attack_base = 2750

    hit_frequency = 0.5
    range = 1.5
    move_speed = 1.35
    armor = 2
    armor_piercing = 0
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND

    class WarriorRage(HeroSpell):
        aoe_lenght = 10
        stun_duration = 2
        ultimate = True
        _damage_factor = {1:80, 2:90, 3:100, 4:125, 5:150}

        @property
        def damage_factor(self):
            return self._damage_factor[self.level]

    class ButalShield(HeroSpell):
        damage_reduction = 0.85
        @property
        def armor_bonus(self):
            return 9 + self.level
        armor_bonus_duration = 5
        hit_chance = 0.15

    class StrongWill(HeroSpell):
        radius = 10
        heath_threshold = 0.5
        @property
        def armor_bonus(self):
            return 2 + self.level

    class KnightFury(HeroSpell):
        damage_reduction = 0.6
        attack_speed_factor = 2.5
        effect_duration = 7
        hit_chance = 0.1

    class IronProtection(HeroSpell):
        @property
        def hp_bonus(self):
            return 0.05 + None * self.level

    def __init__(self, level: int, warrior_rage=1, butal_shield=None, strong_will=None, knight_fury=None, iron_protection=None):
        super().__init__(level, 0, None, None)
        self.spells = [
            self.WarriorRage(warrior_rage),
            ]
        if butal_shield is not None:
            self.spells.append(self.ButalShield(butal_shield))
        if strong_will is not None:
            self.spells.append(self.StrongWill(strong_will))
        if knight_fury is not None:
            self.spells.append(self.KnightFury(knight_fury))
        if iron_protection is not None:
            self.spells.append(self.IronProtection(iron_protection))


# Register all defined cards
HEROES.register_cards_in_module(Hero, __name__)
