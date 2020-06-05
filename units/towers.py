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

from typing import Union, List, Optional

from buildings.buildings import WorkShop
from common.card_categories import TOWERS
from common.resources import resourcepackets_gold
from units.heroes import Hero
from utils.class_property import classproperty
from common.target_types import TargetType
from units.base_units import BaseUnit, AOE, Heal, MovableUnit, FakeMovableUnit


class Tower(BaseUnit):
    base_building = WorkShop
    parent_tower = None
    _cost = None

    @classproperty
    def cost(cls):
        # FIXME: possible infinite recursive loop
        if cls._cost is None:
            return None
        if cls.parent_tower is None:
            return cls._cost
        else:
            assert issubclass(cls.parent_tower, Tower), "Parent ({}) is not a Tower".format(cls.parent_tower)
            return cls._cost + cls.parent_tower.cost

    @classproperty
    def gem_cost(cls):
        return cls.rarity.spell_gem_cost

    @classmethod
    def gold_cost(cls, ligue: 'Ligue'):
        return cls.rarity.spell_gold_cost(ligue)


class Sentinelle(Tower):
    attack_base = 72
    hit_frequency = 1.6
    range = 9
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = 150
    parent_tower = None
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -240, -1300, -6000, -14000, -30000,  # 1 -> 6
        -68000, -144000, -202000, -300000, -430000,  # 6 -> 11
        -800000, -1400000, -2470000, -4230000, -7360000,  # 11 -> 16
        -13060000, -23290000, -41020000, -73800000, -141450000,  # 16 -> 21
        -235850000, -402250000, -663350000, -1108330000, -1873420000,  # 21 -> 26
        -3159230000, -4871390000, -6823430000, -9561770000,
        )


class Arbalete(Tower):
    attack_base = 100
    hit_frequency = 1.6
    range = 11
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = 160
    parent_tower = Sentinelle
    multiple_target_limit = 2
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -470, -2700, -12100, -27000, -59000,  # 1 -> 6
        -136000, -287000, -404000, -590000, -860000,  # 6 -> 11
        -1600000, -2800000, -4940000, -8470000, -14710000,  # 11 -> 16
        -26120000, -46570000, -82050000, -147590000, -282910000,  # 16 -> 21
        -471710000, -804510000, -1326710000, -2216670000, -3746830000,  # 21 -> 26
        -6318460000, -9742790000, -13646860000, -19123540000,
        )


class Eolance(Tower):
    attack_base = 535
    hit_frequency = 0.6
    range = 11
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = 150
    parent_tower = Arbalete
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -520, -2900, -13300, -30000, -65000,  # 1 -> 6
        -150000, -316000, -444000, -650000, -940000,  # 6 -> 11
        -1760000, -3080000, -5440000, -9320000, -16180000,  # 11 -> 16
        -28730000, -51230000, -90250000, -162350000, -311200000,  # 16 -> 21
        -518880000, -884960000, -1459380000, -2438330000, -4121510000,  # 21 -> 26
        -6950310000, -10717070000, -15011550000, -21035890000,
        )


class Sniper(Tower):
    attack_base = 330
    hit_frequency = 0.5
    range = 13
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = 160
    parent_tower = Sentinelle
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -570, -3200, -14500, -33000, -71000,  # 1 -> 6
        -163000, -345000, -485000, -710000, -1030000,  # 6 -> 11
        -1920000, -3360000, -5930000, -10160000, -17660000,  # 11 -> 16
        -31350000, -55890000, -98460000, -177110000, -339490000,  # 16 -> 21
        -566050000, -965410000, -1592050000, -2660000000, -4496200000,  # 21 -> 26
        -7582160000, -11691350000, -16376230000, -22948240000,
        )


class HeavySniper(Tower):
    attack_base = 200
    hit_frequency = 1.5
    range = 13
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = 150
    parent_tower = Sniper
    tower_power_reward = (20, 20, 35, 50)
    # TODO special effect
    upgrade_costs = Sniper.upgrade_costs[:25] + resourcepackets_gold(
        -3746830000,  # 25 -> 26
        -6318460000, -9742790000, -13646860000, -19123540000,
        )
    # damage, with 4 stars [240, 276, 318, 366, 421, 483, 555, 638, 734, 844, 972, 1117]


class Mage(Tower):
    attack_base = 85
    hit_frequency = 1.2
    range = 8
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 6
    _cost = 150
    parent_tower = None
    upgrade_costs = Sentinelle.upgrade_costs  # basic towers seems to have the same upgrade costs


class Lightning(Tower):
    attack_base = 137
    hit_frequency = 0.8
    range = 8
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 6
    _cost = 175
    parent_tower = Mage
    multiple_target_limit = 8
    upgrade_costs = Sniper.upgrade_costs

    def damage_formule(self, target: MovableUnit, target_index=0, hit_combo=0):
        return (
            super().damage_formule(target, target_index=target_index)
            * (0.25 * max(0, 4 - target_index))  # Reduction factor
            )


