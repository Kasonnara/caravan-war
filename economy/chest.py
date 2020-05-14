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

"""
List the different types of chests (and temporally, samples of their possible loots)
"""

from collections import namedtuple
from typing import Tuple

from common.resources import ResourcePacket, Resources
from spells.convoy_boosts import SpeedBoost, AttackSpeedBoost, LifeBoost, AttackBoost, ModuleBoost, VehicleArmor
from spells.spells import Landmine, Meteor, Poison, Arrow, Ice
from units.bandits import Drone, Archer, Brute, Maraudeur, Hunter, Berserk, Spider, Alchimist, Lutin
from units.guardians import Scout, Guard, Healer, Follet, Shield, Knight, Sword
from units.vehicles import Charrette, Helicopter, Chariot
from units.modules import Balista, Mortar, Shotgun, Chaingun
from common.ligues import Rank as L


class Chest:
    number_of_card = None  # TODO property based on loot_example
    loot_example = None
    available_loot_categories = None  # TODO property based on loot_example


Loot = namedtuple('Loot', 'HQ_level ligue vip index resource_packet cards')
"""Memorise a chest loot result as well as looting current conditions (HQ looting, vip level and ligue level) 
for later analise (index is used for campaign, daily and weekly quests chest)"""
# TODO split card loots, ressources loots and shield loots


class RecycleChest(Chest):
    number_of_card = 5
    loot_example = [
        Loot(8, L.Horse2, 6, None, ResourcePacket(10103, 6816), (AttackSpeedBoost, Landmine, Landmine)),
        Loot(8, L.Horse3, 6, None, ResourcePacket(17576, 6859), (SpeedBoost, Landmine, LifeBoost)),
        Loot(8, L.Camel1, 6, None, ResourcePacket(22964, 6339), (SpeedBoost, Arrow, LifeBoost)),
        Loot(17, L.RedDragon3, 8, None, ResourcePacket(523000, 275000), (Ice, SpeedBoost, Poison)),
        Loot(17, L.RedDragon3, 8, None, ResourcePacket(579000, 313000), (Ice, Landmine, SpeedBoost)),
        Loot(17, L.RedDragon3, 8, None, ResourcePacket(439000, 310000), (Landmine, AttackSpeedBoost, AttackBoost)),
        Loot(17, L.RedDragon3, 8, None, ResourcePacket(436000, 298000), (Landmine, VehicleArmor, ModuleBoost)),  # entrepot full
        Loot(17, L.RedDragon3, 8, None, ResourcePacket(320000, 225000), (LifeBoost, Poison, Landmine)),  # entrepot full
        Loot(17, L.RedDragon3, 8, None, ResourcePacket(512000, 242000), (Landmine, VehicleArmor, AttackBoost)),
        Loot(17, L.RedDragon3, 8, None, ResourcePacket(457000, 277000), (Meteor, Arrow, LifeBoost)),
        Loot(17, L.RedDragon3, 8, None, ResourcePacket(410000, 163000), (Landmine, LifeBoost, AttackSpeedBoost)),
        Loot(17, L.RedDragon3, 8, None, ResourcePacket(378000, 305000), (AttackBoost, Arrow, Poison)),
        Loot(17, L.RedDragon3, 8, None, ResourcePacket(537000, 186000), (Arrow, Arrow, Landmine)),
        Loot(17, L.RedDragon3, 8, None, ResourcePacket(600000, 195000), (Meteor, Arrow, Poison)),
        Loot(17, L.RedDragon3, 8, None, ResourcePacket(589000, 161000), (Meteor, Landmine, Landmine)),  # entrepot full mais ça semble ok
        #Loot(17, L.RedDragon3, 8, None, ResourcePacket(, ), (, ,)),
        ]


class Exchange10km(Chest):
    # Wood Chest
    number_of_card = 5
    loot_example = [
        Loot(8, L.Horse2, 6, None, ResourcePacket(Resources.ReincarnationToken(1)), (Drone, Archer, Archer, Archer, Balista)),
        Loot(8, L.Horse2, 6, None, ResourcePacket(), (Scout, Scout, Archer, Archer, Balista)),
        Loot(8, L.Horse3, 6, None, ResourcePacket(), (Maraudeur, Follet, Guard, Guard, Guard)),
        Loot(8, L.Horse3, 6, None, ResourcePacket(), (Maraudeur, Maraudeur, Balista, Spider, AttackBoost)),
        Loot(8, L.Horse3, 6, None, ResourcePacket(), (Scout, Scout, Shotgun, Drone, Follet)),
        Loot(8, L.Horse3, 6, None, ResourcePacket(), (Maraudeur, Scout, Maraudeur, Scout, Guard)),
        Loot(8, L.Horse3, 6, None, ResourcePacket(), (Meteor, Drone, Drone, Archer, Balista)),
        ]



class Exchange100km(Chest):
    # Iron chest
    number_of_card = 6
    loot_example = [
        Loot(8, L.Horse3, 6, None, ResourcePacket(Resources.ReincarnationToken(2)), (Spider, Charrette, Follet, Maraudeur, Guard, Guard)),
        Loot(8, L.Horse3, 6, None, ResourcePacket(Resources.ReincarnationToken(1)), (Maraudeur, Drone, Drone, Archer, Archer, Archer)),
        Loot(8, L.Horse3, 6, None, ResourcePacket(), (Scout, Guard, Knight, LifeBoost, Archer, Archer)),
        ]


