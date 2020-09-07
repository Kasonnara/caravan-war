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

from typing import Union, List

from buildings.buildings import Academy
from common.alignment import Alignment
from common.card_categories import GUARDIANS
from common.rarity import Rarity
from common.resources import resourcepackets_gold
from lang.languages import TranslatableString
from units.base_units import MovableUnit, Heal, AOE, reincarnation, DPS_SCORE_FACTOR, \
    HP_SCORE_FACTOR
from common.target_types import TargetType


class Guardian(MovableUnit):
    alignment = Alignment.DEFENDER
    base_building = Academy
    move_speed = 1.2
    bossfight_cost = None

    __display_name = TranslatableString("Guardian", french="Gardien")


class Scout(Guardian):
    hp_base = 700
    attack_base = 87
    hit_frequency = 0.5
    range = 3
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 1
    bossfight_cost = 20
    rarity = Rarity.Common
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -110, -500, -2100, -5000, -13000,  # 1 -> 6
        -31000, -65000, -92000, -130000, -240000,  # 6 -> 11
        -450000, -790000, -1390000, -2370000, -4120000,  # 11 -> 16
        -7320000, -13050000, -22990000, -41360000, -79270000,  # 16 -> 21
        -132170000, -225420000, -371750000, -621110000, -1049870000,  # 21 -> 26
        -1770440000, -2729940000, -3823860000, -5358430000,
        )

    __display_name = TranslatableString("Scout", french="Scout")


class Guard(Guardian):
    hp_base = 800
    attack_base = 67
    hit_frequency = 0.5
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 4
    armor_piercing = 0
    cost = 1
    bossfight_cost = 18
    rarity = Rarity.Common
    upgrade_costs = Scout.upgrade_costs

    __display_name = TranslatableString("Guard", french="Garde")


class Healer(AOE, Heal, Guardian):
    hp_base = 800
    base_heal = 60
    heal_frequency = 1/8
    heal_range = 5.5
    heal_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    cost = 2
    # TODO: heal spell
    bossfight_cost = 25
    rarity = Rarity.Rare
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -190, -900, -3700, -10000, -24000,  # 1 -> 6
        -56000, -118000, -165000, -240000, -430000,  # 6 -> 11
        -810000, -1410000, -2490000, -4270000, -7420000,  # 11 -> 16
        -13170000, -23490000, -41380000, -74440000, -142690000,  # 16 -> 21
        -237130000, -428300000, -706320000, -1180110000, -1889760000,  # 21 -> 26
        -3186790000, -4913890000, -6882960000, -9645180000,
        )

    __display_name = TranslatableString("Artificer", french="Artificière")


class Follet(Guardian):
    hp_base = 760
    attack_base = 135
    hit_frequency = 0.4
    range = 2
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.AIR
    armor = 0
    armor_piercing = 0
    cost = 2
    bossfight_cost = 25
    rarity = Rarity.Common
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -130, -600, -2500, -6000, -16000,  # 1 -> 6
        -37000, -78000, -110000, -160000, -290000,  # 6 -> 11
        -540000, -940000, -1660000, -2850000, -4950000,  # 11 -> 16
        -8780000, -15660000, -27590000, -49630000, -95130000,  # 16 -> 21
        -158610000, -270510000, -446090000, -745330000, -1259840000,  # 21 -> 26
        -2124530000, -3275930000, -4588640000, -6430120000,
        )
    __display_name = TranslatableString("Wisp", french="Feu follet")


class Shield(Guardian):
    hp_base = 1425
    attack_base = 205
    hit_frequency = 0.4
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 2
    bossfight_cost = 35
    rarity = Rarity.Rare
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -220, -1000, -4100, -11000, -27000,  # 1 -> 6
        -62000, -131000, -183000, -270000, -480000,  # 6 -> 11
        -900000, -1570000, -2770000, -4750000, -8240000,  # 11 -> 16
        -14640000, -26100000, -45980000, -82710000, -158540000,  # 16 -> 21
        -264340000, -450850000, -743490000, -1242220000, -2099730000,  # 21 -> 26
        -3540880000, -5459880000, -8649730000, -10716870000,
        )
    __display_name = TranslatableString("Shield Master", french="Bouclier")


class Jetpack(Guardian):
    hp_base = 990
    attack_base = 175
    hit_frequency = 0.5
    range = 4
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.AIR
    armor = 0
    armor_piercing = 0
    cost = 2
    # TODO: EMP spell
    bossfight_cost = 33
    rarity = Rarity.Rare
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -170, -800, -3300, -9000, -22000,  # 1 -> 6
        -49000, -105000, -146000, -210000, -380000,  # 6 -> 11
        -720000, -1260000, -2220000, -3800000, -6600000,  # 11 -> 16
        -11710000, -20880000, -36780000, -66170000, -126830000,  # 16 -> 21
        -211480000, -360680000, -594790000, -993780000, -1679790000,  # 21 -> 26
        -2832700000, -4367900000, -6118180000, -8573490000,
        )
    __display_name = TranslatableString("Jet Trooper", french="Unité jetpack")


