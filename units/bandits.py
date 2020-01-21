from cards import Rarity
from units.base_units import MovableUnit, AOE, register_unit_type, reincarnation
from target_types import TargetType


class Bandit(MovableUnit):
    pass


@register_unit_type('Bandits')
class Maraudeur(Bandit):
    hp_base = 451
    # _u_hp = {5: 816, 6: 938}
    attack_base = 120
    # _u_attack = {5: 210, 6: 241}
    atk_speed = 0.4
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 2
    armor_piercing = 0
    cost = 3
    move_speed = 1.7
    rarity = Rarity.Common


@register_unit_type('Bandits')
class Archer(Bandit):
    hp_base = 300
    # _u_hp = {5: 525, 6: 604}
    attack_base = 71
    # _u_attack = {5: 124, 6: 143}
    atk_speed = 1
    range = 8
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 3
    move_speed = 1.7
    rarity = Rarity.Common


@register_unit_type('Bandits')
class Drone(Bandit):
    hp_base = 500
    # _u_hp = {5: 874, 6: 1005}
    attack_base = 95
    # _u_attack = {5: 163, 6: 187}
    atk_speed = 0.75
    range = 3
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.AIR
    armor = 0
    armor_piercing = 0
    cost = 3
    move_speed = 2
    rarity = Rarity.Common


@register_unit_type('Bandits')
class Brute(Bandit):
    hp_base = 1125
    # _u_hp = {5: 1968, 6: 2263}
    attack_base = 130
    # _u_attack = {5: 228, 6: 262}
    atk_speed = 0.5
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 4
    move_speed = 1.6
    rarity = Rarity.Rare


@register_unit_type('Bandits')
class Lutin(Bandit):
    hp_base = 650
    # _u_hp = {5: 1136, 6: 1307}
    attack_base = 110
    # _u_attack = {5: 193, 6: 222}
    atk_speed = 0.8
    range = 4
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.AIR
    armor = 0
    armor_piercing = 0
    cost = 6
    move_speed = 1.9
    rarity = Rarity.Rare


@register_unit_type('Bandits')
class Berserk(Bandit):
    hp_base = 960
    # _u_hp = {5: 1679, 6: 1931}
    attack_base = 150
    # _u_attack = {5: 262, 6: 301}
    atk_speed = 0.6
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 4
    armor_piercing = 0
    cost = 4
    move_speed = 1.8


@register_unit_type('Bandits')
class Hunter(Bandit):
    hp_base = 500
    # _u_hp = {5: 874, 6: 1005}
    attack_base = 122
    # _u_attack = {5: 213, 6: 245}
    atk_speed = 0.6
    range = 9
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 3
    cost = 4
    move_speed = 1.5
    rarity = Rarity.Rare


@register_unit_type('Bandits')
class Spider(AOE, Bandit):
    hp_base = 1140
    # _u_hp = {1: 1140, 2: 1311, 3: 1508, 4: 1734, 5: 1994, 6: 2293}
    attack_base = 110
    # _u_attack = {1: 110, 2: 127, 3: 146, 4: 168, 5: 193, 6: 222}
    atk_speed = 0.35
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 4
    move_speed = 1.4
    rarity = Rarity.Rare


@register_unit_type('Bandits')
class Alchimist(AOE, Bandit):
    hp_base = 482
    # _u_hp = {5: 843, 6: 969}
    attack_base = 140
    # _u_attack = {5: 245, 6: 282}
    atk_speed = 0.4
    range = 4
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 5
    move_speed = 1.6
    rarity = Rarity.Rare


@register_unit_type('Bandits')
class Viking(Bandit):
    hp_base = 1900
    # _u_hp = {5: 3323, 6: 3821}
    attack_base = 200
    # _u_attack = {5: 351, 6: 403}
    atk_speed = 1
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 6
    armor_piercing = 2
    cost = 8
    move_speed = 1.9
    rarity = Rarity.Epic


@register_unit_type('Bandits')
@reincarnation
class VikingLeg(Viking):
    # _u_hp = {1: 2090, 2: 2404, 3: 2765, 4: 3180, 5: 3657}
    # _u_attack = {1: 220, 2: 253, 3: 291, 4: 335, 5: 385}
    atk_speed = 1.25


@register_unit_type('Bandits')
class Momie(Bandit):
    hp_base = 1400
    # _u_hp = {1: 1470}
    attack_base = 240
    # _u_attack = {1: 240}
    atk_speed = 0.6
    range = 7
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 7
    move_speed = 1.4
    rarity = Rarity.Epic