class Stormspire(Tower, AOE):
    attack_base = 0
    hit_frequency = 0.25
    range = 3.5
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 6
    _cost = 200
    parent_tower = Lightning
    _log_once = False
    # TODO special effects
    stun_duration = 1
    stun_radius = 4
    stun_frequency=0.2
    upgrade_costs = Sentinelle.upgrade_costs

    def damage_formule(self, target: MovableUnit, target_index=0, hit_combo=0):
        # return super().damage_formule(target, target_index, hit_combo)
        if isinstance(target, Hero):
            return target.hp * 0.625  # TODO test if level difference impact damage on hero, and how
        if isinstance(target, FakeMovableUnit):
            if not type(self)._log_once:
                type(self)._log_once = True
                print("Stormspire can only be evaluated against a real unit")
            return 0
        return target.hp * (0.125 - 0.0125 * max(0, target.level - self.level))  # TODO test if it's -1.25% linear or exponential (by default I assumed it linear here )


class Fire(Tower):
    attack_base = 130
    hit_frequency = 2
    range = 8
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 2
    _cost = 160
    parent_tower = Mage
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -610, -3500, -15700, -35000, -77000,  # 1 -> 6
        -177000, -374000, -525000, -770000, -990000,  # 6 -> 11
        -1840000, -3220000, -5690000, -9740000, -16920000,  # 11 -> 16
        -30040000, -53560000, -94350000, -169730000, -325340000,  # 16 -> 21
        -542460000, -925180000, -1525720000, -2549170000, -4308860000,  # 21 -> 26
        -7266230000, -11204210000, -15693890000, -21992070000,
        )


class Bomber(AOE, Tower):
    attack_base = 88
    hit_frequency = 0.4
    range = 10
    shoot_to = TargetType.GROUND
    armor_piercing = 0
    _cost = 170
    parent_tower = None
    aoe_radius = 2
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -280, -1600, -7200, -16000, -36000,  # 1 -> 6
        -82000, -172000, -242000, -350000, -510000,  # 6 -> 11
        -960000, -1680000, -2970000, -5080000, -8830000,  # 11 -> 16
        -15670000, -27940000, -49230000, -88560000, -169750000,  # 16 -> 21
        -283020000, -482700000, -796030000, -1330000000, -2248100000,  # 21 -> 26
        -3791080000, -5845670000, -8188120000, -11474120000,
        )


class Canon(Tower):
    attack_base = 184
    hit_frequency = 0.5
    range = 10
    shoot_to = TargetType.GROUND
    armor_piercing = 0
    _cost = 120
    parent_tower = Bomber
    multiple_target_limit = 3
    upgrade_costs = Eolance.upgrade_costs


class Hydra(Tower):
    attack_base = 200
    hit_frequency = 1
    range = 150
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = 280
    parent_tower = Canon
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -610, -3500, -15700, -35000, -77000,  # 1 -> 6
        -177000, -374000, -525000, -770000, -1110000,  # 6 -> 11
        -2080000, -3640000, -6430000, -11010000, -19130000,  # 11 -> 16
        -33960000, -60550000, -106660000, -191870000, -367780000,  # 16 -> 21
        -613220000, -1045860000, -1724720000, -2881670000, -4870880000,  # 21 -> 26
        -8214000000, -12665620000, -17740920000, -24860600000,
        )


class MissileLaucher(AOE, Tower):
    attack_base = 240
    hit_frequency = 0.8
    range = 12
    shoot_to = TargetType.AIR
    armor_piercing = 0
    _cost = 80
    parent_tower = Bomber
    aoe_radius = 2
    upgrade_costs = Arbalete.upgrade_costs


class Hospital(AOE, Heal, Tower):
    base_heal = 20
    heal_frequency = 1
    range = None
    shoot_to = TargetType.AIR_GROUND
    _cost = 120
    parent_tower = None
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -190, -1100, -4800, -11000, -24000,  # 1 -> 6
        -54000, -115000, -162000, -240000, -340000,  # 6 -> 11
        -640000, -1120000, -1980000, -3390000, -5890000,  # 11 -> 16
        -10450000, -18630000, -32820000, -59040000, -113160000,  # 16 -> 21
        -188680000, -321800000, -530680000, -886670000, -1498430000,  # 21 -> 26
        -2527390000, -3897120000, -5458740000, -7649410000,
        )

    def dps(self, targets: Union[MovableUnit, List[MovableUnit]]) -> Optional[float]:
        return None


class Armory(Hospital):
    _cost = 80
    parent_tower = Hospital
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -350, -2000, -9100, -20000, -44000,  # 1 -> 6
        -102000, -216000, -303000, -440000, -640000,  # 6 -> 11
        -1200000, -2100000, -3710000, -6350000, -11030000,  # 11 -> 16
        -19590000, -34930000, -61540000, -110690000, -212180000,  # 16 -> 21
        -353780000, -603380000, -995030000, -1662500000, -2810120000,  # 21 -> 26
        -4738850000, -7307090000, -10235150000, -14342650000,
        )


class Tambour(Hospital):
    _cost = 130
    parent_tower = Hospital
    upgrade_costs = Armory.upgrade_costs


class Garnison(Tambour, Armory):
    _cost = 190
    parent_tower = Armory
    upgrade_costs = Arbalete.upgrade_costs


# Register all defined cards
TOWERS.register_cards_in_module(Tower, __name__)
