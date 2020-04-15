#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This module implement resources types.

In fact for most resources, it's just an integer encapsulated in an object. But each resource have it's own class to get
more clarity when exchanging resources between multiple submodules implemented separately and detect errors when trying
to add different resources.

When outputting resources from a system, it's recommended to use these classes, but feel free to use regular integers
for computations inside the system itself. If you need to output/add many arbitrary resources look at the ResourcePacket
class.


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

from collections import defaultdict
from enum import Enum, auto

from typing import Type, Union, List, Tuple

_meta_unit_list = ['', 'K', 'M', 'B']
"""~= No meta unit, thousand, million, billion"""


class ResourceQuantity:
    """
    A class for manipulating resource quantity while asserting we do not add cats and dogs.
    It enable adding/substracting resources of the same type and/or integers.

    It doesn't aim for computation heavy process but for clarity instead. For consequent computation inside a process
    just use integers.
    """

    def __init__(self, type: 'Resources', quantity: int):
        self.type = type
        self.quantity = quantity

    def __add__(self, other: Union['ResourceQuantity', int]):
        if type(other) is int:
            return type(self)(self.quantity + other)

        assert self.type is other.type, "Cannot add resources of different types"
        return type(self)(self.type, self.quantity + other.quantity)

    def __sub__(self, other: Union['ResourceQuantity',int]):
        if type(other) is int:
            return type(self)(self.quantity - other)

        assert self.type is other.type, "Cannot add resources of different types"
        return type(self)(self.type, self.quantity - other.quantity)

    def __repr__(self):
        return "{}[{}]".format(self.type.name, self.quantity)

    def prettify(self) -> str:
        """
        Format the resource like these examples: "156.2K Gold", "3 CapacityToken", "3.59B Goods"
        :return: str
        """
        # Find the closest meta unit
        for k, meta_unit in enumerate(_meta_unit_list):
            meta_unit_base = 1000 ** k
            if self.quantity < 1000 * meta_unit_base:
                return "{}{} {}".format(round(self.quantity / meta_unit_base), meta_unit, self.type.name)
        else:
            return "{}{} {}".format(round(self.quantity / meta_unit_base, 2), _meta_unit_list[-1], self.type.name)


class Resources(Enum):
    """
    Enumeration of all the collectible resources.
    Each item in the enum can be called to generate the corresponding ResourceQuantity object (ex: Gold(1254) )

    It doesn't aim for computation heavy process or memory savings, but for clarity instead. For consequent computation
    inside a process just use integers.
    """
    Gold = auto()
    Goods = auto()
    Gem = auto()

    LegendarySoul = auto()
    ReincarnationToken = auto()
    HeroExperience = auto()
    CapacityToken = auto()
    DalvirSoul = auto()
    ZoraSoul = auto()
    GhohralSoul = auto()
    AilulSnowsingerSoul = auto()
    MardonDarkflameSoul = auto()

    LifePotion = auto()
    # BanditShieldSeconds = auto()

    BeginnerGrowth = auto()
    VIP = auto()

    def __call__(self, quantity: int):
        return ResourceQuantity(self, quantity)


class ResourcePacket(defaultdict):
    """
    A ResourcePacket is basically a defaultdict taking any item of the Resources Enum as key, and integers as value.

    It additionally implements basic operation: addition, subtraction of ResourcePacket or ResourceQuantity and display.

    It doesn't aim for computation heavy process or memory savings, but for clarity instead. For heavy computation
    inside a process just use new specialized data types.
    """
    def __init__(self, *initial_resources: Union[ResourceQuantity, int]) -> None:
        # TODO add the possibility to provide <initial_resources> as a dictionary or ResourcePacket objects
        #      or to provide kwargs.
        super().__init__(int)

        for k, resource in enumerate(initial_resources):
            if k == 0 and type(resource) is int:
                resource = Resources.Goods(resource)
            if k == 1 and type(resource) is int:
                resource = Resources.Gold(resource)

            assert type(resource) is ResourceQuantity
            if resource != 0:
                self[resource.type] += resource.quantity

    def __add__(self, other):
        result = self.copy()

        if type(other) is type(self):
            # Addition of two ResourcePack
            for key in other:
                result[key] += other[key]
        elif isinstance(other, ResourceQuantity):
            # Addition of one resource to a ResourcePack
            result[other.type] += other.quantity
        else:
            raise ValueError("<other> must be of type ResourcePacket or ResourcesQuantity, not {}".format(type(other)))

        return result

    def __sub__(self, other):
        result = self.copy()

        if type(other) is type(self):
            # Addition of two ResourcePack
            for key in other:
                result[key] -= other[key]
        elif isinstance(other, ResourceQuantity):
            # Addition of one resource to a ResourcePack
            result[other.type] -= other.quantity
        else:
            raise ValueError("<other> must be of type ResourcePacket or ResourcesQuantity, not {}".format(type(other)))

        return result

    def prettify(self, exact_value=False):
        return '\n'.join(
            ["- " +
             ("{} {}".format(self[key], key.name) if exact_value else key(self[key]).prettify())
             for key in self])


def resourcepackets_gold(*golds: int):
    """Alias function for easily creating list of ResourcePacket (with only gold) when defining units upgrade_costs"""
    return list(ResourcePacket(0, gold) for gold in golds)


def resourcepackets_goods(*goodss: int):
    """Alias function for easily creating list of ResourcePacket (with only goods) when defining units upgrade_costs
    """
    return list(ResourcePacket(goods, 0) for goods in goodss)


def resourcepackets(*goods_golds_tuples: Tuple[int, int]):
    """Alias function for easily creating list of ResourcePacket when defining units upgrade_costs
    """
    return list(ResourcePacket(goods, gold) for goods, gold in goods_golds_tuples)
