from cards import Rarity
from units.base_units import MovableUnit, AOE, register_unit_type, reincarnation
from target_types import TargetType


class Bandit(MovableUnit):
    pass


@register_unit_type('Bandits')
class Maraudeur(Bandit):
    hp_base = 451
    attack_base = 120
    hit_frequency = 0.4
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
    attack_base = 71
    hit_frequency = 1
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
    attack_base = 95
    hit_frequency = 0.75
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
    attack_base = 130
    hit_frequency = 0.5
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
    attack_base = 110
    hit_frequency = 0.8
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
    attack_base = 150
    hit_frequency = 0.6
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
    attack_base = 122
    hit_frequency = 0.6
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
    attack_base = 110
    hit_frequency = 0.35
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
    attack_base = 140
    hit_frequency = 0.4
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
    attack_base = 200
    hit_frequency = 1
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 6
    armor_piercing = 2
    cost = 8
    move_speed = 1.9
    consecutive_hit_attack_boost = 0.4
    max_consecutive_boost = 3.
    rarity = Rarity.Epic


@register_unit_type('Bandits')
@reincarnation
class VikingLeg(Viking):
    hit_frequency = 1.25
    # FIXME: viking combo doesn't behave like other combo


@register_unit_type('Bandits')
class Momie(Bandit):
    hp_base = 1400
    attack_base = 240
    hit_frequency = 0.6
    range = 7
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 7
    move_speed = 1.4
    rarity = Rarity.Epic


@register_unit_type('Bandits')
@reincarnation
class MomieLeg(Momie):
    pass


@register_unit_type('Bandits')
class DarkKnight(Bandit):
    hp_base = 1677
    attack_base = 394
    hit_frequency = 0.8
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
    stun_duration = 2.5


@register_unit_type('Bandits')
class Condor(Bandit):
    hp_base = 1469
    attack_base = 260
    hit_frequency = 0.7
    range = 8
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.AIR
    armor = 0
    armor_piercing = 0
    cost = 8
    move_speed = 1.7
    armor_reduction = 5
    spell_duration = 60
    rarity = Rarity.Epic


@register_unit_type('Bandits')
@reincarnation
class CondorLeg(Condor):
    armor_reduction = 100


@register_unit_type('Bandits')
class Stealer(Bandit):
    hp_base = 1430
    attack_base = 328
    hit_frequency = 0.9
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
    hit_frequency = 1.2
    shoot_to = TargetType.AIR_GROUND
    vehicule_damage_factor = 2.5


@register_unit_type('Bandits')
class Lich(Bandit):
    hp_base = 1072
    attack_base = 390
    hit_frequency = 0.4
    range = 5
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 6
    cost = 8
    move_speed = 1
    summon_number = 3
    summon_hp_base = 455
    summon_attack_base = 38
    summon_atk_speed = 1/10
    rarity = Rarity.Epic


@register_unit_type('Bandits')
@reincarnation
class LichLeg(Lich):
    summon_number = 5
    summon_atk_speed = 1 / 7


@register_unit_type('Bandits')
class Inferno(Bandit):
    hp_base = 4407
    attack_base = 630
    hit_frequency = 0.7
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
    attack_base = 500
    hit_frequency = 1
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
    attack_base = 504
    hit_frequency = 0.5
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
    attack_base = 370
    hit_frequency = 0.5
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
    attack_base = 331
    hit_frequency = 0.6
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
