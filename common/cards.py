from enum import Enum, auto
from typing import Optional

from utils.class_property import classproperty


class Rarity(Enum):
    #  name   = gem card cost, gem spell card cost, ratio between 10km exchange and the cost in gold of the card, the same for spells, the value of the card when recycled
    Legendary = 2400, None, None, None, None
    Epic = 390, 8, None, 4/20, None
    Rare = None, 4, 1, 2/20, 6
    Common = None, 2, None, 1/20, 2

    def __init__(self, gem_cost, spell_gem_cost, gold_cost, spell_gold_cost, recycle_value):
        self.gem_cost = gem_cost
        """Cost of weapons, vehicules, guardians and bandits cards when purchased with gems (may be None of the card is not purchasable with gem)"""
        self.spell_gem_cost = spell_gem_cost
        """Cost of spell cards when purchased with gems (may be None of the spell is not purchasable with gem)"""
        self._gold_cost_base = gold_cost
        self._spell_gold_cost_base = spell_gold_cost
        self.recycle_value = recycle_value
        """Value of the card if it is recycled"""

    def gold_cost(self, ligue: 'Ligue') -> Optional[int]:
        """
        Cost of weapons, vehicules, guardians and bandits cards when purchased with gold
        :param ligue: The ligue rank you have when the store was reset.
        :return: int (or None of the card is not purchasable with gold)
        """
        if self._gold_cost_base is None:
            return None
        return ligue.ex10km_goods_cost * self._gold_cost_base

    def spell_gold_cost(self, ligue: 'Ligue') -> Optional[int]:
        """
        Cost of spell cards when purchased with gold
        :param ligue: The ligue rank you have when the store was reset.
        :return: int (or None of the spell is not purchasable with gold)
        """
        if self._spell_gold_cost_base is None:
            return None
        return ligue.ex10km_goods_cost * self._spell_gold_cost_base


class Card:
    category: str = None
    rarity: Rarity = None

    def __init__(self, level: int, stars=0):
        self.level = level
        self.stars = stars
        self._repr = None

    @classproperty
    def gem_cost(cls):
        return cls.rarity.gem_cost

    @classmethod
    def gold_cost(cls, ligue: 'Ligue'):
        return cls.rarity.gold_cost(ligue)


class Resources:
    category = "Resources"

    def __init__(self, quantity):
        self.quantity = quantity


class Gold(Resources):
    pass


class Goods(Resources):
    pass


class Gem(Resources):
    pass


class AmeLegendaire(Resources):
    pass


class LifePotion(Resources):
    pass


class BanditShieldProtection:
    pass


class ReincarnationToken(Resources):
    pass


class Croissance(Resources):
    pass
