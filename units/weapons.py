from typing import Union, Type

from cards import Rarity
from units.base_units import AOE, COE, BaseUnitType, register_unit_type, reincarnation
from target_types import TargetType
from units.equipments import Weapon


class ModuleWeapon(BaseUnitType):
    cost = 1


@register_unit_type('Weapons')
class Balista(ModuleWeapon):
    attack_base = 53
    atk_speed = 2
    range = 7
    armor_piercing = 0
    shoot_to = TargetType.AIR_GROUND
    rarity = Rarity.Common


@register_unit_type('Weapons')
class Mortar(AOE, ModuleWeapon):
    attack_base = 115
    atk_speed = 0.4
    range = 8
    armor_piercing = 0
    shoot_to = TargetType.GROUND
    rarity = Rarity.Rare


@register_unit_type('Weapons')
class Shotgun(COE, ModuleWeapon):
    attack_base = 77
    atk_speed = 0.8
    range = 6
    armor_piercing = 0
    shoot_to = TargetType.AIR
    rarity = Rarity.Rare


@register_unit_type('Weapons')
class Chaingun(ModuleWeapon):
    attack_base = 125
    atk_speed = 2
    range = 7
    armor_piercing = 3
    shoot_to = TargetType.AIR_GROUND
    rarity = Rarity.Epic
    anti_air_bonus = 1.5

    @classmethod
    def damage_formule(cls, target: Union['MovableUnit', Type['MovableUnit']], attacker_level=1, stars=0,
                       weapon: Weapon = None, target_index=0):
        return super().damage_formule(target, attacker_level, stars, weapon, target_index) * (1 if target.shooted_as is TargetType.GROUND else cls.anti_air_bonus)


@register_unit_type('Weapons')
@reincarnation
class ChaingunLeg(Chaingun):
    multiple_target_limit = 2
    # FIXME the 2nd target must be at less than 1m
    anti_air_bonus = 1.6

    @classmethod
    def damage_formule(cls, target: Union['MovableUnit', Type['MovableUnit']], attacker_level=1, stars=0,
                       weapon: Weapon = None, target_index=0):
        return super().damage_formule(target, attacker_level, stars, weapon, target_index) * max(1 - 0.5 * target_index, 0)


@register_unit_type('Weapons')
class Laser(ModuleWeapon):
    attack_base = 86
    atk_speed = 2
    range = 7
    armor_piercing = 6
    shoot_to = TargetType.AIR_GROUND
    rarity = Rarity.Epic


@register_unit_type('Weapons')
class FlameTrower(COE, ModuleWeapon):
    attack_base = 43
    atk_speed = 2
    range = 4
    armor_piercing = 0
    shoot_to = TargetType.AIR_GROUND
    rarity = Rarity.Epic


@register_unit_type('Weapons')
class Tesla(COE, ModuleWeapon):
    attack_base = 144
    atk_speed = 1
    range = 7
    armor_piercing = 0
    shoot_to = TargetType.AIR_GROUND
    multiple_target_limit = 4
    rarity = Rarity.Legendary

    @classmethod
    def damage_formule(cls, target, attacker_level=1, stars=0, target_index=0, weapon=None):
        return super().damage_formule(target, attacker_level=attacker_level, stars=stars, target_index=target_index) * (1.7 if target.is_summoned else 1)
