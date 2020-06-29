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
Contain several chest opening examples for exploration and testing
"""
from collections import namedtuple

from common.resources import ResourcePacket, Resources
from economy.chests import RecycleChest, WoodenChest, IronChest, SilverChest, GoldenChest, RaidChest
from spells.convoy_boosts import *
from spells.spells import *
from units.bandits import *
from units.guardians import *
from units.vehicles import *
from units.modules import *
from common.leagues import Rank as L


Loot = namedtuple('Loot', 'HQ_level ligue vip index resource_packet cards')
"""Memorise a chest loot result as well as looting current conditions (HQ looting, vip level and ligue level) 
for later analise (index indicate the campaign index or the index in of the chest for daily and weekly quests chest, and for regular tradings it indicate the index of the chest since the last reset and in the entire day)"""
# TODO split card loots, ressources loots and shield loots

chest_opening_examples = {
    RecycleChest: [
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
        ],

    WoodenChest: [
        Loot(8, L.Horse2, 6, None, ResourcePacket(Resources.ReincarnationToken(1)),
             (Drone, Archer, Archer, Archer, Balista)),
        Loot(8, L.Horse2, 6, None, ResourcePacket(), (Scout, Scout, Archer, Archer, Balista)),
        Loot(8, L.Horse3, 6, None, ResourcePacket(), (Maraudeur, Follet, Guard, Guard, Guard)),
        Loot(8, L.Horse3, 6, None, ResourcePacket(), (Maraudeur, Maraudeur, Balista, Spider, AttackBoost)),
        Loot(8, L.Horse3, 6, None, ResourcePacket(), (Scout, Scout, Shotgun, Drone, Follet)),
        Loot(8, L.Horse3, 6, None, ResourcePacket(), (Maraudeur, Scout, Maraudeur, Scout, Guard)),
        Loot(8, L.Horse3, 6, None, ResourcePacket(), (Meteor, Drone, Drone, Archer, Balista)),
        Loot(19, L.Phenix1, 8, None, ResourcePacket(), (Archer, Maraudeur, Hunter, Follet, Follet)),
        Loot(19, L.Phenix1, 8, (6, 6), ResourcePacket(), (Guard, Guard, Follet, Follet, Healer)),
        ],

    IronChest: [
        Loot(8, L.Horse3, 6, None, ResourcePacket(Resources.ReincarnationToken(2)), (Spider, Charrette, Follet, Maraudeur, Guard, Guard)),
        Loot(8, L.Horse3, 6, None, ResourcePacket(Resources.ReincarnationToken(1)), (Maraudeur, Drone, Drone, Archer, Archer, Archer)),
        Loot(8, L.Horse3, 6, None, ResourcePacket(), (Scout, Guard, Knight, LifeBoost, Archer, Archer)),
        Loot(19, L.Phenix1, 8, None, ResourcePacket(Resources.ReincarnationToken(1)), (Meteor, Landmine, Drone, Healer, Brute, Knight)),
        Loot(19, L.Phenix1, 8, (0, 6), ResourcePacket(), (Drone, Follet, Mortar, Scout, Scout, Chariot)),
        ],

    SilverChest: [
        Loot(8, L.Horse2, 6, None, ResourcePacket(),
             (Mortar, Berserk, Charrette, Maraudeur, Maraudeur, Archer, Landmine)),
        Loot(8, L.Horse2, 6, None, ResourcePacket(), (Shield, Knight, Sword, Archer, Scout, Scout, Guard)),
        Loot(8, L.Horse2, 6, None, ResourcePacket(Resources.ReincarnationToken(2)),
             (Maraudeur, Maraudeur, Archer, Alchimist, Scout, Maraudeur, Alchimist)),
        Loot(8, L.Horse2, 6, None, ResourcePacket(Resources.ReincarnationToken(2)),
             (Maraudeur, Maraudeur, Archer, Alchimist, Scout, Maraudeur, Alchimist)),
        Loot(19, L.Phenix1, 8, (1, 3), ResourcePacket(), (Hunter, Alchimist, Maraudeur, Maraudeur, Archer, Archer, Scout)),
        ],

    GoldenChest: [
        Loot(8, L.Horse2, 6, None, ResourcePacket(Resources.ReincarnationToken(5)),
             (Follet, Healer, Maraudeur, Guard, Guard, Maraudeur, Chariot)),
        Loot(8, L.Horse3, 6, 5, ResourcePacket(), (Hunter, Maraudeur, Arrow, Shield, Brute, Follet, Archer, Archer)),
        Loot(19, L.Phenix1, 8, (0, 1), ResourcePacket(Resources.ReincarnationToken(1)), (Hunter, Maraudeur, Maraudeur, Alchimist, Alchimist, AttackBoost, Scout, Healer)),
        ],

    RaidChest: [
        # For raid chest: index means the number of stars won
        Loot(8, L.Horse2, 6, None, ResourcePacket(Resources.ReincarnationToken(2), Resources.BanditShieldProtection()),
             (Charrette, Helicopter, Brute, Maraudeur, Hunter, Archer, Guard,)),
        Loot(8, L.Horse3, 6, None, ResourcePacket(Resources.ReincarnationToken(2)),
             (Chaingun, Maraudeur, Scout, Scout, Poison, Lutin, Berserk)),
        ],

    #DailyQuestChest: [
    #    Loot(8, L.Horse3, 6, 2, ResourcePacket(Resources.Gold(10000), Resources.BeginnerGrowth(20)), ()),
    #    Loot(8, L.Horse3, 6, 3, ResourcePacket(Resources.Goods(10000), Resources.BeginnerGrowth(20)), (Hunter,)),
    #    Loot(8, L.Horse3, 6, 4, ResourcePacket(Resources.Gold(10000), Resources.BeginnerGrowth(20)), (Healer,)),
    #    Loot(8, L.Horse3, 6, 5,
    #         ResourcePacket(Resources.Gem(20), Resources.LifePotion(1), Resources.BeginnerGrowth(20)), ()),
    #    Loot(8, L.Horse3, 6, 1, ResourcePacket(Resources.Goods(10000), Resources.BeginnerGrowth(20)), ()),
    #    Loot(8, L.Horse3, 6, 2, ResourcePacket(Resources.Gold(10000), Resources.BeginnerGrowth(20)), ()),
    #    Loot(8, L.Horse3, 6, 3, ResourcePacket(Resources.Goods(10000), Resources.BeginnerGrowth(20)), (Alchimist,)),
    #    Loot(8, L.Horse3, 6, 4, ResourcePacket(Resources.Gold(10000), Resources.BeginnerGrowth(20)), (Shield,)),
    #    Loot(8, L.Camel1, 6, 5,
    #         ResourcePacket(Resources.Gem(20), Resources.LifePotion(1), Resources.BeginnerGrowth(20)), ()),
    #    ],

    WeeklyQuestChest: [
        Loot(8, L.Horse3, 6, 4,
             ResourcePacket(Resources.Gold(30000), Resources.LifePotion(5), Resources.BeginnerGrowth(60)), ()),
        Loot(8, L.Horse3, 6, 5, ResourcePacket(Resources.Gold(50000), Resources.Gem(100), Resources.BeginnerGrowth(60)),
             ()),
        ],

    }
