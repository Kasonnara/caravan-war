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
from typing import List, Type, Tuple

from common.leagues import Rank
from common.rarity import Rarity
from common.resources import ResourcePacket, ResourceQuantity, Resources
from lang.languages import TranslatableString
from spells.common_spell import Spell
from units.base_units import MovableUnit
from utils.prettifying import Displayable


class Chest(Displayable):
    """Represent an in-game chest and its loot"""
    number_of_card: int = None
    _average_gold_base = None
    _average_goods_base = None
    _average_loot: ResourcePacket = None
    max_reincarnation_token = None

    @classmethod
    def average_loot(cls, rank=Rank.NONE):
        # TODO idea: make Chest inherit from ResourcePacket.
        #  rank if necessary would be given to __init__
        #  Enables to seamlessly open chest just by adding them to other resource packets
        loot = cls._average_loot
        # Gold and goods are not included in _average_loot as their value depend on the rank
        if cls._average_goods_base is not None:
            loot = loot + Resources.Goods(cls._average_goods_base * rank.traiding_base)
        if cls._average_gold_base is not None:
            loot = loot + Resources.Gold(cls._average_gold_base * rank.traiding_base)
        return loot
    # FIXME spells doesn't have the same looting stats
    # FIXME reincarnation tokens have weird loot conditions
    # FIXME loot chance aren't equal between all units


class WoodenChest(Chest):
    number_of_card = 5
    _average_loot = ResourcePacket(
        ResourceQuantity(Rarity.Rare, 2/35),
        ResourceQuantity(Rarity.Common, 4 + 33 / 35),
        #Resources.ReincarnationToken(1),
        )
    max_reincarnation_token = 3
    __display_name = TranslatableString("Wooden chest", french="Coffre en bois")


class IronChest(Chest):
    number_of_card = 6
    _average_loot = ResourcePacket(
        ResourceQuantity(Rarity.Rare, number_of_card * (3/10)),
        ResourceQuantity(Rarity.Common, number_of_card * (7/10)),
        # Resources.ReincarnationToken(2),
        )
    max_reincarnation_token = 3
    __display_name = TranslatableString("Iron chest", french="Coffre en fer")


class SilverChest(Chest):
    number_of_card = 7
    _average_loot = ResourcePacket(
        ResourceQuantity(Rarity.Legendary, 3 / 100),
        ResourceQuantity(Rarity.Epic, 18 / 100),
        ResourceQuantity(Rarity.Rare, 1 + (579/100) * (2/10)),
        ResourceQuantity(Rarity.Common, (579/100) * (8/10)),
        # Resources.ReincarnationToken(2.5),
        )
    max_reincarnation_token = 4
    __display_name = TranslatableString("Silver chest", french="Coffre argenté")


class GoldenChest(Chest):
    number_of_card = 8
    _average_loot = ResourcePacket(
        ResourceQuantity(Rarity.Legendary, 7 / 100),
        ResourceQuantity(Rarity.Epic, 42 / 100),
        ResourceQuantity(Rarity.Rare, 1 + (651 / 100) * (3 / 10)),
        ResourceQuantity(Rarity.Common, (651 / 100) * (7 / 10)),
        # Resources.ReincarnationToken(4),
        )
    max_reincarnation_token = 5
    __display_name = TranslatableString("Golden chest", french="Coffre doré")


class RecycleChest(Chest):
    required_sacrifice = 100
    recyclable_types: List[Tuple[ResourceQuantity.VALID_RESOURCE_TYPE, int]] = [
        ((MovableUnit, Rarity.Common), 2),
        ((MovableUnit, Rarity.Rare),   6),
        ]  # FIXME this should include heroes!!
    number_of_card = 5
    _average_loot = ResourcePacket(
        ResourceQuantity(Spell, 3),
        )
    _average_gold_base = 0.75
    _average_goods_base = 1.5
    __display_name = TranslatableString("Recycle chest", french="Coffre de recyclage")


class RaidChest(SilverChest):
    __display_name = TranslatableString("Raid chest", french="Coffre d'embuscade")
    # TODO assert that RaidChests are in fact exactly equals to SilverChests


# TODO Epic chest

# TODO Legendary chest

# TODO Super Legendary chest

ALL_CHESTS: List[Type[Chest]] = [GoldenChest, SilverChest, IronChest, WoodenChest, RaidChest, RecycleChest]
"""List all defined chests class"""
