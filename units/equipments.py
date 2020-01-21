from typing import Tuple
from cards import Card


class Equipement(Card):
    def __init__(self, level, equipements:Tuple[object] = ()):
        self.equipements = equipements
        self.level = level

class Weapon(Equipement):
    pass


class Armor(Equipement):
    pass

