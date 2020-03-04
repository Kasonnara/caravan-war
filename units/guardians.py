from typing import Union, List

from common.rarity import Rarity
from units.base_units import MovableUnit, Heal, AOE, register_unit_type, reincarnation, DPS_SCORE_FACTOR, \
    HP_SCORE_FACTOR
from common.target_types import TargetType


class Guardian(MovableUnit):
    move_speed = 1.2
    bossfight_cost = None


@register_unit_type('Guardians')
class Scout(Guardian):
    hp_base = 700
    attack_base = 87
    hit_frequency = 0.5
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
    attack_base = 67
    hit_frequency = 0.5
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
    base_heal = 60
    heal_frequency = 1/8
    heal_range = 5.5
    heal_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    cost = 2
    # TODO: heal spell
    bossfight_cost = 25
    rarity = Rarity.Rare


@register_unit_type('Guardians')
class Follet(Guardian):
    hp_base = 760
    attack_base = 135
    hit_frequency = 0.4
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
    hp_base = 1425
    attack_base = 205
    hit_frequency = 0.4
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
    attack_base = 175
    hit_frequency = 0.5
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
    attack_base = 135
    hit_frequency = 0.6
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
    attack_base = 143
    hit_frequency = 0.5
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
    attack_base = 260
    hit_frequency = 0.7
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
    armor_boost = 2
    armor_boost_duration = 6
    max_armor_boost = 16


@register_unit_type('Guardians')
class Paladin(Guardian):
    hp_base = 2561
    attack_base = 253
    hit_frequency = 0.8
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 5
    armor_piercing = 0
    cost = 4
    # TODO: charge spell
    bossfight_cost = None
    rarity = Rarity.Epic


@register_unit_type('Guardians')
@reincarnation
class PaladinLeg(Paladin):
    charge_resistance = 0.5


@register_unit_type('Guardians')
class Marchal(Guardian):
    hp_base = 2500
    attack_base = 299
    hit_frequency = 0.5
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
    multiple_target_limit = 3


@register_unit_type('Guardians')
class Griffon(Guardian):
    hp_base = 1794
    attack_base = 347
    hit_frequency = 0.4
    range = 4
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.AIR
    armor = 3
    armor_piercing = 0
    cost = 4
    esquive_rate = 0.2
    move_speed = 1.8
    bossfight_cost = None
    rarity = Rarity.Epic


@register_unit_type('Guardians')
@reincarnation
class GriffonLeg(Griffon):
    esquive_next_attack_boost = 3.0


@register_unit_type('Guardians')
class Hammer(Guardian):
    hp_base = 2145
    attack_base = 364
    hit_frequency = 0.5
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
@reincarnation
class HammerLeg(Hammer):
    spell_max_stacking = 3


@register_unit_type('Guardians')
class Canonner(Guardian, AOE):
    hp_base = 4000
    attack_base = 204
    hit_frequency = 0.5
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
    attack_base = 230
    hit_frequency = 1
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
    attack_base = 367
    hit_frequency = 0.4
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 6
    cost = 6
    # TODO: stone wall on death
    bossfight_cost = 190
    rarity = Rarity.Legendary


@register_unit_type('Guardians')
class Seraphin(Guardian, Heal):
    hp_base = 3718
    attack_base = 478
    hit_frequency = 1
    range = 2
    shoot_to = TargetType.AIR_GROUND
    base_heal = 30
    heal_frequency = 1
    heal_range = 4
    heal_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 4
    armor_piercing = 0
    cost = 6
    # TODO: heal spell
    bossfight_cost = 200
    rarity = Rarity.Legendary

    def score(self, allies_targets: Union['MovableUnit', List['MovableUnit']]):
        # FIXME: heal doesn't apply to ennemy but to allies!
        return (
                self.dps_score(allies_targets) / DPS_SCORE_FACTOR
                + self.hps_score(allies_targets) / DPS_SCORE_FACTOR
                + self.hp_score(allies_targets) / HP_SCORE_FACTOR
            )


@register_unit_type('Guardians')
class Wizard(Guardian):
    hp_base = 4400
    attack_base = 500
    hit_frequency = 0.7
    range = 2
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.AIR
    armor = 0
    armor_piercing = 0
    cost = 6
    # TODO: stun
    bossfight_cost = 190
    rarity = Rarity.Legendary
