from cards import Rarity
from units.base_units import AOE, COE, BaseUnitType, register_unit_type
from target_types import TargetType


class ModuleWeapon(BaseUnitType):
    cost = 1


@register_unit_type('Weapons')
class Balista(ModuleWeapon):
    attack_base = 53
    # _u_attack = {5: 93, 6: 107}
    atk_speed = 2
    range = 7
    armor_piercing = 0
    shoot_to = TargetType.AIR_GROUND
    rarity = Rarity.Common


@register_unit_type('Weapons')
class Mortar(AOE, ModuleWeapon):
    attack_base = 115
    # _u_attack = {5: 201, 6:231}
    atk_speed = 0.4
    range = 8
    armor_piercing = 0
    shoot_to = TargetType.GROUND
    rarity = Rarity.Rare


@register_unit_type('Weapons')
class Shotgun(COE, ModuleWeapon):
    attack_base = 77
    # _u_attack = {5: 135, 6: 155}
    atk_speed = 0.8
    range = 6
    armor_piercing = 0
    shoot_to = TargetType.AIR
    rarity = Rarity.Rare


@register_unit_type('Weapons')
class Chaingun(ModuleWeapon):
    attack_base = 125
    # _u_attack = {5: 220, 6: 253}
    atk_speed = 2
    range = 7
    armor_piercing = 3
    shoot_to = TargetType.AIR_GROUND
    rarity = Rarity.Epic


@register_unit_type('Weapons')
class Laser(ModuleWeapon):
    attack_base = 86
    # _u_attack = {1: 86}
    atk_speed = 2
    range = 7
    armor_piercing = 6
    shoot_to = TargetType.AIR_GROUND
    rarity = Rarity.Epic


@register_unit_type('Weapons')
class FlameTrower(COE, ModuleWeapon):
    attack_base = 43
    # _u_attack = {1: 43}
    atk_speed = 2
    range = 4
    armor_piercing = 0
    shoot_to = TargetType.AIR_GROUND
    rarity = Rarity.Epic


@register_unit_type('Weapons')
class Tesla(COE, ModuleWeapon):
    attack_base = 144
    # _u_attack = {1: 144, 2: 166, 3: 191, 4: 191, 5: 253, 6: 291}
    atk_speed = 1
    range = 7
    armor_piercing = 0
    shoot_to = TargetType.AIR_GROUND
    multiple_target_limit = 4
    rarity = Rarity.Legendary

    @classmethod
    def damage_formule(cls, attacker, target, attacker_level=1, star=0):
        return super().damage_formule(attacker, target, attacker_level, star) * (1.7 if target.is_summoned else 1)
