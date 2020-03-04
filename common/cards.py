from typing import Optional

from common.rarity import Rarity
from utils.class_property import classproperty



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
