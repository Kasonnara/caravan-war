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
from collections import namedtuple
from typing import Tuple

from cards import Gold, Goods, LifePotion, Gem, ReincarnationToken, AmeLegendaire, BanditShieldProtection, Croissance
from spells import AttackSpeedBoost, Landmine, AttackBoost, Meteor, LifeBoost, Poison, Arrow, SpeedBoost
from units.bandits import Drone, Archer, Brute, Maraudeur, Hunter, Berserk, Spider, Alchimist, Lutin
from units.guardians import Scout, Guard, Healer, Follet, Shield, Knight, Sword
from units.vehicules import Charrette, Helicopter, Chariot
from units.weapons import Balista, Mortar, Shotgun, Chaingun
from ligues import Ligue as L

class Chest:
    number_of_card = None  # TODO property based on loot_example
    loot_example = None
    available_loot_categories = None  # TODO property based on loot_example


Loot = namedtuple('Loot', 'HQ_level ligue vip index cards')
"""Memorise a chest loot result as well as looting current conditions (HQ looting, vip level and ligue level) 
for later analise (index is used for campaign, daily and weekly quests chest)"""
# TODO split card loots, ressources loots and shield loots


class RecycleChest(Chest):
    number_of_card = 5
    loot_example = [
        Loot(8, "Cheval 2", 6, None, (Gold(6816), Goods(10103), AttackSpeedBoost, Landmine, Landmine)),
        Loot(8, "Cheval 3", 6, None, (Gold(6859), Goods(17576), SpeedBoost, Landmine, LifeBoost)),
        Loot(8, "Chameau 1", 6, None, (Gold(6339), Goods(22964), SpeedBoost, Arrow, LifeBoost)),
        ]


class Exchange10km(Chest):
    # Wood Chest
    number_of_card = 5
    loot_example = [
        Loot(8, L.Horse2, 6, None, (ReincarnationToken(1), Drone, Archer, Archer, Archer, Balista)),
        Loot(8, L.Horse2, 6, None, (Scout, Scout, Archer, Archer, Balista)),
        Loot(8, L.Horse3, 6, None, (Maraudeur, Follet, Guard, Guard, Guard)),
        Loot(8, L.Horse3, 6, None, (Maraudeur, Maraudeur, Balista, Spider, AttackBoost)),
        Loot(8, L.Horse3, 6, None, (Scout, Scout, Shotgun, Drone, Follet)),
        Loot(8, L.Horse3, 6, None, (Maraudeur, Scout, Maraudeur, Scout, Guard)),
        Loot(8, L.Horse3, 6, None, (Meteor, Drone, Drone, Archer, Balista)),
        ]



class Exchange100km(Chest):
    # Iron chest
    number_of_card = 6
    loot_example = [
        Loot(8, L.Horse3, 6, None, (ReincarnationToken(2), Spider, Charrette, Follet, Maraudeur, Guard, Guard)),
        Loot(8, L.Horse3, 6, None, (ReincarnationToken(1), Maraudeur, Drone, Drone, Archer, Archer, Archer)),
        Loot(8, L.Horse3, 6, None, (Scout, Guard, Knight, LifeBoost, Archer, Archer)),
        ]


class Exchange1000km(Chest):
    # Silver chest
    number_of_card = 7
    loot_example = [
        Loot(8, L.Horse2, 6, None, (Mortar, Berserk, Charrette, Maraudeur, Maraudeur, Archer, Landmine)),
        Loot(8, L.Horse2, 6, None, (Shield, Knight, Sword, Archer, Scout, Scout, Guard)),
        Loot(8, L.Horse2, 6, None, (ReincarnationToken(2), Maraudeur, Maraudeur, Archer, Alchimist, Scout, Maraudeur, Alchimist)),
        ]


class BestExchange(Chest):
    # Gold Chest
    # 1 rare minimum
    # Epic 42 %
    # Legendary 7%
    number_of_card = 8
    loot_example = [
        Loot(8, "Cheval 2", 6, None, (ReincarnationToken(5), Follet, Healer, Maraudeur, Guard, Guard, Maraudeur, Chariot)),
        ]


class RaidChest(Chest):
    # At least 1 Rare
    # Legendary: 3%
    # Epic: 18%
    number_of_card = 7
    loot_example = [
        Loot(8, L.Horse2, 6, None, (ReincarnationToken(2), Charrette, Helicopter, Brute, Maraudeur, Hunter, Archer, Guard, BanditShieldProtection)),
        Loot(8, L.Horse3, 6, None, (ReincarnationToken(2), Chaingun, Maraudeur, Scout , Scout, Poison, Lutin, Berserk)),
        ]


class DailyQuest(Chest):
    # for DailyQuest chest index means the chest index in the list
    loot_example = [
        Loot(8, L.Horse3, 6, 2, (Gold(10000), Croissance(20))),
        Loot(8, L.Horse3, 6, 3, (Goods(10000),  Croissance(20), Hunter)),
        Loot(8, L.Horse3, 6, 4, (Gold(10000), Croissance(20), Healer)),
        Loot(8, L.Horse3, 6, 5, (Gem(20), LifePotion(1), Croissance(20))),
        Loot(8, L.Horse3, 6, 1, (Goods(10000), Croissance(20))),
        Loot(8, L.Horse3, 6, 2, (Gold(10000), Croissance(20))),
        Loot(8, L.Horse3, 6, 3, (Goods(10000), Croissance(20), Alchimist)),
        Loot(8, L.Horse3, 6, 4, (Gold(10000), Croissance(20), Shield)),
        Loot(8, L.Camel1, 6, 5, (Gem(20), LifePotion(1), Croissance(20))),
        ]


class WeklyQuest(Chest):
    # for WeklyQuest chest index means the chest index in the list
    loot_example = [
        Loot(8, L.Horse3, 6, 4, (Gold(30000), LifePotion(5), Croissance(60))),
        Loot(8, L.Horse3, 6, 5, (Gold(50000), Gem(100), Croissance(60))),
        ]


class Campaign(Chest):
    # for campaign chest index means the compaign index
    loot_example = [
        # Gold Chest
        # 1 rare minimum
        # Epic 42 %
        # Legendary 7%
        Loot(8, L.Horse3, 6, 5, (Hunter, Maraudeur, Arrow, Shield, Brute, Follet, Archer, Archer))
        ]


class Raid(Chest):
    # For raid chest: index means the number of stars won
    loot_example = [
        Loot(8, L.Horse2, 6, 3, (Gem(24), LifePotion(1))),
        Loot(8, L.Horse2, 6, 3, (LifePotion(1), ReincarnationToken(3))),
        Loot(8, L.Horse2, 6, 3, (Gem(25), LifePotion(1), ReincarnationToken(3), AmeLegendaire(3))),
        Loot(8, L.Horse2, 6, 3, (LifePotion(1), AmeLegendaire(2))),
        Loot(8, L.Horse3, 6, 3, (ReincarnationToken(3))),
        ]
