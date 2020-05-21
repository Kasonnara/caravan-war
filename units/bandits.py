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

from buildings.buildings import Camp
from common.card_categories import BANDITS
from common.rarity import Rarity
from common.resources import resourcepackets_gold
from units.base_units import MovableUnit, AOE, reincarnation
from common.target_types import TargetType
from units.vehicles import Vehicle


class Bandit(MovableUnit):
    base_building = Camp


class Maraudeur(Bandit):
    hp_base = 451
    attack_base = 120
    hit_frequency = 0.4
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 2
    armor_piercing = 0
    cost = 3
    move_speed = 1.7
    rarity = Rarity.Common
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -210, -1100, -4000, -9000, -25000,  # 1 -> 6
        -56000, -119000, -168000, -250000, -350000,  # 6 -> 11
        -660000, -1150000, -2020000, -3470000, -6020000,  # 11 -> 16
        -10690000, -19060000, -33580000, -60410000, -115790000,  # 16 -> 21
        -193060000, -329260000, -542990000, -907230000, -1533480000,  # 21 -> 26
        -2585980000, -3987470000, -5585310000, -7826770000,
        )


class Archer(Bandit):
    hp_base = 300
    attack_base = 71
    hit_frequency = 1
    range = 8
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 3
    move_speed = 1.7
    rarity = Rarity.Common
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -250, -1300, -4800, -11000, -30000,  # 1 -> 6
        -68000, -143000, -201000, -290000, -420000,  # 6 -> 11
        -790000, -1380000, -2430000, -4160000, -7230000,  # 11 -> 16
        -12830000, -22870000, -40300000, -72490000, -138940000,  # 16 -> 21
        -231670000, -395120000, -651590000, -1088670000, -1840180000,  # 21 -> 26
        -3103180000, -4784970000, -6702370000, -9392120000,
        )


class Drone(Bandit):
    hp_base = 500
    attack_base = 95
    hit_frequency = 0.75
    range = 3
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.AIR
    armor = 0
    armor_piercing = 0
    cost = 3
    move_speed = 2
    rarity = Rarity.Common
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -270, -1400, -5200, -12000, -32000,  # 1 -> 6
        -73000, -155000, -218000, -320000, -460000,  # 6 -> 11
        -850000, -1490000, -2630000, -4510000, -7830000,  # 11 -> 16
        -13900000, -24780000, -43650000, -78530000, -150520000,  # 16 -> 21
        -250970000, -428040000, -705880000, -1179390000, -1993530000,  # 21 -> 26
        -3361780000, -5183710000, -7260900000, -10174800000,
        )


class Brute(Bandit):
    hp_base = 1125
    attack_base = 130
    hit_frequency = 0.5
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 4
    move_speed = 1.6
    rarity = Rarity.Rare
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -360, -1800, -6800, -15000, -42000,  # 1 -> 6
        -96000, -203000, -285000, -420000, -600000,  # 6 -> 11
        -1110000, -1950000, -3440000, -5890000, -10240000,  # 11 -> 16
        -18170000, -32400000, -57090000, -102690000, -196840000,  # 16 -> 21
        -328200000, -559750000, -923080000, -1542280000, -2606920000,  # 21 -> 26
        -4396170000, -6778700000, -9495020000, -13305510000,
        )


class Lutin(Bandit):
    hp_base = 650
    attack_base = 110
    hit_frequency = 0.8
    range = 4
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.AIR
    armor = 0
    armor_piercing = 0
    cost = 6
    move_speed = 1.9
    rarity = Rarity.Rare
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -400, -2000, -7600, -17000, -47000,  # 1 -> 6
        -107000, -227000, -319000, -470000, -670000,  # 6 -> 11
        -1250000, -2180000, -3840000, -6590000, -11440000,  # 11 -> 16
        -20310000, -36220000, -63800000, -114770000, -220000000,  # 16 -> 21
        -366810000, -625600000, -1031680000, -1723730000, -2913610000,  # 21 -> 26
        -4913370000, -7576200000, -10612090000, -14870860000,
        )