@register_unit_type('Bandits')
class DarkKnight(Bandit):
    hp_base = 1677
    # _u_hp = {5: 2934, 6: 3374}
    attack_base = 394
    # _u_attack = {5: 689, 6: 792}
    atk_speed = 0.8
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 6
    armor_piercing = 0
    cost = 8
    move_speed = 1.9
    rarity = Rarity.Epic


@register_unit_type('Bandits')
@reincarnation
class DarkKnightLeg(DarkKnight):
    # _u_hp = {1: 1845}
    # _u_attack = {1: 433}
    stun_duration = 2.5


@register_unit_type('Bandits')
class Condor(Bandit):
    hp_base
    # _u_hp = {8: 3906}
    attack_base
    # _u_attack = {8: 691}
    atk_speed = 0.7
    range = 8
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.AIR
    armor = 0
    armor_piercing = 0
    cost = 8
    move_speed = 1.7
    rarity = Rarity.Epic


@register_unit_type('Bandits')
class Stealer(Bandit):
    hp_base = 1430
    # _u_hp = {5: 2502, 6: 2877}
    attack_base = 328
    # _u_attack = {5: 574, 6: 660}
    atk_speed = 0.9
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 3
    armor_piercing = 2
    cost = 7
    move_speed = 2
    rarity = Rarity.Epic


@register_unit_type('Bandits')
@reincarnation
class StealerLeg(Stealer):
    # _u_hp = {1: 1573}
    # _u_attack = {1: 361}
    atk_speed = 1.2
    shoot_to = TargetType.AIR_GROUND
    vehicule_damage_factor = 2.5


@register_unit_type('Bandits')
class Lich(Bandit):
    hp_base = 1072
    # _u_hp = {1: 1072, 2: 1233, 3: 1418, 4: 1631, 5: 1876, 6: 2157}
    attack_base = 390
    # _u_attack = {1: 390, 2: 448, 3: 515, 4: 592, 5: 681, 6: 783}
    atk_speed = 0.4
    range = 5
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 6
    cost = 8
    move_speed = 1
    summon_number = 3
    #summon_hp = {1: 455, 2: 523, 3: 601, 4: 691, 5: 795}
    summon_hp_base = 455
    #summon_atk = {1: 38, 2: 44, 3: 51, 4: 59, 5: 68}
    summon_attack_base = 38
    summon_atk_speed = 1/10
    rarity = Rarity.Epic


@register_unit_type('Bandits')
@reincarnation
class LichLeg(Lich):
    # _u_hp = {1: 1179}
    # _u_attack = {1: 429}
    summon_number = 5
    summon_hp = {1: 501}
    summon_atk = {1: 42}
    summon_atk_speed = 1 / 7


@register_unit_type('Bandits')
class Inferno(Bandit):
    hp_base = 4407
    # _u_hp = {5: 7707, 6: 8863}
    attack_base = 630
    # _u_attack = {5: 1103, 6: 1268}
    atk_speed = 0.7
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 12
    move_speed = 1.7
    rarity = Rarity.Legendary


@register_unit_type('Bandits')
class Demon(Bandit):
    hp_base = 3900
    # _u_hp = {5: 6822, 6: 7845}
    attack_base = 500
    # _u_attack = {5: 874, 6: 1005}
    atk_speed = 1
    range = 2
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 8
    armor_piercing = 4
    cost = 10
    move_speed = 1.9
    rarity = Rarity.Legendary


@register_unit_type('Bandits')
class Chaman(Bandit):
    hp_base = 1605
    # _u_hp = {1: 1605}
    attack_base = 504
    # _u_attack = {1: 504}
    atk_speed = 0.5
    range = 8
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 3
    cost = 12
    move_speed = 1.4
    rarity = Rarity.Legendary
    # TODO heal effect


@register_unit_type('Bandits')
class Djin(Bandit, AOE):
    hp_base = 1456
    # _u_hp = {8: 3872}
    attack_base = 370
    # _u_attack = {8: 983}
    atk_speed = 0.5
    range = 6
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 11
    move_speed = 1.3
    summon_number = 1
    summon_hp = {8: 2627}
    summon_atk = {8: 450}
    summon_atk_speed = 1/10
    # TODO Slow down effect
    rarity = Rarity.Legendary


@register_unit_type('Bandits')
class Mecha(Bandit):
    hp_base = 1885
    # _u_hp = {8: 5015}
    attack_base = 331
    # _u_attack = {8: 882}
    atk_speed = 0.6
    range = 7
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 6
    armor_piercing = 0
    cost = 11
    move_speed = 1.5
    multiple_target_limit = 3
    missil_attack_base = 374
    missile_atk_speed = 0.5
    # TODO missile
    rarity = Rarity.Legendary
