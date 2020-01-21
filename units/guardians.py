from typing import Union, List

from cards import Rarity
from units.base_units import MovableUnit, Heal, AOE, register_unit_type, reincarnation
from target_types import TargetType


class Guardian(MovableUnit):
    move_speed = 1.2
    bossfight_cost = None


@register_unit_type('Guardians')
class Scout(Guardian):
    hp_base = 700
    # _u_hp = {5: 1289, 6: 1495}
    attack_base = 87
    # _u_attack = {5: 152, 6: 175}
    atk_speed = 0.5
    range = 3
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 1
    bossfight_cost = 20
    rarity = Rarity.Common


@register_unit_type('Guardians')
class Guard(Guardian):
    hp_base = 800
    # _u_hp = {6: 1610}
    attack_base = 67
    # _u_attack = {6: 135}
    atk_speed = 0.5
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 4
    armor_piercing = 0
    cost = 1
    bossfight_cost = 18
    rarity = Rarity.Common


@register_unit_type('Guardians')
class Healer(AOE, Heal, Guardian):
    hp_base = 800
    # _u_hp = {5: 1400, 6: 1610}
    heal_base = 60
    #_u_heal = {5: 105, 6: 121}
    heal_speed = 1/8
    heal_range = 5.5
    heal_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    cost = 2
    # TODO: heal spell
    bossfight_cost = 25
    rarity = Rarity.Rare

    #def dps(cls, targets: Union['MovableUnit', List['MovableUnit']], attacker_level: int = 1) -> None:
    #    return None


@register_unit_type('Guardians')
class Follet(Guardian):
    hp_base = 760
    # _u_hp = {6:1528}
    attack_base = 135
    # _u_attack = {6:271}
    atk_speed = 0.4
    range = 2
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.AIR
    armor = 0
    armor_piercing = 0
    cost = 2
    bossfight_cost = 25
    rarity = Rarity.Common


@register_unit_type('Guardians')
class Shield(Guardian):
    hp_base =  1425
    # _u_hp = {5: 2493, 6: 2867}
    attack_base = 205
    # _u_attack = {5: 359, 6: 413}
    atk_speed = 0.4
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 2
    bossfight_cost = 35
    rarity = Rarity.Rare


@register_unit_type('Guardians')
class Jetpack(Guardian):
    hp_base = 990
    # _u_hp = {5: 1732}
    attack_base = 175
    # _u_attack = {5: 306}
    atk_speed = 0.5
    range = 4
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.AIR
    armor = 0
    armor_piercing = 0
    cost = 2
    # TODO: EMP spell
    bossfight_cost = 33
    rarity = Rarity.Rare


@register_unit_type('Guardians')
class Knight(Guardian):
    hp_base = 1254
    # _u_hp = {5: 2193, 6: 2522}
    attack_base = 135
    # _u_attack = {5: 236, 6: 271}
    atk_speed = 0.6
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 4
    armor_piercing = 0
    cost = 2
    # TODO double armor spell
    bossfight_cost = 35
    rarity = Rarity.Rare


@register_unit_type('Guardians')
class Sword(AOE, Guardian):
    hp_base = 1024
    # _u_hp = {5: 1792, 6: 2061}
    attack_base = 143
    # _u_attack = {5: 250, 6: 288}
    atk_speed = 0.5
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 2
    bossfight_cost = 40
    rarity = Rarity.Rare
    gold_cost = 10000


@register_unit_type('Guardians')
class Sparte(Guardian):
    hp_base = 2895
    # _u_hp = {5: 5062}
    attack_base = 260
    # _u_attack = {5: 455}
    atk_speed = 0.7
    range = 2
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 4
    # TODO armor gain spell
    bossfight_cost = 80
    rarity = Rarity.Epic


@register_unit_type('Guardians')
@reincarnation
class SparteLeg(Sparte):
    # _u_hp = {1: 3185}
    # _u_attack = {1:  286}
    armor_boost = 2
    armor_boost_duration = 6
    max_armor_boost = 16


@register_unit_type('Guardians')
class Paladin(Guardian):
    hp_base = 2561
    # _u_hp = {1: 2561}
    attack_base = 253
    # _u_attack = {1: 253}
    atk_speed = 0.8
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 5
    armor_piercing = 0
    cost = 4
    # TODO: charge spell
    bossfight_cost = None
    rarity = Rarity.Epic
    gem_cost = 390


@register_unit_type('Guardians')
class Marchal(Guardian):
    hp_base = 2500
    # _u_hp = {6: 5028}
    attack_base = 299
    # _u_attack = {6: 601}
    atk_speed = 0.5
    range = 6
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 4
    multiple_target_limit = 2
    bossfight_cost = 90
    rarity = Rarity.Epic


@register_unit_type('Guardians')
@reincarnation
class MarchalLeg(Marchal):
    # _u_hp = {1: 2750}
    # _u_attack = {1: 329}
    multiple_target_limit = 3


@register_unit_type('Guardians')
class Griffon(Guardian):
    hp_base = 1794
    # _u_hp = {1: 1794}
    attack_base = 347
    # _u_attack = {1: 347}
    atk_speed = 0.4
    range = 4
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.AIR
    armor = 3
    armor_piercing = 0
    cost = 4
    esquive_rate = 0.2
    move_speed = 1.8
    bossfight_cost = None
    rarity = Rarity.Rare


@register_unit_type('Guardians')
class Hammer(Guardian):
    hp_base = 2145
    # _u_hp = {1: 2145}
    attack_base = 364
    # _u_attack = {1: 364}
    atk_speed = 0.5
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 5
    armor_piercing = 0
    cost = 4
    # TODO: shield spell
    bossfight_cost = None
    rarity = Rarity.Epic


@register_unit_type('Guardians')
class Canonner(Guardian, AOE):
    hp_base = 4000
    # _u_hp = {1: 4000}
    attack_base = 204
    # _u_attack = {1: 204}
    atk_speed = 0.5
    range = 8
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 4
    bossfight_cost = 190
    rarity = Rarity.Legendary


@register_unit_type('Guardians')
class DemonSlayer(Guardian):
    hp_base = 3750
    # _u_hp = {1: 3750, 2: 4313, 3: 4960, 4: 5704}
    attack_base = 230
    # _u_attack = {1: 230, 2: 265, 3: 305, 4: 351}
    atk_speed = 1
    range = 6
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 4
    armor_piercing = 6
    cost = 4
    can_miss = False
    # TODO: ignore 50% armmor (50% of what : armor value or damage reduction % ?)
    bossfight_cost = 200
    rarity = Rarity.Legendary


@register_unit_type('Guardians')
class Golem(AOE, Guardian):
    hp_base = 4849
    # _u_hp = {5: 8480}
    attack_base = 367
    # _u_attack = {5: 642}
    atk_speed = 0.4
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 6
    cost = 6
    # TODO: stone wall on death
    bossfight_cost = 190
    rarity = Rarity.Legendary
    gem_cost = 2400


@register_unit_type('Guardians')
class Seraphin(Guardian, Heal):
    hp_base = 3718
    # _u_hp = {6: 7478}
    attack_base = 478
    # _u_attack = {6: 961}
    atk_speed = 1
    range = 2
    shoot_to = TargetType.AIR_GROUND
    _u_heal = {6: 60}
    heal_speed = 1
    heal_range = 4
    heal_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 4
    armor_piercing = 0
    cost = 6
    # TODO: heal spell
    bossfight_cost = 200
    rarity = Rarity.Legendary
