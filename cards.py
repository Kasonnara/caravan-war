from enum import Enum, auto
from typing import Optional


class Rarity(Enum):

    # Rhino 1: 3379; base lvl 9
    Legendary = 2400, None, None, None, None
    Epic = 390, 8, None, None, None
    Rare = None, 4, 34000, 3400, 6
    Common = None, 2, None, 1700, 2

    """ Buffle 3: 2771; base lvl 8
    Legendary = 2400, None, None, None, None
    Epic = 390, 8, None, 5680, None
    Rare = None, 4, 28000, 2840, 6
    Common = None, 2, None, 1420, 2
    """

    """ Buffle 2: 2566; base lvl 8
    Legendary = 2400, None, None, None, None
    Epic = 390, 8, None, None, None
    Rare = None, 4, 24000, 2420, 6
    Common = None, 2, None, 1000, 2
    """

    """ Chameau 3: 1823 ou Buffle 1: 1962; base lvl 8
    Legendary = 2400, None, None, None, None
    Epic = 390, 8, None, 4000, None
    Rare = None, 4, 20000, 2000, 6
    Common = None, 2, None, 1000, 2
    """

    """ Chameau 3, base lvl 7
    Legendary = 2400, None, None, None, None
    Epic = 390, 8, None, 3360, None
    Rare = None, 4, 16000, 1680, 6
    Common = None, 2, None, 840, 2
    """

    """ Chameau 2
    Legendary = 2400, None, None, None, None
    Epic = 390, None, None, 2880, None
    Rare = None, None, 14000, 1440, 6
    Common = None, None, None, 720, 2
    """

    """ Chameau 1
    Legendary = 2400, None, None, None, None
    Epic = 390, 390, None, 2400, None
    Rare = None, 4, 12000, 1200, 6
    Common = None, 2, 600, 600, 2
    """

    def __init__(self, gem_cost, spell_gem_cost, gold_cost, spell_gold_cost, recycle_value):
        self.gem_cost = gem_cost
        self.spell_gem_cost = spell_gem_cost
        self.gold_cost = gold_cost
        self.spell_gold_cost = spell_gold_cost
        self.recycle_value = recycle_value


class Card:
    category: str = None
    # Fixme: replace str categories by a CardType enumeration
    gold_cost: int = None  # Fixme if it only depends on rarity, factorise code into Rarity
    gem_cost: int = None  # Fixme if it only depends on rarity, factorise code into Rarity
    rarity: Rarity = None

    def __init__(self, level: int, stars=0):
        self.level = level
        self.stars = stars



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