class Knight(Guardian):
    hp_base = 1254
    attack_base = 135
    hit_frequency = 0.6
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 4
    armor_piercing = 0
    cost = 2
    # TODO double armor spell
    bossfight_cost = 35
    rarity = Rarity.Rare
    upgrade_costs = Shield.upgrade_costs
    __display_name = "Champion"


class Sword(AOE, Guardian):
    hp_base = 1024
    attack_base = 143
    hit_frequency = 0.5
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 2
    bossfight_cost = 40
    rarity = Rarity.Rare
    gold_cost = 10000
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -210, -900, -3900, -10000, -26000,  # 1 -> 6
        -59000, -124000, -174000, -260000, -460000,  # 6 -> 11
        -850000, -1490000, -2630000, -4510000, -7830000,  # 11 -> 16
        -13910000, -24790000, -43680000, -78580000, -150620000,  # 16 -> 21
        -251130000, -428300000, -706320000, -1180110000, -1994740000,  # 21 -> 26
        -3363830000, -5186880000, -7265340000, -10181870000,
        )
    __display_name = TranslatableString("Blade Master", french="Maître épéiste")


class Sparte(Guardian):
    hp_base = 2895
    attack_base = 260
    hit_frequency = 0.7
    range = 2
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 4
    # TODO armor gain spell
    bossfight_cost = 80
    #armor_duration = 1
    #armor_cooldown = 0.8
    rarity = Rarity.Epic
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -290, -1300, -5600, -14000, -36000,  # 1 -> 6
        -83000, -177000, -247000, -360000, -650000,  # 6 -> 11
        -1210000, -2120000, -3740000, -6410000, -11130000,  # 11 -> 16
        -19760000, -35230000, -62070000, -111660000, -214030000,  # 16 -> 21
        -356870000, -608640000, -1003710000, -1677000000, -2834640000,  # 21 -> 26
        -4780190000, -7370830000, -10324430000, -14467770000,
        )
    __display_name = TranslatableString("Spartans", french="Spartiates")


@reincarnation
class SparteLeg(Sparte):
    armor_boost = 2
    armor_boost_duration = 6
    max_armor_boost = 16


class Paladin(Guardian):
    hp_base = 2561
    attack_base = 253
    hit_frequency = 0.8
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 5
    armor_piercing = 0
    cost = 4
    # TODO: charge spell
    bossfight_cost = None
    rarity = Rarity.Epic
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -320, -1400, -6200, -16000, -40000,  # 1 -> 6
        -93000, -196000, -275000, -400000, -720000,  # 6 -> 11
        -1350000, -2360000, -4160000, -7120000, -12370000,  # 11 -> 16
        -21960000, -39150000, -68970000, -124070000, -237810000,  # 16 -> 21
        -396520000, -676270000, -1078060000, -1801230000, -3149600000,  # 21 -> 26
        -5311320000, -8189820000, -11471590000, -16075300000,
        )
    __display_name = "Paladin"


@reincarnation
class PaladinLeg(Paladin):
    charge_resistance = 0.5


class Marchal(Guardian):
    hp_base = 2500
    attack_base = 299
    hit_frequency = 0.5
    range = 6
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 4
    multiple_target_limit = 2
    bossfight_cost = 90
    rarity = Rarity.Epic
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -300, -1300, -5800, -15000, -38000,  # 1 -> 6
        -86000, -183000, -256000, -380000, -670000,  # 6 -> 11
        -1260000, -2200000, -3880000, -6640000, -11540000,  # 11 -> 16
        -20490000, -36540000, -64370000, -115800000, -221960000,  # 16 -> 21
        -370080000, -631190000, -1040890000, -1739110000, -2939620000,  # 21 -> 26
        -4957230000, -7643830000, -10706820000, -15063610000,
        )
    __display_name = TranslatableString("Marshal", french="Marchal")


@reincarnation
class MarchalLeg(Marchal):
    multiple_target_limit = 3


class Griffon(Guardian):
    hp_base = 1794
    attack_base = 347
    hit_frequency = 0.4
    range = 4
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.AIR
    armor = 3
    armor_piercing = 0
    cost = 4
    dodge_inaccuracy = 0.8
    move_speed = 1.8
    bossfight_cost = None
    rarity = Rarity.Epic
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -310, -1400, -6000, -15000, -39000,  # 1 -> 6
        -90000, -190000, -265000, -390000, -700000,  # 6 -> 11
        -1300000, -2280000, -4020000, -6880000, -11950000,  # 11 -> 16
        -21230000, -37840000, -66670000, -119930000, -229890000,  # 16 -> 21
        -383300000, -653730000, -1078060000, -1801230000, -3044610000,  # 21 -> 26
        -5134270000, -7916820000, -11089210000, -15539460000,
        )
    __display_name = TranslatableString("Griffin Rider", french="Chevaucheur de Griffon")


@reincarnation
class GriffonLeg(Griffon):
    esquive_next_attack_boost = 3.0


