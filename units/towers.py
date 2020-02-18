from typing import Union, List, Optional

from class_property import classproperty
from target_types import TargetType
from units.base_units import BaseUnit, register_unit_type, AOE, Heal


class Tower(BaseUnit):
    parent_tower = None
    _cost = None

    @classproperty
    def cost(cls):
        # FIXME: possible infinite recursive loop
        if cls._cost is None:
            return None
        if cls.parent_tower is None:
            return cls._cost
        else:
            assert issubclass(cls.parent_tower, Tower), "Parent ({}) is not a Tower".format(cls.parent_tower)
            return cls._cost + cls.parent_tower.cost

    @classproperty
    def gem_cost(cls):
        return cls.rarity.spell_gem_cost

    @classmethod
    def gold_cost(cls, ligue: 'Ligue'):
        return cls.rarity.spell_gold_cost(ligue)


@register_unit_type('Towers')
class Sentinelle(Tower):
    attack_base = 72
    hit_frequency = 1.6
    range = 9
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = 150
    parent_tower = None


@register_unit_type('Towers')
class Arbalete(Tower):
    attack_base = 100
    hit_frequency = 1.6
    range = 11
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = 160
    parent_tower = Sentinelle
    multiple_target_limit = 2


@register_unit_type('Towers')
class Eolance(Tower):
    attack_base = 538
    hit_frequency = 0.6
    range = 11
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = None
    parent_tower = Arbalete


@register_unit_type('Towers')
class Sniper(Tower):
    attack_base = 330
    hit_frequency = 0.5
    range = 13
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = None
    parent_tower = Sentinelle


@register_unit_type('Towers')
class HeavySniper(Tower):
    attack_base = 200
    hit_frequency = 1.5
    range = 13
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = None
    parent_tower = Sniper


@register_unit_type('Towers')
class Mage(Tower):
    attack_base = 85
    hit_frequency = 1.2
    range = 8
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 6
    _cost = 150
    parent_tower = None


@register_unit_type('Towers')
class Lightning(Tower):
    attack_base = 137
    hit_frequency = 0.8
    range = 8
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 6
    _cost = 175
    parent_tower = Mage
    multiple_target_limit = 8

    def damage_formule(self, target: 'MovableUnit', target_index=0):
        return (
            super().damage_formule(target, target_index=target_index)
            * (0.25 * max(0, 4 - target_index))  # Reduction factor
            )


@register_unit_type('Towers')
class Stormspire(Tower, AOE):
    attack_base = 0
    hit_frequency = 0.25
    range = 3.5
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 6
    _cost = 200
    parent_tower = Lightning


@register_unit_type('Towers')
class Fire(Tower):
    attack_base = 130
    hit_frequency = 2
    range = 8
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 2
    _cost = 160
    parent_tower = Mage


@register_unit_type('Towers')
class Bomber(AOE, Tower):
    attack_base = 88
    hit_frequency = 0.4
    range = 10
    shoot_to = TargetType.GROUND
    armor_piercing = 0
    _cost = 170
    parent_tower = None


@register_unit_type('Towers')
class Canon(Tower):
    attack_base = 184
    hit_frequency = 0.5
    range = 10
    shoot_to = TargetType.GROUND
    armor_piercing = 0
    _cost = 120
    parent_tower = Bomber
    multiple_target_limit = 3


@register_unit_type('Towers')
class Hydra(Tower):
    attack_base = 200
    hit_frequency = 1
    range = 150
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = 280
    parent_tower = Canon


@register_unit_type('Towers')
class MissileLaucher(AOE, Tower):
    attack_base = 240
    hit_frequency = 0.8
    range = 12
    shoot_to = TargetType.AIR
    armor_piercing = 0
    _cost = 80
    parent_tower = Bomber


@register_unit_type('Towers')
class Hospital(AOE, Heal, Tower):
    base_heal = 20
    heal_frequency = 1
    range = None
    shoot_to = TargetType.AIR_GROUND
    _cost = 120
    parent_tower = None

    def dps(self, targets: Union['MovableUnit', List['MovableUnit']]) -> Optional[float]:
        return None


@register_unit_type('Towers')
class Armory(Hospital):
    _cost = 80
    parent_tower = Hospital


@register_unit_type('Towers')
class Tambour(Hospital):
    _cost = 130
    parent_tower = Hospital


@register_unit_type('Towers')
class Garnison(Tambour, Armory):
    _cost = 190
    parent_tower = Armory