class Berserk(Bandit):
    hp_base = 960
    attack_base = 150
    hit_frequency = 0.6
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 4
    armor_piercing = 0
    cost = 4
    move_speed = 1.8
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -380, -1900, -7200, -16000, -44000,  # 1 -> 6
        -102000, -215000, -302000, -440000, -630000,  # 6 -> 11
        -1180000, -2060000, -3640000, -6240000, -10840000,  # 11 -> 16
        -19240000, -34310000, -60440000, -108730000, -208420000,  # 16 -> 21
        -347500000, -592670000, -977380000, -1633010000, -2760270000,  # 21 -> 26
        -4654770000, -7177450000, -10053550000, -14088190000,
        )


class Hunter(Bandit):
    hp_base = 500
    attack_base = 122
    hit_frequency = 0.6
    range = 9
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 3
    cost = 4
    move_speed = 1.5
    rarity = Rarity.Rare
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -420, -2100, -8000, -18000, -49000,  # 1 -> 6
        -113000, -239000, -335000, -490000, -700000,  # 6 -> 11
        -1310000, -2290000, -4050000, -6930000, -12040000,  # 11 -> 16
        -21380000, -38120000, -67160000, -120810000, -231570000,  # 16 -> 21
        -386110000, -658530000, -1085980000, -1841450000, -3066960000,  # 21 -> 26
        -5171970000, -7974940000, -11170620000, -15653540000,
        )


class Spider(AOE, Bandit):
    hp_base = 1140
    attack_base = 110
    hit_frequency = 0.35
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 4
    move_speed = 1.4
    rarity = Rarity.Rare
    upgrade_costs = Lutin.upgrade_costs


class Alchimist(AOE, Bandit):
    hp_base = 482
    attack_base = 140
    hit_frequency = 0.4
    range = 4
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 5
    move_speed = 1.6
    rarity = Rarity.Rare
    upgrade_costs = Hunter.upgrade_costs


class Viking(Bandit):
    hp_base = 1900
    attack_base = 200
    hit_frequency = 1
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 6
    armor_piercing = 2
    cost = 8
    move_speed = 1.9
    consecutive_hit_attack_boost = 0.4
    max_consecutive_boost = 3.
    rarity = Rarity.Epic
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -590, -3000, -11200, -25000, -69000,  # 1 -> 6
        -158000, -334000, -470000, -690000, -980000,  # 6 -> 11
        -1840000, -3210000, -5670000, -9710000, -16860000,  # 11 -> 16
        -29940000, -53370000, -94020000, -169140000, -324200000,  # 16 -> 21
        -540560000, -921940000, -1520370000, -2540230000, -4293750000,  # 21 -> 26
        -7240750000, -11164920000, -15638860000, -21914960000,
        )


@reincarnation
class VikingLeg(Viking):
    hit_frequency = 1.25
    # FIXME: viking combo doesn't behave like other combo


class Momie(Bandit):
    hp_base = 1400
    attack_base = 240
    hit_frequency = 0.6
    range = 7
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 7
    move_speed = 1.4
    rarity = Rarity.Epic
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -560, -2900, -10800, -24000, -66000,  # 1 -> 6
        -152000, -322000, -453000, -660000, -950000,  # 6 -> 11
        -1770000, -3100000, -5460000, -9360000, -16260000,  # 11 -> 16
        -28870000, -51470000, -90670000, -163100000, -312630000,  # 16 -> 21
        -521250000, -889010000, -1466070000, -2449510000, -4140400000,  # 21 -> 26
        -6982160000, -10766170000, -15080330000, -21132280000,
        )


@reincarnation
class MomieLeg(Momie):
    pass