class Exchange1000km(Chest):
    # Silver chest
    number_of_card = 7
    loot_example = [
        Loot(8, L.Horse2, 6, None, ResourcePacket(), (Mortar, Berserk, Charrette, Maraudeur, Maraudeur, Archer, Landmine)),
        Loot(8, L.Horse2, 6, None, ResourcePacket(), (Shield, Knight, Sword, Archer, Scout, Scout, Guard)),
        Loot(8, L.Horse2, 6, None, ResourcePacket(Resources.ReincarnationToken(2)), (Maraudeur, Maraudeur, Archer, Alchimist, Scout, Maraudeur, Alchimist)),
        ]


class BestExchange(Chest):
    # Gold Chest
    # 1 rare minimum
    # Epic 42 %
    # Legendary 7%
    number_of_card = 8
    loot_example = [
        Loot(8, L.Horse2, 6, None, ResourcePacket(Resources.ReincarnationToken(5)), (Follet, Healer, Maraudeur, Guard, Guard, Maraudeur, Chariot)),
        ]


class RaidChest(Chest):
    # At least 1 Rare
    # Legendary: 3%
    # Epic: 18%
    number_of_card = 7
    loot_example = [
        Loot(8, L.Horse2, 6, None, ResourcePacket(Resources.ReincarnationToken(2), Resources.BanditShieldProtection()), (Charrette, Helicopter, Brute, Maraudeur, Hunter, Archer, Guard,)),
        Loot(8, L.Horse3, 6, None, ResourcePacket(Resources.ReincarnationToken(2)), (Chaingun, Maraudeur, Scout, Scout, Poison, Lutin, Berserk)),
        ]


class DailyQuest(Chest):
    # for DailyQuest chest index means the chest index in the list
    loot_example = [
        Loot(8, L.Horse3, 6, 2, ResourcePacket(Resources.Gold(10000), Resources.BeginnerGrowth(20)), ()),
        Loot(8, L.Horse3, 6, 3, ResourcePacket(Resources.Goods(10000),  Resources.BeginnerGrowth(20)), (Hunter,)),
        Loot(8, L.Horse3, 6, 4, ResourcePacket(Resources.Gold(10000), Resources.BeginnerGrowth(20)), (Healer,)),
        Loot(8, L.Horse3, 6, 5, ResourcePacket(Resources.Gem(20), Resources.LifePotion(1), Resources.BeginnerGrowth(20)), ()),
        Loot(8, L.Horse3, 6, 1, ResourcePacket(Resources.Goods(10000), Resources.BeginnerGrowth(20)), ()),
        Loot(8, L.Horse3, 6, 2, ResourcePacket(Resources.Gold(10000), Resources.BeginnerGrowth(20)), ()),
        Loot(8, L.Horse3, 6, 3, ResourcePacket(Resources.Goods(10000), Resources.BeginnerGrowth(20)), (Alchimist,)),
        Loot(8, L.Horse3, 6, 4, ResourcePacket(Resources.Gold(10000), Resources.BeginnerGrowth(20)), (Shield,)),
        Loot(8, L.Camel1, 6, 5, ResourcePacket(Resources.Gem(20), Resources.LifePotion(1), Resources.BeginnerGrowth(20)), ()),
        ]


class WeeklyQuest(Chest):
    # for WeklyQuest chest index means the chest index in the list
    loot_example = [
        Loot(8, L.Horse3, 6, 4, ResourcePacket(Resources.Gold(30000), Resources.LifePotion(5), Resources.BeginnerGrowth(60)), ()),
        Loot(8, L.Horse3, 6, 5, ResourcePacket(Resources.Gold(50000), Resources.Gem(100), Resources.BeginnerGrowth(60)), ()),
        ]


class Campaign(Chest):
    # for campaign chest index means the compaign index
    loot_example = [
        # Gold Chest
        # 1 rare minimum
        # Epic 42 %
        # Legendary 7%
        Loot(8, L.Horse3, 6, 5, ResourcePacket(), (Hunter, Maraudeur, Arrow, Shield, Brute, Follet, Archer, Archer))
        ]


class Raid(Chest):
    # For raid chest: index means the number of stars won
    loot_example = [
        Loot(8, L.Horse2, 6, 3, ResourcePacket(Resources.Gem(24), Resources.LifePotion(1))),
        Loot(8, L.Horse2, 6, 3, ResourcePacket(Resources.LifePotion(1), Resources.ReincarnationToken(3))),
        Loot(8, L.Horse2, 6, 3, ResourcePacket(Resources.Gem(25), Resources.LifePotion(1), Resources.ReincarnationToken(3), Resources.LegendarySoul(3))),
        Loot(8, L.Horse2, 6, 3, ResourcePacket(Resources.LifePotion(1), Resources.LegendarySoul(2))),
        Loot(8, L.Horse3, 6, 3, ResourcePacket(Resources.ReincarnationToken(3))),
        ]
