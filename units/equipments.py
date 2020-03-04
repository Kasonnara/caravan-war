from typing import Tuple
from common.cards import Card


class Equipement(Card):
    def __init__(self, level=1, effects: Tuple[object] = ()):
        self.effects = effects
        self.level = level

    @property
    def bonus_factor(self):
        return 0.02 * 1.15 ** (self.level-1)  # FIXME how level impact the bonus factor?


class Weapon(Equipement):
    pass


class Armor(Equipement):
    pass

