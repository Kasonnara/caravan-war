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
from common.resources import Resources, ResourcePacket
from common.target_types import TargetType
from units.base_units import MovableUnit
from utils.class_property import classproperty


class Hero(MovableUnit):
    level_grow_factor = 1.018
    ultimate = False
    cost = 1
    soul_class: Resources = None
    sub_levels_per_level = 10

    _xp_costs = [0, -5, -6, -7, -8, -9, -10, -12, -13, -15,  # 0 -> 10
                 -17, -19, -20, -22, -25, -27, -30, -33, -36, -40,
                 -44, -49, -54, -60, -67, -74, -82, -91, -101, -113,
                 -126, -141, -158, -177, -199, -222, -249, -279, -312, -350,
                 -385, -423, -466, -512, -563, -620, -682, -750, -825, -907,
                 -953, -1000, -1050, -1103, -1158, -1216, -1277, -1341, -1408, -1478,
                 -1522, -1568, -1615, -1664, -1714, -1765, -1818, -1872, -1929, -1986,
                 ]
    # TODO: find a predictive formula for xp costs.  (e.g. experiments/hero_cp_formula.py)
    #      (This seems difficult: growth seems random at first due to round operation, then stabilize around
    #      x1.12 per lvl until lvl 40 where it drop to x1.1; then to 1.05 at lvl 50, and finally to 1.03 at lvl 60 ...)

    @classproperty
    def upgrade_costs(cls):
        # OPTIMIZE: if needed it is possible to save cpu in exhange of memory: As this function will always return the
        #  same results for one specific hero class (only hero soul type change), each hero class can cache the results.
        return [
            (ResourcePacket(Resources.HeroExperience(xp_cost)) if level % 10
             else ResourcePacket(Resources.HeroExperience(xp_cost),
                                 cls.soul_class(-30 if level == 0 else -5 * level//10))
             )
            for level, xp_cost in enumerate(cls._xp_costs)
            ]


class HeroSpell:
    def __init__(self, level):
        assert 0 <= level <= 5
        self.level = level

    upgrade_costs = [ResourcePacket(Resources.CapacityToken(-c)) for c in range(1, 5)]


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

    soul_class = Resources.ZoraSoul

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

    def __init__(self, level: int, ice_arrow=1, arrow_flight=0, fast_hand=0, piercing_shot=0, bounce_arrow=0):
        super().__init__(level, 0, None, None)
        self.spells = [
            self.IceArrow(ice_arrow),
            self.ArrowFlight(arrow_flight),
            self.FastHand(fast_hand),
            self.PiercingShot(piercing_shot),
            self.BounceArrow(bounce_arrow),
            ]


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

    soul_class = Resources.DalvirSoul

    class WarriorRage(HeroSpell):
        aoe_lenght = 10
        stun_duration = 2
        ultimate = True
        _damage_factor = {1: 80, 2: 90, 3: 100, 4: 125, 5: 150}

        @property
        def damage_factor(self):
            return self._damage_factor[self.level]

    class BrutalShield(HeroSpell):
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

    def __init__(self, level: int, warrior_rage=1, brutal_shield=0, strong_will=0, knight_fury=0, iron_protection=0):
        super().__init__(level, 0, None, None)
        self.spells = [
            self.WarriorRage(warrior_rage),
            self.BrutalShield(brutal_shield),
            self.StrongWill(strong_will),
            self.KnightFury(knight_fury),
            self.IronProtection(iron_protection),
            ]


# Register all defined cards
HEROES.register_cards_in_module(Hero, __name__)
