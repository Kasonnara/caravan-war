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
This module implement resources types.

In fact for most resources, it's just an integer encapsulated in an object. But each resource have it's own class to get
more clarity when exchanging resources between multiple submodules implemented separately and detect errors when trying
to add different resources.

When outputting resources from a system, it's recommended to use these classes, but feel free to use regular integers
for computations inside the system itself. If you need to output/add many arbitrary resources look at the ResourcePacket
class.
"""


import itertools
from collections import defaultdict
from enum import Enum, auto

from typing import Type, Union, List, Tuple, Iterable

from utils.prettifying import human_readable


class ResourceQuantity:
    """
    A class for manipulating resource quantity while asserting we do not add cats and dogs.
    It enable adding/substracting resources of the same type and/or integers.

    It doesn't aim for computation heavy process but for clarity instead. For consequent computation inside a process
    just use integers.
    """
    VALID_RESOURCE_TYPE = Union['Resources', Type['Card'], Tuple[Type['Card'], 'Rarity'], 'Rarity', Type['Chest']]

    def __init__(self, res_type: VALID_RESOURCE_TYPE, quantity: float):
        self.type = res_type
        self.quantity = quantity

    @staticmethod
    def compatible_types(main_type: VALID_RESOURCE_TYPE,
                         other_type: VALID_RESOURCE_TYPE):
        # Simple test for common cases where ResourceQuantity are only of type Resources enum.
        # Doesn't recognize cards or rarity and combinaison of both as valid types.
        # return main_type is other_type

        # --- new implementation ---
        # More complex test that also works for Card, rarities and (Card, Rarity) types
        # (This function is surprisingly complex just to handle that)
        if main_type == other_type:
            # match identical Resources, identical cards, identical rarities and identical tuple(card+rarirty)
            return True

        from common.rarity import Rarity
        from common.cards import Card
        from economy.chests import Chest

        # FIXME it may be better organized to only allow final unit class as types and instead use CardCategories
        #  for unspecified cards. (But currently is work fine with a simpler code)
        if isinstance(other_type, Resources):
            return False  # Should already have matched
        elif isinstance(other_type, Type):
            if issubclass(other_type, Chest):
                return False  # Should already have matched
            else:
                assert issubclass(other_type, Card)
                o_card, o_rarity = other_type, other_type.rarity
        elif isinstance(other_type, tuple):
            assert issubclass(other_type[0], Card) and isinstance(other_type[1], Rarity)
            o_card, o_rarity = other_type
        else:
            assert isinstance(other_type, Rarity)
            return False  # Should already have matched

        if isinstance(main_type, Resources):
            return False  # Should already have matched
        elif isinstance(main_type, Type):
            if issubclass(main_type, Chest):
                return False  # Should already have matched
            else:
                assert issubclass(main_type, Card)
                m_card, m_rarity = main_type, main_type.rarity
        elif isinstance(main_type, tuple):
            assert issubclass(main_type[0], Card) and isinstance(main_type[1], Rarity)
            m_card, m_rarity = main_type
        else:
            assert isinstance(main_type, Rarity)
            m_card, m_rarity = None, main_type

        # assert (m_card is not None or m_rarity is not None) and (o_card is not None or o_rarity is not None)
        return (m_rarity is None or o_rarity is m_rarity) and (m_card is None or (o_card is not None and issubclass(o_card, m_card)))

    def __add__(self, other: Union['ResourceQuantity', int, float]):
        if isinstance(other, (int, float)):
            return type(self)(self.quantity + other)
        assert type(other) is type(self), "Cannot only add ResourceQuantity or numerals to ResourceQuantity not {}".format(self.type.__class__.__name__)
        assert self.compatible_types(self.type,other.type), "Cannot add resources of different types"

        return type(self)(self.type, self.quantity + other.quantity)

    def __sub__(self, other: Union['ResourceQuantity', int]):
        if type(other) is int:
            return type(self)(self.quantity - other)

        assert type(other) is type(self), "Cannot only subtract ResourceQuantity or numerals to ResourceQuantity not {}".format(self.type.__class__.__name__)
        assert self.compatible_types(self.type, other.type), "Cannot subtract resources of different types"
        assert False, "By convention, you should not need to subtract resources all gains must be positive " \
                      "ResourceQuantity while costs must be negative ResourceQuantity from the very beginning"  # Remove this assert if you found cases where the convention cannot apply
        return type(self)(self.type, self.quantity - other.quantity)

    def __mul__(self, other: Union[int, float]):
        assert isinstance(other, (int, float))
        return type(self)(self.type, self.quantity * other)

    def __repr__(self):
        return "{}[{}]".format(self.prettify_type(self.type), self.quantity)

    @staticmethod
    def prettify_type(res_type: VALID_RESOURCE_TYPE) -> str:
        # Simple test for common cases where ResourceQuantity are only of type Resources enum.
        # Doesn't recognize cards or rarity and combinaison of both as valid types.
        #  return res_type.name
        # --- new implementation ---
        # More complex test that also works for Card, rarities and (Card, Rarity) types
        # (This function is surprisingly complex just to handle that)
        if isinstance(res_type, Resources):
            return res_type.name

        from common.rarity import Rarity
        from common.cards import Card
        from economy.chests import Chest
        if isinstance(res_type, Rarity):
            return "Unspecified{}Card".format(res_type.name)
        elif isinstance(res_type, tuple):
            assert issubclass(res_type[0], Card)
            assert isinstance(res_type[1], Rarity)
            assert res_type[0].rarity is None, "When using (CardType, Rarity) type, that card type should be a category base class not a final unit class" # and thus .rarity shouldn't be defined yet
            return "Unspecified{}{}".format(res_type[1].name, res_type[0].__name__)
        else:
            assert isinstance(res_type, Type), "Invalid resource type, expected one of: Ressources enum, Rarity enum, unit Card, a tuple(Card category base class, rarity) or a Chest. But {} was found".format(type(res_type))
            if issubclass(res_type, Chest):
                return res_type.__name__
            else:
                assert issubclass(res_type, Card), "Invalid resource type, expected one of: Ressources enum, Rarity enum, unit Card, a tuple(Card category base class, rarity) or a Chest. But {} was found".format(res_type.__name__)
                if res_type.rarity is None:
                    return "Unspecified{}".format(res_type.__name__)
                else:
                    return res_type.__name__

    def prettify(self) -> str:
        """
        Format the resource like these examples: "156.2K Gold", "3 CapacityToken", "3.59B Goods"
        :return: str
        """

        return "{value} {type}".format(value=human_readable(self.quantity), type=self.prettify_type(self.type))


class Resources(Enum):
    """
    Enumeration of all the collectible resources.
    Each item in the enum can be called to generate the corresponding ResourceQuantity object (ex: Gold(1254) )

    It doesn't aim for computation heavy process or memory savings, but for clarity instead. For consequent computation
    inside a process just use integers.
    """
    Goods = auto()
    Gold = auto()
    Gem = auto()
    Dust = auto()

    LegendarySoul = auto()
    ReincarnationToken = auto()
    CapacityToken = auto()
    DalvirSoul = auto()
    ZoraSoul = auto()
    GhohralSoul = auto()
    AilulSoul = auto()
    MardonSoul = auto()
    HeroExperience = auto()

    LifePotion = auto()
    LotteryTicket = auto()
    # BanditShieldSeconds = auto()

    BeginnerGrowth = auto()
    VIP = auto()
    Trophy = auto()

    def __call__(self, quantity: float):
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
            if k == 0 and isinstance(resource, (int, float)):
                resource = Resources.Goods(resource)
            if k == 1 and isinstance(resource, (int, float)):
                resource = Resources.Gold(resource)

            assert type(resource) is ResourceQuantity, "Must be of type ResourceQuantity not {}".format(type(resource))
            if resource != 0:
                self[resource.type] += resource.quantity

    def copy(self):
        new_dict = type(self)()
        for res_type in self:
            new_dict[res_type] = self[res_type]
        return new_dict

    def __add__(self, other):
        result = self.copy()

        if type(other) is type(self):
            # Addition of two ResourcePack
            for res_type in other:
                if other[res_type] != 0:
                    result[res_type] += other[res_type]
        elif isinstance(other, ResourceQuantity):
            # Addition of one resource to a ResourcePack
            result[other.type] += other.quantity
        else:
            raise ValueError("<other> must be of type ResourcePacket or ResourcesQuantity, not {}".format(type(other)))

        return result

    def __sub__(self, other):
        assert False, "By convention, you should not need to subtract resources, all gains must already be positive " \
                      "value while costs must be negative value from the very beginning"  # Remove this assert if you found cases where the convention cannot apply
        result = self.copy()

        if type(other) is type(self):
            # Addition of two ResourcePack
            for res_type in other:
                if other[res_type] != 0:
                    result[res_type] -= other[res_type]
        elif isinstance(other, ResourceQuantity):
            # Addition of one resource to a ResourcePack
            result[other.type] -= other.quantity
        else:
            raise ValueError("<other> must be of type ResourcePacket or ResourcesQuantity, not {}".format(type(other)))

        return result

    def __mul__(self, other: float):
        # One liner: cleaner but generate many temporary useless ResourceQuantity objects and two iteration instead of one
        # return ResourcePacket(*(ResourceQuantity(res_type, self[res_type] * other) for res_type in self))

        result = ResourcePacket()
        if isinstance(other, (int, float)):
            for res_type in self:
                result[res_type] = self[res_type] * other
        else:
            raise ValueError("ResourcePacket can only be multiplied by scalars (int/float), not {}".format(type(other)))
        return result

    def prettify(self, exact_value=False):
        return '\n'.join(
            ["- " + ("{} {}".format(self[key], ResourceQuantity.prettify_type(key))
                     if exact_value
                     else ResourceQuantity(key, self[key]).prettify())
             for key in self])

    def to_pandas(self, prettify=True) -> 'pandas.Series':
        import pandas
        return pandas.Series(
            data=[self[res_type] for res_type in self],
            index=[ResourceQuantity.prettify_type(res_type) for res_type in self] if prettify else [res_type for res_type in self],
            )

    @staticmethod
    def get_all_resource_types(resource_packets: Iterable['ResourcePacket'],
                               sort=False) -> Union[List[ResourceQuantity.VALID_RESOURCE_TYPE], List[str]]:
        """
        Return the list of all the resource types present in the given ResourcePacket Iterable

        :param resource_packets: Iterable['ResourcePacket'], a bunch of ResourcePacket to analyse.
        :param sort: bool [default False], if set to True, basic resources will be sorted first.
        """
        found_types = {res_type
                       for resource_packet in resource_packets
                       for res_type in resource_packet}
        if sort:
            # Probably not the best way to do all this. Maybe better with a `sort(key=lambda:...)`
            found_types = (
                    [basic_res_type for basic_res_type in Resources if basic_res_type in found_types]
                    + [other_type for other_type in found_types if not isinstance(other_type, Resources)]
                )
        return found_types


def resourcepackets_gold(*golds: int):
    """Alias function for easily creating list of ResourcePacket (with only gold) when defining units upgrade_costs"""
    return list((ResourcePacket(0, gold) if gold is not None else None) for gold in golds)


def resourcepackets_goods(*goodss: int):
    """Alias function for easily creating list of ResourcePacket (with only goods) when defining units upgrade_costs
    """
    return list((ResourcePacket(goods, 0) if goods is not None else None) for goods in goodss)


def resourcepackets(*goods_golds_tuples: Tuple[int, int]):
    """Alias function for easily creating list of ResourcePacket when defining units upgrade_costs
    """
    return list((ResourcePacket(*goods_gold) if goods_gold is not None else None) for goods_gold in goods_golds_tuples)


hero_souls = [Resources.ZoraSoul, Resources.DalvirSoul, Resources.GhohralSoul, Resources.AilulSoul, Resources.MardonSoul]
"""Alias that list the different hero souls"""

hero_pair_combinaisons = list(itertools.combinations(hero_souls, 2))
"""List all the possible unordered combinations of 2 hero souls"""
