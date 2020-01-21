from typing import Union, List, Optional

from class_property import classproperty
from target_types import TargetType
from units.base_units import BaseUnitType, register_unit_type, AOE, Heal, damage_formule


class Tower(BaseUnitType):
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


@register_unit_type('Towers')
class Sentinelle(Tower):
    attack_base = 72
    # _u_attack = {5: 125, 6: 144}
    atk_speed = 1.6
    range = 9
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = 150
    parent_tower = None


@register_unit_type('Towers')
class Arbalete(Tower):
    attack_base = 100
    # _u_attack = {5: 175, 6: 201}
    atk_speed = 1.6
    range = 11
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = 160
    parent_tower = Sentinelle
    multiple_target_limit = 2


@register_unit_type('Towers')
class Eolance(Tower):
    attack_base = 538
    # _u_attack = {1: 535}
    atk_speed = 0.6
    range = 11
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = None
    parent_tower = Arbalete


@register_unit_type('Towers')
class Sniper(Tower):
    attack_base = 330
    # _u_attack = {1: 330}
    atk_speed = 0.5
    range = 13
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = None
    parent_tower = Sentinelle


@register_unit_type('Towers')
class HeavySniper(Tower):
    attack_base = 200
    # _u_attack = {1: 200}
    atk_speed = 1.5
    range = 13
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = None
    parent_tower = Sniper


@register_unit_type('Towers')
class Mage(Tower):
    attack_base = 85
    # _u_attack = {5: 151, 6: 174}
    atk_speed = 1.2
    range = 8
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 6
    _cost = 150
    parent_tower = None


@register_unit_type('Towers')
class Lightning(Tower):
    attack_base = 137
    # _u_attack = {5: 240, 6: 276}
    atk_speed = 0.8
    range = 8
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 6
    _cost = 175
    parent_tower = Mage
    multiple_target_limit = 8

    @classmethod
    def damage_formule(cls, target, target_index, attacker_level=1, star=0):
        #return super().damage_formule(target, target_index, attacker_level) * (0.75 ** target_index)
        return super().damage_formule(target, target_index, attacker_level, star=star) * (0.25 * max(0, 4 - target_index))


@register_unit_type('Towers')
class Stormspire(Tower, AOE):
    attack_base = 0
    # _u_attack = {1: 0}
    atk_speed = 0.25
    range = 3.5
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 6
    _cost = 200
    parent_tower = Lightning


@register_unit_type('Towers')
class Fire(Tower):
    attack_base = 130
    # _u_attack = {1: 130}
    atk_speed = 2
    range = 8
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 2
    _cost = 160
    parent_tower = Mage


@register_unit_type('Towers')
class Bomber(AOE, Tower):
    attack_base = 88
    # _u_attack = {5: 159, 6: 183}
    atk_speed = 0.4
    range = 10
    shoot_to = TargetType.GROUND
    armor_piercing = 0
    _cost = 170
    parent_tower = None


@register_unit_type('Towers')
class Canon(Tower):
    attack_base = 184
    # _u_attack = {1: 184}
    atk_speed = 0.5
    range = 10
    shoot_to = TargetType.GROUND
    armor_piercing = 0
    _cost = 120
    parent_tower = Bomber
    multiple_target_limit = 3


@register_unit_type('Towers')
class Hydra(Tower):
    attack_base = 200
    # _u_attack = {1: 125}
    atk_speed = 1
    range = 150
    shoot_to = TargetType.AIR_GROUND
    armor_piercing = 0
    _cost = 280
    parent_tower = Canon


@register_unit_type('Towers')
class MissileLaucher(AOE, Tower):
    attack_base = 240
    # _u_attack = {1: 240, 5: 383, 6: 433}
    atk_speed = 0.8
    range = 12
    shoot_to = TargetType.AIR
    armor_piercing = 0
    _cost = 80
    parent_tower = Bomber


@register_unit_type('Towers')
class Hospital(AOE, Heal, Tower):
    heal_base = 20
    #_u_heal = {1: 20, 5: 35, 6: 40}
    heal_atk_speed = 1
    range = None
    shoot_to = TargetType.AIR_GROUND
    _cost = 120
    parent_tower = None

    #def dps(cls, targets: Union['MovableUnit', List['MovableUnit']], attacker_level: int = 1) -> None:
    #    return None


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
