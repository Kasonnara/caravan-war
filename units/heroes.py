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

from typing import Type

from buildings.buildings import HeroTemple
from common.card_categories import HEROES
from common.resources import Resources, ResourcePacket
from common.target_types import TargetType
from units.base_units import MovableUnit
from utils.class_property import classproperty


class Hero(MovableUnit):
    base_building = HeroTemple
    LEVEL_GROW_FACTOR = 1.018
    ultimate = False
    cost = 1
    soul_class: Resources = None
    sub_levels_per_level = 10

    _xp_costs = [0, -5, -6, -7, -8, -9, -10, -12, -13, -15,  # 0 -> 10
                 -17, -19, -20, -22, -25, -27, -30, -33, -36, -40,  # 10 -> 20
                 -44, -49, -54, -60, -67, -74, -82, -91, -101, -113,  # 20 -> 30
                 -126, -141, -158, -177, -199, -222, -249, -279, -312, -350,  # 30 -> 40
                 -385, -423, -466, -512, -563, -620, -682, -750, -825, -907,  # 40 -> 50
                 -953, -1000, -1050, -1103, -1158, -1216, -1277, -1341, -1408, -1478,  # 50 -> 60
                 -1522, -1568, -1615, -1664, -1714, -1765, -1818, -1872, -1929, -1986,  # 60 -> 70
                 -2036, -2087, -2139, -2193, -2248, -2304, -2361, -2420, -2481, -2543,  # 70 -> 80
                 -2594, -2646, -2698, -2752, -2808, -2864, -2921, -2979, -3039, -3100,  # 80 -> 90
                 -3146, -3193, -3241, -3290, -3339, -3389, -3440, -3492, -3544, -3597,  # 90 -> 100
                 -3633, -3670, -3706, -3743, -3781, -3819, -3857, -3895, -3934, -3974,  # 100 -> 110
                 -4033, -4094, -4155, -4218, -4281, -4345, -4410, -4476, -4544, -4612,  # 110 -> 120
                 -4681, -4751, -4822, -4895, -4968, -5043, -5118, -5195, -5273, -5352,  # 120 -> 130
                 -5432, -5514, -5596, -5680, -5766, -5852, -5940, -6029, -6119, -6211,  # 130 -> 140
                 -6304, -6399, -6495, -6592, -6691, -6792, -6893, -6997, -7102, -7208,  # 140 -> 150
                 -7317, -7426, -7538, -7651, -7765, -7882, -8000, -8120, -8242, -8366,  # 150 -> 160
                 -8491, -8618, -8748, -8879, -9012, -9147, -9285, -9424, -9565, -9709,  # 160 -> 170
                 -9854, -10002, -10152, -10304, -10459, -10616, -10775, -10937, -11101, -11267,  # 170 -> 180
                 -11436, -11608, -11782, -11959, -12138, -12320, -12505, -12693, -12883, -13076,  # 180 -> 190
                 -13272, -13471, -13673, -13879, -14087, -14298, -14512, -14730, -14951, -15175,  # 190 -> 200
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

    ultimate = False
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
        hit_chance = None

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
        @property
        def damage_factor(self):
            return 1. + 0.25 * self.level

    class BounceArrow(HeroSpell):
        bouce_range = 6
        @property
        def bouce_hit_chance(self):
            return 0.1 + 0.05*self.level

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
        attack_speed_factor = [1.5, 1.75, 2., 2.25, 2.5]  # TODO test if it is x150% or +150%
        effect_duration = 7
        hit_chance = 0.1

    class IronProtection(HeroSpell):
        @property
        def hp_bonus(self):
            return 0.05 * self.level

    def __init__(self, level: int, warrior_rage=1, brutal_shield=0, strong_will=0, knight_fury=0, iron_protection=0):
        super().__init__(level, 0, None, None)
        self.spells = [
            self.WarriorRage(warrior_rage),
            self.BrutalShield(brutal_shield),
            self.StrongWill(strong_will),
            self.KnightFury(knight_fury),
            self.IronProtection(iron_protection),
            ]


class Ghohral(Hero):
    hp_base = 15000
    # level 21 à 30: 21432, 21818, 22211, 22611, 23018, 23432, 23854, 24283, 24720, 25165;
    attack_base = 2500
    # level 21 à 30: 3573, 3637, 3702, 3769, 3837, 3906, 3976, 4048, 4121, 4195;

    hit_frequency = 0.5
    range = 1.5
    move_speed = 1.3
    armor = 3
    armor_piercing = 0
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND

    soul_class = Resources.GhohralSoul

    class Warlord(HeroSpell):
        ultimate = True
        summon_number = [3, 3, 4, 4, 5]
        summon_time = 23
        #summon_hp_base = hp_base * 0.2

    class Lacerate(HeroSpell):
        attack_number = 3
        hit_chance = 0.4

    class Duelist(HeroSpell):
        max_combo_factor = 3.
        combo_time = 5

    class Exemplary(HeroSpell):
        damage_factor = [2 + 0.1 * i for i in range(5)]
        duration = 10
        hit_chance = 0.1
        radius = 6

    class BruteForce(HeroSpell):
        target_number = 3
        radius = 4
        stun_duration = 1
        hit_chance = 0.3

    def __init__(self, level: int, warlord=1, lacerate=0, duelist=0, exemplary=0, brute_force=0):
        super().__init__(level, 0, None, None)
        self.spells = [
            self.Warlord(warlord),
            self.Lacerate(lacerate),
            self.Duelist(duelist),
            self.Exemplary(exemplary),
            self.BruteForce(brute_force),
            ]

class Ailul(Hero):
    hp_base = 15000
    # level 10 à 40: 17613; 17930, 18253, 18582, 18916, 19256, 19603, 19956, 20315, 20681, 21053; 21432, 21818, 22211, 22611, 23018, 23432, 23854, 24283, 24720, 25165; 25618, 26079, 26548, 27026, 27512, 28007, 28511, 29024, 29546, 30078;
    # level 41 à 50: 30619, 31170, 31731, 32302, 32883, 33475, 34078, 34691, 35315, 35951;
    attack_base = 2000
    # level 10 à 40: 2349; 2391, 2434, 2478, 2523, 2568, 2614, 2661, 2709, 2758, 2808; 2859, 2910, 2962, 3015, 3069, 3124, 3180, 3237, 3295, 3354; 3414, 3475, 3538, 3602, 3667, 3733, 3800, 3868, 3938, 4009;
    # level 41 à 50: 4081, 4154, 4229, 4305, 4383, 4462, 4542, 4624, 4707, 4792;

    hit_frequency = 0.4
    range = 8
    move_speed = 1.3
    armor = 2
    armor_piercing = 0
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND

    soul_class = Resources.AilulSoul

    class Explosion(HeroSpell):
        ultimate = True
        radius = 10

        @property
        def damage_heal_factor(self):
            return 1.10 + 0.15*self.level

    class FrozenLightning(HeroSpell):
        # AOE?
        hit_chance = 0.2
        slowness_factor = 0.2
        slowness_duration = 3
        @property
        def damage_factor(self):
            return 1.25 + 0.25 * self.level

    class Rejuvenation(HeroSpell):
        @property
        def auto_heal_factor(self):
            return 0.0025 * (self.level + 1)

    class IceAmore(HeroSpell):
        target_number = 5  # here targets are ally
        radius = 10
        @property
        def armor_factor(self):
            return 0.5 * (self.level + 1)
        armor_duration = 10
        hit_chance = 0.1

    class Regeneration(HeroSpell):
        target_number = 3
        radius = 5
        @property
        def heal_factor(self):
            return 0.03 + 0.005 * self.level
        duration = 10
        hit_chance = 0.3

    def __init__(self, level: int, explosion=1, frozen_lightning=0, rejuvenation=0, ice_armor=0, regeneration=0):
        super().__init__(level, 0, None, None)
        self.spells = [
            self.Explosion(explosion),
            self.FrozenLightning(frozen_lightning),
            self.Rejuvenation(rejuvenation),
            self.IceAmore(ice_armor),
            self.Regeneration(regeneration),
            ]


class Mardon(Hero):
    hp_base = 17000
    # level 1 à 10 : 17000, 17306, 17618, 17935, 18258, 18587, 18922, 19263, 19610, 19963;
    # level 11 à 20; 20322, 20688, 21060, 21439, 21825, 22218, 22618, 23025, 23439, 23861;
    # level 21 à 30: 24290, 24727, 25172, 25625, 26086, 26556, 27034, 27521, 28016, 28520;
    # level 31 à 40: 29033, 29556, 30088, 30630, 31181, 31742, 32313, 32895, 33487, 34090;
    # level 41 à 50: 34704, 35329, 35965, 36612, 37271, 37942, 38625, 39320, 40028, 40748;
    # level 51 à 60: 41481, 42228, 42988, 43762, 44550, 45352, 46168, 46999, 47845, 48706;
    # level 61 à 70: 49583, 50475, 51384, 52309, , , , , , ;
    attack_base = 2350
    # level 1 à 10 : 2350, 2392, 2435, 2479, 2524, 2569, 2615, 2662, 2710, 2759;
    # level 11 à 20; 2809, 2860, 2911, 2963, 3016, 3070, 3125, 3181, 3238, 3296;
    # level 21 à 30: 3355, 3415, 3477, 3540, 3604, 3669, 3735, 3802, 3870, 3940;
    # level 31 à 40: 4011, 4083, 4157, 4232, 4308, 4386, 4465, 4545, 4627, 4710;
    # level 41 à 50: 4795, 4881, 4969, 5058, 5149, 5242, 5336, 5432, 5530, 5630;
    # level 51 à 60: 5731, 5834, 5939, 6046, 6155, 6266, 6379, 6494, 6611, 6730;
    # level 61 à 70: 6851, 6974, 7100, 7228, , , , , , ;

    # level 21 à 30: , , , , , , , , , ;

    hit_frequency = 0.6
    range = 8
    move_speed = 1.3
    armor = 0
    armor_piercing = 0
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND

    soul_class = Resources.MardonSoul

    class Nova(HeroSpell):
        ultimate = True
        damage_factor_range = [(1., 2. + 0.5 * level) for level in range(5)]
        radius_range = (5, 20)
        load_max_duration = 4

    class SparseFlames(HeroSpell):
        damage_factor = [1.4 + 0.1 * level for level in range(5)]
        sub_projectil_num = 2
        sub_projectil_damage_factor = [0.5 + 0.1 * level for level in range(5)]
        hit_chance = 0.2

    class FireArmor(HeroSpell):
        damage_reduction_factor = [0.05 + 0.05 * level for level in range(5)]   # TODO: test if this spell reduce taken damages or inflict backfire damage
        melee_damage_mirror_factor = 0.25

    class FirePit(HeroSpell):
        radius = 3
        inital_damage_factor = [0.4 + 0.1 * level for level in range(5)]
        duration = 10
        enter_damage_factor = 0.3
        hit_chance = 0.1

    class FieryUnction(HeroSpell):
        duration = 10
        atk_boost_factor, atk_speed_boost_factor = ([0.25 + 0.05 * level for level in range(5)],) * 2
        aoe_radius = 3
        aoe_dmg_factor = 0.2
        hit_chance = 0.3

    def __init__(self, level: int, nova=1, sparse_flames=0, fire_armor=0, fire_pit=0, fiery_unction=0):
        super().__init__(level, 0, None, None)
        self.spells = [
            self.Nova(nova),
            self.SparseFlames(sparse_flames),
            self.FireArmor(fire_armor),
            self.FirePit(fire_pit),
            self.FieryUnction(fiery_unction),
            ]


# Register all defined cards
HEROES.register_cards_in_module(Hero, __name__)