class DarkKnight(Bandit):
    hp_base = 1677
    attack_base = 394
    hit_frequency = 0.8
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 6
    armor_piercing = 0
    cost = 8
    move_speed = 1.9
    rarity = Rarity.Epic
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -620, -3100, -11600, -26000, -71000,  # 1 -> 6
        -164000, -346000, -486000, -710000, -1020000,  # 6 -> 11
        -1900000, -3330000, -5870000, -10050000, -17460000,  # 11 -> 16
        -31000000, -55280000, -97380000, -175180000, -335780000,  # 16 -> 21
        -559870000, -954860000, -1574660000, -2630950000, -4447100000,  # 21 -> 26
        -7499350000, -11563670000, -16197390000, -22697630000,
        )


@reincarnation
class DarkKnightLeg(DarkKnight):
    stun_duration = 2.5


class Condor(Bandit):
    hp_base = 1469
    attack_base = 260
    hit_frequency = 0.7
    range = 8
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.AIR
    armor = 0
    armor_piercing = 0
    cost = 8
    move_speed = 1.7
    armor_reduction = 5
    spell_duration = 60
    rarity = Rarity.Epic
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -630, -3200, -12000, -27000, -74000,  # 1 -> 6
        -164000, -358000, -503000, -740000, -1050000,  # 6 -> 11
        -1970000, -3440000, -6070000, -10400000, -18070000,  # 11 -> 16
        -32070000, -57180000, -100740000, -181220000, -347360000,  # 16 -> 21
        -579170000, -987790000, -1628960000, -2721680000, -4600440000,  # 21 -> 26
        -7757950000, -11962420000, -16755920000, -23480310000,
        )


@reincarnation
class CondorLeg(Condor):
    armor_reduction = 100


class Stealer(Bandit):
    hp_base = 1430
    attack_base = 328
    hit_frequency = 0.9
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 3
    armor_piercing = 2
    cost = 7
    move_speed = 2
    vehicule_damage_factor = 2  # Fixme: check if it's "200% damages" or "200% additional damages"
    rarity = Rarity.Epic
    upgrade_costs = Condor.upgrade_costs

    # TODO: invisibility effect

    def damage_formule(self, target: MovableUnit, target_index=0, hit_combo=0):
        dmg = super().damage_formule(target, target_index, hit_combo)
        if dmg is None:
            return None
        if isinstance(target, Vehicle):
            return dmg * self.vehicule_damage_factor
        else:
            return dmg


@reincarnation
class StealerLeg(Stealer):
    hit_frequency = 1.2
    shoot_to = TargetType.AIR_GROUND
    vehicule_damage_factor = 2.5


class Lich(Bandit):
    hp_base = 1072
    attack_base = 390
    hit_frequency = 0.4
    range = 5
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 6
    cost = 8
    move_speed = 1
    summon_number = 3
    summon_hp_base = 455
    summon_attack_base = 38
    summon_atk_speed = 1 / 10
    rarity = Rarity.Epic
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -590, -3000, -11200, -25000, -69000,  # 1 -> 6
        -158000, -334000, -470000, -690000, -980000,  # 6 -> 11
        -1840000, -3210000, -5670000, -9710000, -16860000,  # 11 -> 16
        -29940000, -53370000, -94020000, -169140000, -324200000,  # 16 -> 21
        -540560000, -921940000, -1520370000, -2540230000, -4293750000,  # 21 -> 26
        -7240750000, -11164920000, -15638860000, -21914960000,
        )


@reincarnation
class LichLeg(Lich):
    summon_number = 5
    summon_atk_speed = 1 / 7


class Inferno(Bandit):
    hp_base = 4407
    attack_base = 630
    hit_frequency = 0.7
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 12
    move_speed = 1.7
    rarity = Rarity.Legendary
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -940, -4800, -18100, -41000, -111000,  # 1 -> 6
        -254000, -537000, -755000, -1100000, -1580000,  # 6 -> 11
        -2950000, -5160000, -9110000, -15600000, -27100000,  # 11 -> 16
        -48110000, -85780000, -151110000, -271830000, -521040000,  # 16 -> 21
        -868760000, -1481690000, -2443450000, -4082510000, -6900670000,  # 21 -> 26
        -11636930000, -17943620000, -25133890000, -35220470000,
        )


