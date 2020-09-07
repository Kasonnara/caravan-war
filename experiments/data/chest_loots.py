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
        # --- Test day 1 ---
        Loot(19, L.Phenix1, 8, None, ResourcePacket(Resources.ReincarnationToken(1)), (Archer, Follet, Follet, Follet, Guard)),
        Loot(19, L.Phenix1, 8, (1, 1), ResourcePacket(Resources.ReincarnationToken(1)), (Maraudeur,)*5),
        Loot(19, L.Phenix1, 8, (2, 2), ResourcePacket(Resources.ReincarnationToken(0)), (Scout,)*4 + (Archer,)),
        Loot(19, L.Phenix1, 8, (3, 3), ResourcePacket(Resources.ReincarnationToken(0)),
             (Poison, Scout, Scout, Balista, Drone)),
        Loot(19, L.Phenix1, 8, (4, 4), ResourcePacket(Resources.ReincarnationToken(0)), (Guard, Guard, Follet, Follet, Scout)),
        Loot(19, L.Phenix1, 8, (5, 5), ResourcePacket(Resources.ReincarnationToken(0)), (Follet, Balista, Archer, Archer, LifeBoost)),
        # -- reset
        Loot(19, L.Phenix1, 8, (6, 6), ResourcePacket(Resources.ReincarnationToken(2)), (Landmine, Guard, Maraudeur, Scout, Poison)),
        Loot(19, L.Phenix1, 8, (7, 7), ResourcePacket(), (Maraudeur, Archer, Archer, Archer, Follet)),
        Loot(19, L.Phenix1, 8, (8, 8), ResourcePacket(Resources.ReincarnationToken(2)),
             (Guard, Guard, Scout, Scout, Archer)),
        # -- reset
        Loot(19, L.Phenix1, 8, (9, 9), ResourcePacket(Resources.ReincarnationToken(0)),
             (Guard, Guard, Drone, Drone, LifeBoost)),
        Loot(19, L.Phenix1, 8, (10, 10), ResourcePacket(Resources.ReincarnationToken(0)),
             (Follet, Guard, Guard, Guard, Archer)),
        # -- reset
        Loot(19, L.Phenix1, 8, (11, 11), ResourcePacket(Resources.ReincarnationToken(2)),
             (Follet, Follet, Archer, Archer, Scout)),
        Loot(19, L.Phenix1, 8, (12, 12), ResourcePacket(Resources.ReincarnationToken(0)),
             (Guard, Guard, Archer, Follet, Follet)),
        Loot(19, L.Phenix1, 8, (13, 13), ResourcePacket(Resources.ReincarnationToken(0)),
             (Maraudeur, Maraudeur, Guard, Guard, Follet)),
        Loot(19, L.Phenix1, 8, (14, 14), ResourcePacket(Resources.ReincarnationToken(0)),
             (Scout, Scout, Landmine, Maraudeur, Drone)),
        Loot(19, L.Phenix1, 8, (15, 15), ResourcePacket(Resources.ReincarnationToken(0)),
             (Follet, Follet, Archer, Balista, Balista)),
        Loot(19, L.Phenix1, 8, (16, 16), ResourcePacket(Resources.ReincarnationToken(0)),
             (Maraudeur, Maraudeur, Scout, Scout, Guard)),
        Loot(19, L.Phenix1, 8, (17, 17), ResourcePacket(Resources.ReincarnationToken(0)),
             (Scout, Scout, Balista, Balista, Maraudeur)),
        # --- End test day 1 ---
        # --- Test day 2 ---
        Loot(19, L.Phenix1, 8, (0, 0), ResourcePacket(Resources.ReincarnationToken(0)),
             (Arrow, Maraudeur, Maraudeur, Guard, Scout)),
        Loot(19, L.Phenix1, 8, (1, 1), ResourcePacket(Resources.ReincarnationToken(0)),
             (Guard, Guard, Brute, Scout, Scout)),
        Loot(19, L.Phenix1, 8, (2, 2), ResourcePacket(Resources.ReincarnationToken(1)),
             (Guard, Guard, Follet, Scout, Scout)),
        Loot(19, L.Phenix1, 8, (3, 3), ResourcePacket(Resources.ReincarnationToken(2)),
             (Scout, Guard, Guard, Guard, Poison)),
        #  -- reset
        Loot(19, L.Phenix1, 8, (4, 4), ResourcePacket(Resources.ReincarnationToken(0)),
             (Landmine, Follet, Archer, Archer, Balista)),
        Loot(19, L.Phenix1, 8, (5, 5), ResourcePacket(Resources.ReincarnationToken(0)),
             (Guard, Guard, Drone, Drone, Balista)),
        Loot(19, L.Phenix1, 8, (6, 6), ResourcePacket(Resources.ReincarnationToken(0)),
             (Scout, Balista, Balista, Knight, Maraudeur)),
        #  -- reset
        Loot(19, L.Phenix1, 8, (7, 7), ResourcePacket(Resources.ReincarnationToken(1)),
             (Arrow, Alchimist, Guard, Archer, Guard)),
        # --- End test day 2 ---
        ],

    IronChest: [
        Loot(8, L.Horse3, 6, None, ResourcePacket(Resources.ReincarnationToken(2)), (Spider, Charrette, Follet, Maraudeur, Guard, Guard)),
        Loot(8, L.Horse3, 6, None, ResourcePacket(Resources.ReincarnationToken(1)), (Maraudeur, Drone, Drone, Archer, Archer, Archer)),
        Loot(8, L.Horse3, 6, None, ResourcePacket(), (Scout, Guard, Knight, LifeBoost, Archer, Archer)),
        Loot(19, L.Phenix1, 8, None, ResourcePacket(Resources.ReincarnationToken(1)), (Meteor, Landmine, Drone, Healer, Brute, Knight)),
        Loot(19, L.Phenix1, 8, (0, 6), ResourcePacket(), (Drone, Follet, Mortar, Scout, Scout, Chariot)),
        # --- Test day 1 ---
        Loot(19, L.Phenix1, 8, (1, 1), ResourcePacket(Resources.ReincarnationToken(2)), (Guard, Maraudeur, Berserk, Follet, Brute, Meteor)),
        Loot(19, L.Phenix1, 8, (2, 2), ResourcePacket(Resources.ReincarnationToken(0)),
             (Chariot, Knight, Arrow, Archer, Alchimist)),
        Loot(19, L.Phenix1, 8, (3, 3), ResourcePacket(Resources.ReincarnationToken(0)),
             (Follet, Follet, Maraudeur, Lutin, Scout, Scout)),
        # -- reset
        Loot(19, L.Phenix1, 8, (0, 4), ResourcePacket(Resources.ReincarnationToken(0)),
             (Archer, Archer, Archer, Guard, Berserk, Maraudeur)),
        Loot(19, L.Phenix1, 8, (1, 5), ResourcePacket(),
             (Follet, Guard, Archer, Hunter, Mortar, Berserk)),
        # -- reset
        Loot(19, L.Phenix1, 8, (2, 6), ResourcePacket(Resources.ReincarnationToken(0)),
             (Scout,Follet, Chariot, Lutin, Drone, Alchimist)),
        Loot(19, L.Phenix1, 8, (0, 7), ResourcePacket(Resources.ReincarnationToken(0)),
             (SpeedBoost, Follet, Berserk, Berserk, Hunter, Brute)),
        Loot(19, L.Phenix1, 8, (1, 8), ResourcePacket(Resources.ReincarnationToken(0)),
             (Lutin, Archer, Maraudeur, Shield, Guard, Guard)),
        # -- reset
        Loot(19, L.Phenix1, 8, (2, 9), ResourcePacket(Resources.ReincarnationToken(0)),
             (Jetpack, Archer, Drone, Hunter, Hunter, Hunter)),
        Loot(19, L.Phenix1, 8, (0, 10), ResourcePacket(), None),
        Loot(19, L.Phenix1, 8, (1, 11), ResourcePacket(Resources.ReincarnationToken(0)),
             (Scout, Scout, Scout, Hunter, Maraudeur, Drone)),
        Loot(19, L.Phenix1, 8, (2, 12), ResourcePacket(Resources.ReincarnationToken(0)),
             (Charrette, Follet, Archer, Brute, Guard, Chariot)),
        # --- End test day 1 ---
        # --- Test day 2 ---
        Loot(19, L.Phenix1, 8, (0, 0), ResourcePacket(Resources.ReincarnationToken(3)),
             (Guard, AttackSpeedBoost, Arrow, Scout, Alchimist, Lutin)),
        Loot(19, L.Phenix1, 8, (1, 1), ResourcePacket(Resources.ReincarnationToken(0)),
             (Guard, Guard, Follet, Maraudeur, Maraudeur, Maraudeur)),
        #  -- reset
        Loot(19, L.Phenix1, 8, (2, 2), ResourcePacket(Resources.ReincarnationToken(0)),
             (Landmine, Maraudeur, Healer, Follet, Alchimist, Guard)),
        Loot(19, L.Phenix1, 8, (0, 3), ResourcePacket(Resources.ReincarnationToken(0)),
             (Drone, Drone, Jetpack, Hunter, Knight, Archer)),
        Loot(19, L.Phenix1, 8, (1, 4), ResourcePacket(Resources.ReincarnationToken(0)),
             (Maraudeur,) * 4 + (Archer, Knight)),
        #  -- reset
        Loot(19, L.Phenix1, 8, (2, 5), ResourcePacket(Resources.ReincarnationToken(0)),
             (Archer, Healer, Hunter, Guard, Alchimist, Landmine)),
        # --- End test day 2 ---
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
        # --- Test day 1 ---
        Loot(19, L.Phenix1, 8, (0, 0), ResourcePacket(Resources.ReincarnationToken(3)),
             (Shield, Shield, Maraudeur, Maraudeur, Guard, Guard, Guard)),
        Loot(19, L.Phenix1, 8, (1, 1), ResourcePacket(Resources.ReincarnationToken(1)),
             (Shield, Guard, Guard, Follet, Dirigeable, Drone, Drone)),
        # -- reset
        Loot(19, L.Phenix1, 8, (0, 2), ResourcePacket(Resources.ReincarnationToken(0)),
             (Shield, Sword, Follet, Follet, Spider, Spider, Drone)),
        # -- reset
        Loot(19, L.Phenix1, 8, (1, 3), ResourcePacket(Resources.ReincarnationToken(0)),
             (Arrow, Storm, Paladin, Maraudeur, Spider, Shield, Shield)),
        Loot(19, L.Phenix1, 8, (0, 4), ResourcePacket(Resources.ReincarnationToken(0)),
             (Alchimist, Scout, Scout, Shotgun, Drone, Maraudeur, Maraudeur)),
        #  -- reset
        Loot(19, L.Phenix1, 8, (1, 5), ResourcePacket(Resources.ReincarnationToken(0)),
             (Lutin, Arrow, Knight, Sword, Follet, Guard, Guard)),
        Loot(19, L.Phenix1, 8, (0, 6), ResourcePacket(), None),
        # --- End test day 1 ---
        # --- Test day 2 ---
        Loot(19, L.Phenix1, 8, (0, 0), ResourcePacket(Resources.ReincarnationToken(4)),
             (Maraudeur, Maraudeur, Hunter, DarkKnight, Archer, Mortar, Jetpack)),
        Loot(19, L.Phenix1, 8, (1, 1), ResourcePacket(), None),
        #  -- reset
        Loot(19, L.Phenix1, 8, (0, 2), ResourcePacket(Resources.ReincarnationToken(0)),
             (Maraudeur, Scout, LifeBoost, Berserk, Shotgun, Drone, Drone)),
        #  -- reset
        Loot(19, L.Phenix1, 8, (1, 3), ResourcePacket(Resources.ReincarnationToken(0)),
             (Chaingun, Archer, Follet, Arrow, Shield, Guard, Guard)),
        # --- End test day 2 ---
        ],

    GoldenChest: [
        Loot(8, L.Horse2, 6, None, ResourcePacket(Resources.ReincarnationToken(5)),
             (Follet, Healer, Maraudeur, Guard, Guard, Maraudeur, Chariot)),
        Loot(8, L.Horse3, 6, 5, ResourcePacket(), (Hunter, Maraudeur, Arrow, Shield, Brute, Follet, Archer, Archer)),
        Loot(19, L.Phenix1, 8, (0, 1), ResourcePacket(Resources.ReincarnationToken(1)), (Hunter, Maraudeur, Maraudeur, Alchimist, Alchimist, AttackBoost, Scout, Healer)),
        # --- Test day 1 ---
        Loot(19, L.Phenix1, 8, (0, 0), ResourcePacket(Resources.ReincarnationToken(3)),
             (Follet, Berserk, Ice, Arrow, Guard, LifeBoost, Alchimist, Scout)),
        # -- reset
        Loot(19, L.Phenix1, 8, (0, 1), ResourcePacket(Resources.ReincarnationToken(2)),
             (Landmine, Charrette, Scout, Scout, Alchimist, Maraudeur, Maraudeur, Hunter)),
        # -- reset
        Loot(19, L.Phenix1, 8, (0, 2), ResourcePacket(Resources.ReincarnationToken(0)),
             (Scout, Scout, Follet, Berserk, Maraudeur, Maraudeur, Maraudeur, Maraudeur)),
        #  -- reset
        Loot(19, L.Phenix1, 8, (0, 3), ResourcePacket(Resources.ReincarnationToken(0)), (Hunter, Drone, Scout, Momie, Alchimist, Berserk, Guard, ModuleBoost)),
        # --- End test day 1 ---
        # --- Test day 2 ---
        Loot(19, L.Phenix1, 8, (0, 0), ResourcePacket(Resources.ReincarnationToken(4)),
             (Follet, Maraudeur, Hunter, Arrow, Shield, Shield, Shield, Lutin)),
        #  -- reset
        Loot(19, L.Phenix1, 8, (0, 1), ResourcePacket(Resources.ReincarnationToken(1)),
             (Sword, Archer, Archer, Guard, Drone, Drone, Hunter, Arrow)),
        #  -- reset
        # --- End test day 2 ---
        Loot(19, L.Phenix1, 8, (0, 4), ResourcePacket(Resources.ReincarnationToken(4)), (Drone, Sparte, Chariot, Chaman, Archer, Scout, Alchimist, Healer))

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