class Hammer(Guardian):
    hp_base = 2145
    attack_base = 364
    hit_frequency = 0.5
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 5
    armor_piercing = 0
    cost = 4
    shield_range = 10
    shield_duration = 7
    # TODO: shield spell
    bossfight_cost = None
    rarity = Rarity.Epic
    upgrade_costs = Sparte.upgrade_costs
    __display_name = TranslatableString("Chaplain", french="Aumonier")


@reincarnation
class HammerLeg(Hammer):
    spell_max_stacking = 3


class Canonner(Guardian, AOE):
    hp_base = 4000
    attack_base = 204
    hit_frequency = 0.5
    range = 8
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 4
    bossfight_cost = 190
    rarity = Rarity.Legendary
    aoe_radius = 1
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -440, -2000, -8500, -22000, -55000,  # 1 -> 6
        -127000, -268000, -375000, -550000, -980000,  # 6 -> 11
        -1840000, -3220000, -5680000, -9730000, -16900000,  # 11 -> 16
        -30010000, -53500000, -94260000, -169560000, -325010000,  # 16 -> 21
        -541910000, -924240000, -1524160000, -2546560000, -4304450000,  # 21 -> 26
        -7258800000, -11192750000, -15677840000, -21969580000,
        )
    __display_name = TranslatableString("Cannoneer", french="Cannonière")


class DemonSlayer(Guardian):
    hp_base = 3750
    attack_base = 230
    hit_frequency = 1
    range = 6
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 4
    armor_piercing = 6
    cost = 4
    can_miss = False
    # TODO: ignore 50% armmor (50% of what : armor value or damage reduction % ?)
    bossfight_cost = 200
    rarity = Rarity.Legendary
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -450, -2000, -8700, -22000, -57000,  # 1 -> 6
        -130000, -275000, -384000, -560000, -1010000,  # 6 -> 11
        -1880000, -3300000, -5820000, -9970000, -17310000,  # 11 -> 16
        -30740000, -54810000, -96560000, -173690000, -332940000,  # 16 -> 21
        -555120000, -946780000, -1561330000, -2608670000, -4514420000,  # 21 -> 26
        -7612890000, -11738740000, -16442620000, -23041260000,
        )
    __display_name = TranslatableString("Demon Hunter", french="Chasseur de démon")


class Golem(AOE, Guardian):
    hp_base = 4849
    attack_base = 367
    hit_frequency = 0.4
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 6
    cost = 6
    aoe_radius = 1
    # TODO: stone wall on death
    bossfight_cost = 190
    rarity = Rarity.Legendary
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -480, -2100, -9100, -23000, -59000,  # 1 -> 6
        -136000, -288000, -403000, -590000, -1060000,  # 6 -> 11
        -1970000, -3450000, -6100000, -10440000, -18140000,  # 11 -> 16
        -32200000, -57420000, -101150000, -181960000, -348790000,  # 16 -> 21
        -581560000, -991860000, -1635680000, -2732890000, -4619410000,  # 21 -> 26
        -7789930000, -12011730000, -16825000000, -23577110000,
        )
    __display_name = "Golem"


class Seraphin(Guardian, Heal):
    hp_base = 3718
    attack_base = 478
    hit_frequency = 1
    range = 2
    shoot_to = TargetType.AIR_GROUND
    base_heal = 30
    heal_frequency = 1
    heal_range = 3  #4
    heal_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 4
    armor_piercing = 0
    cost = 6
    # TODO: heal spell
    bossfight_cost = 200
    rarity = Rarity.Legendary
    upgrade_costs = DemonSlayer.upgrade_costs[:25] + resourcepackets_gold(
        -4409440000,  # 21 -> 26
        -7435840000, -11465740000, -16060230000, -22505420000,
        )
    __display_name = TranslatableString("Seraph", french="Seraphin")

    def score(self, allies_targets: Union['MovableUnit', List['MovableUnit']]):
        # FIXME: heal doesn't apply to ennemy but to allies!
        return (
                self.dps_score(allies_targets) / DPS_SCORE_FACTOR
                + self.hps_score(allies_targets) / DPS_SCORE_FACTOR
                + self.hp_score(allies_targets) / HP_SCORE_FACTOR
            )


class Wizard(Guardian):
    hp_base = 4400
    attack_base = 500
    hit_frequency = 0.7
    range = 2
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.AIR
    armor = 0
    armor_piercing = 0
    cost = 6
    # TODO: stun
    stun_duration = 1
    stun_radius = 4
    bossfight_cost = 190
    rarity = Rarity.Legendary
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        -460, -2100, -8900, -23000, -58000,  # 1 -> 6
        -133000, -281000, -394000, -580000, -1030000,  # 6 -> 11
        -1930000, -3380000, -5960000, -10200000, -17730000,  # 11 -> 16
        -31470000, -56110000, -98860000, -177830000, -340870000,  # 16 -> 21
        -568340000, -969320000, -1598500000, -2670780000, -4514420000,  # 21 -> 26
        -7612890000, -11738740000, -16442620000, -23041260000,
        )
    __display_name = TranslatableString("Warlock", french="Sorcier")


# Register all defined cards
GUARDIANS.register_cards_in_module(Guardian, __name__)
