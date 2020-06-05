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

from collections import namedtuple, defaultdict
from typing import List, Type, Dict, Set, Union

from common.rarity import Rarity
from common.resources import ResourcePacket
from utils.class_property import classproperty

Upgrade = namedtuple('Upgrade', 'costs requirements')

MAX_LEVEL = 30


class Upgradable:
    upgrade_costs: List[ResourcePacket] = []
    # FIXME: fill <get_upgrade> for all unit and all level, or find an approximation formula
    #        to predict it (cf economy/analyse_costs.py)
    base_building: 'Type[Building]' = None
    base_building_level = 1
    sub_levels_per_level = 1
    """Number of upgradable level per basebuilding level (Specific to heroes)"""

    # Following parameter will be later defined for category base classes by the register_card_in_module call
    category: str = None

    def __init__(self, level=1):
        assert 0 <= level <= MAX_LEVEL * self.sub_levels_per_level, "Level should be in range [0;{}], {} is forbidden".format(MAX_LEVEL * self.sub_levels_per_level, level)
        self.level = level

    @classmethod
    def _get_upgrade(cls, level):
        """
        Return an Upgrade named tuple containing the costs and requirement for upgrading from <level> to <level> + 1

        Note: Even if this would cause no problem in most case, the Upgrade object never contain requirements of level 0
              because such requirement would always been met. Then you do not need to check for it.
        :param level: int [0;MAX_LEVEL[, to level to upgrade from
        :return: named tuple Upgrade{goods_cost: int, gold_cost: int, requirements: List[Upgradable]}
        """
        # Note: this function apply to any upgradable item, except the HeadQuarters that re-implement the function.

        # Note: for the attribute upgrade_costs (and upgrade_requirements in the case of the HQ) as long as I don't find
        #       a formula to automatically define them at any level, and thus as long as I have to hardcode them, I took
        #       the option of storing them directly in their final form (ResourcePacket instances or Building instances)
        #       this may lead to little more memory usage at the benefit of not having to recreate them at each usage.
        #       Either way I think this is inconsequential, but if in the future we experiment memory problem it can
        #       still be changed.

        assert 0 <= level < MAX_LEVEL, "Level should be in range [0;{}], {} is forbidden".format(MAX_LEVEL-1, level)
        assert level < len(cls.upgrade_costs), "{} upgrade_costs attribute is not implemented for level {}".format(cls.__name__, level)

        return Upgrade(
            cls.upgrade_costs[level],                                # - paying gold and goods costs
            ([cls(level)] if level > 0 else [])                      # - previous level (except for 0 -> 1)
            + [cls.base_building(level//cls.sub_levels_per_level + cls.base_building_level)],  # - the base building of the same level
            )

    def get_next_upgrade(self):
        """
        Return an Upgrade named tuple containing the costs and requirement for upgrading this unit to the next level
        (``self.level`` to ``self.level + 1``)

        *WARNING: this will not work for units at level max*

        :return: named tuple Upgrade{goods_cost: int, gold_cost: int, requirements: List[Upgradable]}
        """
        return self._get_upgrade(self.level)

    def get_previous_upgrade(self):
        """
        Return an Upgrade named tuple containing the costs and requirement for upgrading to this unit from the previous
        level (``self.level - 1`` to ``self.level``)

        *WARNING: this will not work for units at level 0*

        :return: named tuple Upgrade{goods_cost: int, gold_cost: int, requirements: List[Upgradable]}
        """
        return self._get_upgrade(self.level - 1)

    def __eq__(self, other: 'Upgradable'):
        """
        WARNING: Currently the equality is only used in recursive upgrade cost evaluation to search for duplicates of
        the same unit type and level. In this use case; stars, items and other attributes are not relevant and then are
        not included in the equality function. If you need a more precise equality function, the function must be
        reimplemented first.
        :param other:
        :return: bool, True if other is the same unit/building/spell class and has the same level
        """
        return type(self) is type(other) and self.level == other.level

    def __hash__(self):
        """
        Return a hash that take into account the final class used and the level of the unit

        WARNING: Currently the hash is only used in recursive upgrade cost evaluation to search for duplicates of
        the same unit type and level. In this use case stars, items and other attributes are not relevant and then are
        not included in the hash function. If you need a more precise hash function, the hash function will need to be
        reimplemented first.

        :return: int, the hash of the object
        """
        # TODO: if we need faster hash, it is possible to give to each class an ID using the register_card_type decorator
        #       and then crate a hash by ((id * id_max + level) * level_max + star) * level_max + ...
        return hash((type(self), self.level))

    def __repr__(self):
        return "{}[lvl={}]".format(self.__class__.__name__, self.level)

    @classmethod
    def total_upgrade_cost(cls, required_items: List['Upgradable'], inital_items: Union[Dict['CardCategories', Set['Upgradable']], List['Upgradable']], verbose=False) -> ResourcePacket:
        """
        Compute the total resources needed to upgrade from <inital_items> to <required_cards>
        :param required_items: List[Upgradable], the list of unit/building that we want to upgrade
        :param inital_items: Dict[CardCategories, Set[Upgradable]], the dictionary of already built items (MY_CARDS like)
        :return: ResourcePacket
        """

        # Genreate the
        built_items = defaultdict(lambda: 1)
        """default dictionary of built items: {upgradable class: level}"""

        if isinstance(inital_items, dict):
            for categories in inital_items:  # TODO maybe add a filter to exclude categories useless for the given requirements
                for upgradable_item in inital_items[categories]:
                    assert isinstance(upgradable_item, cls), "<inital_cards> dict must contain elements of elements that are subclass of Upgradable; but {} was found".format(type(upgradable_item))
                    assert type(upgradable_item) not in built_items.keys(), "<initial_cards> shouldn't contains duplicates"
                    built_items[type(upgradable_item)] = upgradable_item.level
        else:
            # inital_items is a list
            for upgradable_item in inital_items:
                assert isinstance(upgradable_item, cls), "<inital_cards> list must contain elements that are subclass of Upgradable; but {} was found".format(type(upgradable_item))
                built_items[type(upgradable_item)] = max(upgradable_item.level, built_items[type(upgradable_item)])

        total_costs = ResourcePacket()
        required_items = list(required_items)  # TODO: maybe replacing with a set is more efficient?
        """A queue to store items that still need to be done"""

        # Compute item upgrade costs until the queue is empty
        while len(required_items):
            # Extract from the process queue a requirement to consider
            requirement = required_items.pop()
            # Process all the missing levels for this upgradable
            for requirement_level in range(built_items[type(requirement)], requirement.level):
                requirement_cost, requirement_dependencies = requirement._get_upgrade(requirement_level)
                if verbose:
                    #print(built_items)
                    print("need {}: {}".format("{}[{}->{}]".format(type(requirement).__name__, requirement_level, requirement_level+1),
                                               (requirement_cost, requirement_dependencies)))
                    #time.sleep(2)
                # Add-up the upgrade cost
                total_costs = total_costs + requirement_cost
                # Put dependencies in the process queue
                required_items = required_items + requirement_dependencies
            built_items[type(requirement)] = max(requirement.level, built_items[type(requirement)])

        return total_costs


class Card(Upgradable):
    rarity: Rarity = None

    def __init__(self, level=1):
        super().__init__(level)
        self._repr = None

    @classproperty
    def gem_cost(cls):  # TODO: refactor to store_cost
        return cls.rarity.gem_cost

    @classmethod
    def gold_cost(cls, ligue: 'Ligue'):
        return cls.rarity.gold_cost(ligue)