class Demon(Bandit):
    hp_base = 3900
    attack_base = 500
    hit_frequency = 1
    range = 2
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 8
    armor_piercing = 4
    cost = 10
    move_speed = 1.9
    rarity = Rarity.Legendary
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -880, -4500, -16900, -38000, -103000,  # 1 -> 6
        -237000, -501000, -705000, -1030000, -1470000,  # 6 -> 11
        -2750000, -4820000, -8500000, -14560000, -25290000,  # 11 -> 16
        -44900000, -80060000, -141040000, -253700000, -486310000,  # 16 -> 21
        -810840000, -1382910000, -2280550000, -3810350000, -6440620000,  # 21 -> 26
        -10861130000, -16747380000, -23458290000, -32872430000,
        )


class Chaman(Bandit):
    hp_base = 1605
    attack_base = 504
    hit_frequency = 0.5
    range = 8
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 3
    cost = 12
    move_speed = 1.4
    rarity = Rarity.Legendary
    # TODO heal effect
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -840, -4300, -16100, -36000, -98000,  # 1 -> 6
        -226000, -477000, -671000, -980000, -1400000,  # 6 -> 11
        -2620000, -4590000, -8090000, -13860000, -24090000,  # 11 -> 16
        -42760000, -76250000, -134320000, -241620000, -463150000,  # 16 -> 21
        -772230000, -1317050000, -2171950000, -3628900000, -6133930000,  # 21 -> 26
        -10343940000, -15949890000, -22341230000, -31307080000,
        )


class Djin(Bandit, AOE):
    hp_base = 1456
    attack_base = 370
    hit_frequency = 0.5
    range = 6
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 11
    move_speed = 1.3
    summon_number = 1
    summon_hp = {8: 2627}
    summon_atk = {8: 450}
    summon_atk_speed = 1 / 10
    # TODO Slow down effect
    rarity = Rarity.Legendary
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -860, -4400, -16500, -37000, -101000,  # 1 -> 6
        -231000, -489000, -688000, -1010000, -1440000,  # 6 -> 11
        -2690000, -4700000, -8300000, -14210000, -24690000,  # 11 -> 16
        -43830000, -78150000, -137690000, -247660000, -474730000,  # 16 -> 21
        -791530000, -1349980000, -2226250000, -3719620000, -6287270000,  # 21 -> 26
        -10602530000, -16348630000, -22899760000, -32089760000,
        )


class Mecha(Bandit):
    hp_base = 1885
    attack_base = 331
    hit_frequency = 0.6
    range = 7
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 6
    armor_piercing = 0
    cost = 11
    move_speed = 1.5
    multiple_target_limit = 3
    missil_attack_base = 374
    missile_atk_speed = 0.5
    # TODO missile
    rarity = Rarity.Legendary
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -900, -4600, -17300, -39000, -106000,  # 1 -> 6
        -243000, -513000, -721000, -1050000, -1510000,  # 6 -> 11
        -2820000, -4930000, -8700000, -14900000, -25890000,  # 11 -> 16
        -45970000, -81960000, -144390000, -259740000, -497880000,  # 16 -> 21
        -830150000, -1415830000, -2334850000, -3901070000, -6593970000,  # 21 -> 26
        -11119730000, -17146130000, -24016820000, -33655110000,
        )


class Vampire(Bandit):
    hp_base = 1800
    attack_base = 510
    hit_frequency = 1
    range = 1.5
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 3
    cost = 12
    move_speed = 1.7
    # TODO spells
    rarity = Rarity.Legendary
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -940, -4800, -18100, -41000, -111000,  # 1 -> 6
        -254000, -537000, -755000, -1100000, -1580000,  # 6 -> 11
        -2950000, -5160000, -9110000, -15600000, -27100000,  # 11 -> 16
        -48110000, -85780000, -151110000, -271830000, -521040000,  # 16 -> 21
        -868760000, -1481690000, -2443450000, -4082510000, -6900670000,  # 21 -> 26
        -11636930000, -17943620000, -25133890000, -35220470000,
        )

# Register all defined cards
BANDITS.register_cards_in_module(Bandit, __name__)
