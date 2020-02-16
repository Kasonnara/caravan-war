#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    <Software description> 
    Copyright (C) 2019  Kasonnara <kasonnara@laposte.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from abc import abstractmethod
from collections import defaultdict
from statistics import mean
from typing import Iterable, Union, List, Optional, Type

import collections.abc

from armor import armor_reduction
from cards import Card, Rarity
from target_types import TargetType
from units.equipments import Weapon, Armor

MAX_LEVEL = 7
DPS_SCORE_FACTOR = 135 * 0.5  # Based on Guard units attack value
HP_SCORE_FACTOR = 1610 / 0.815  # Based on Guard units hp value


class AOE:
    multiple_target_limit = 100


class COE(AOE):
    """Cone of effect"""
    pass


class BaseUnitType(Card):
    attack_base = None
    atk_speed: int = None
    range: int = None
    shoot_to: TargetType = None
    armor_piercing: int = None
    cost: int = None
    multiple_target_limit = 1
    can_miss = True

    level_grow_factor = 1.15
    star_grow_factor = 1.05

    def __init__(self, level: int, stars=0, weapon: Weapon=None):
        super().__init__(level, stars)
        self.weapon = weapon

    @classmethod
    def u_attack(cls, level, stars=0, weapon: Weapon=None) -> int:
        if cls.attack_base is None:
            return None
        return round(cls.attack_base * cls.level_grow_factor ** (level-1) * cls.star_grow_factor ** stars) \
               + (0 if weapon is None else weapon.bonus_factor * cls.attack_base)

    @property
    def attack(self):
        return type(self).u_attack(self.level, stars=self.stars, weapon=self.weapon)

    @classmethod
    def get_reachable_targets(cls, targets: Union['MovableUnit', List['MovableUnit']]) -> List['MovableUnit']:
        """
        Return the given targets removing those which are unreachable
        :param targets: a single target or an iterable of targets
        :return: List[TargetType]
        """
        # Ensure we have a list
        if not isinstance(targets, collections.abc.Iterable):
            targets = (targets,)
        # Ensure unit is sufficiently defined
        if cls.shoot_to is None:
            return []
        # Remove unreachable targets
        return [target for target in targets if cls.shoot_to.can_fire_on(target.shooted_as)]

    @classmethod
    def damage_formule(cls, target: Union['MovableUnit', Type['MovableUnit']], attacker_level=1, stars=0,
                       weapon: Weapon = None, target_index=0):
        if target_index >= cls.multiple_target_limit:
            return 0
        return cls.u_attack(attacker_level, stars=stars, weapon=weapon) * armor_reduction(
            target.armor - cls.armor_piercing)

    @classmethod
    def dps(cls, targets: Union['MovableUnit', List['MovableUnit']], attacker_level=1, stars=0, weapon: Weapon=None) -> Optional[float]:
        # WARNING: if modified report changes to the classes :Lightning
        targets: List['MovableUnit'] = cls.get_reachable_targets(targets)

        damages = [cls.damage_formule(target, target_index=k, attacker_level=attacker_level, stars=stars, weapon=weapon) * (target.esquive_rate if cls.can_miss else 1)
                   for k, target in enumerate(targets)]
        damages = [damage for damage in damages if damage is not None]
        if len(damages) == 0 or cls.atk_speed is None:
            return None
        return sum(damages) * cls.atk_speed

    @classmethod
    def dps_ratio(cls, targets: Union['MovableUnit', List['MovableUnit']], attacker_level=1, stars=0, weapon: Weapon=None) -> Optional[float]:
        dps = cls.dps(targets, attacker_level, stars=stars, weapon=weapon)
        if dps is None or cls.cost is None:
            return None
        return dps / cls.cost

    @classmethod
    def score(cls, enemies: Union['MovableUnit', List['MovableUnit']], unit_level=1, stars=0, weapon: Weapon=None):
        return (cls.dps_ratio(enemies, attacker_level=unit_level, stars=stars, weapon=weapon) or 0) / DPS_SCORE_FACTOR


class MovableUnit(BaseUnitType):
    hp_base = None
    shooted_as: TargetType = None
    armor: int = None
    move_speed: float = None
    esquive_rate = 1
    is_summoned = False
    is_immune_to_effect = False

    def __init__(self, level: int, stars=0, weapon_item: Weapon = None, armor_item: Armor = None):
        super().__init__(level, stars, weapon_item)
        self.armor_item = armor_item

    @classmethod
    def u_hp(cls, level, stars=0, armor_item: Armor = None):
        return cls.hp_base * cls.level_grow_factor ** (level-1) * cls.star_grow_factor ** stars \
               + (0 if armor_item is None else Armor.bonus_factor * cls.hp_base)

    @property
    def hp(self):
        return type(self).u_hp(self.level, stars=self.stars, armor_item=self.armor_item)

    @classmethod
    def hp_ratio(cls, attackers: List[BaseUnitType], defenser_level=1, stars=0, armor_item: Armor = None) -> float:
        # TODO take into account that multiple small units are more sensible to AOE? or that faster units take less attacks
        # TODO: sum or mean or ... ? Do we want the hp part of the score to change when fighting multiple units?
        armor_esquive_factor = mean([armor_reduction(cls.armor - attacker.armor_piercing) / (cls.esquive_rate if attacker.can_miss else 1)
                                     for attacker in attackers])
        return cls.u_hp(defenser_level, stars=stars, armor_item=armor_item) * armor_esquive_factor / cls.cost

    @classmethod
    def score(cls, enemies: Union['MovableUnit', List['MovableUnit']], unit_level=1, stars=0, weapon_item: Weapon = None, armor_item: Armor = None):
        return (super().score(enemies, unit_level=unit_level, stars=stars)
                + cls.hp_ratio(enemies, defenser_level=unit_level, stars=stars) / HP_SCORE_FACTOR)

    @classmethod
    def to_string(cls):
        return cls.__name__.lower()

    @classmethod
    def dpm(cls, target: 'MovableUnit', attacker_level=1, stars=0, weapon: Weapon = None) -> Optional[float]:
        """
        return the damage per meter of the unit when chaising the target unit
        (its mainly usefull for simulating vehicule et clan boss damage)
        :param target: the chased unit
        :param attacker_level: level of the unit
        :param stars: stars of the unit
        :param weapon: weapon of the unit
        :return: float = (damage dealt to the target)  / (distance walked by the target including chasing time)
        """
        # Distance = TargetSpeed * (ChaseTime + AttackTime) = AttackerSpeed * (ChaseTime)
        #  ==> ChaseTime = (TargetSpeed * AttackTime) / (AttackerSpeed - TargetSpeed)
        #  ==> Distance = AttackerSpeed * (TargetSpeed * AttackTime) / (AttackerSpeed - TargetSpeed)
        if cls.move_speed <= target.move_speed:
            return None
        distance = cls.move_speed * (target.move_speed * 1/cls.atk_speed) / (cls.move_speed - target.move_speed)
        return (
            cls.damage_formule(target, attacker_level=attacker_level, stars=stars, weapon=weapon)
            * (target.esquive_rate if cls.can_miss else 1)
            / distance
            )

    @classmethod
    def chase_damage(cls, target: 'MovableUnit', path_length, **kwargs):
        """
        return the total damages dealt when chaising the target unit on the given distance
        (its similar to dpm, but take into account effect that depend on the number of hit (e.g vikings, sparte, etc))
        (its mainly usefull for simulating vehicule et clan boss damage)
        :param target: the chased unit
        :param path_length: chase length
        :param attacker_level: level of the unit
        :param stars: stars of the unit
        :param weapon: weapon of the unit
        :return: float, damage dealt to the target over the entire path
        """
        return path_length * cls.dpm(target, **kwargs)


class FakeMovableUnit(MovableUnit):
    def __init__(self, shooted_as=TargetType.AIR_GROUND, armor=0, armor_piercing=0, can_miss=True):
        self.shooted_as = shooted_as
        self.armor = armor
        self.armor_piercing = armor_piercing
        self.can_miss = can_miss

    def to_string(self):
        return self.shooted_as.name.lower + " unit"


class Heal:
    base_heal = None
    @classmethod
    def u_heal(cls, level, stars=0, weapon_item: Weapon = None):
        return cls.base_heal * cls.level_grow_factor ** (level-1) * cls.star_grow_factor**stars \
               + (0 if weapon_item is None else weapon_item.bonus_factor * cls.base_heal)

    @classmethod
    def hps(cls, allies, healer_level=1, stars=0, weapon_item: Weapon = None):
        raw_heal = cls.u_heal(healer_level, stars=stars, weapon_item=weapon_item)
        if raw_heal is None:
            return None
        return raw_heal * cls.heal_speed * len(allies)

    @classmethod
    def hps_ratio(cls, allies, healer_level=1, stars=0, weapon_item: Weapon = None):
        hps = cls.hps(allies, healer_level, stars=stars, weapon_item=weapon_item)
        if hps is None or cls.cost is None:
            return None
        return hps / cls.cost

    @classmethod
    def score(cls, enemies: Union['MovableUnit', List['MovableUnit']], unit_level=1, stars=0, weapon_item: Weapon = None, armor_item: Armor = None):
        # FIXME: heal doesn't apply to enely but to allies!
        return (cls.hps_ratio(enemies, unit_level, stars=stars, weapon_item=weapon_item) / DPS_SCORE_FACTOR
                + (cls.hp_ratio(enemies, unit_level, stars=stars, armor_item=armor_item) / HP_SCORE_FACTOR if issubclass(cls, MovableUnit) else 0))


class Summon:
    summon_number = None
    summon_hp_base = None
    summon_attack_base = None
    summon_atk_speed = None


UNIT_DICTIONNARY = defaultdict(list)


def register_unit_type(category: str):
    def register_unit_type_aux(cls):
        cls.category = category
        UNIT_DICTIONNARY[category].append(cls)
        return cls
    return register_unit_type_aux


def reincarnation(cls: Type[BaseUnitType]):
    assert cls.rarity is Rarity.Epic, "Only Epic card can be reincarned"
    cls.attack_base = cls.__base__.attack_base * 1.1

    if issubclass(cls, MovableUnit):
        cls.hp_base = cls.__base__.hp_base * 1.1

    if issubclass(cls, Summon):
        cls.summon_hp_base = cls.__base__.summon_hp_base * 1.1
        cls.summon_attack_base = cls.__base__.summon_attack_base * 1.1

    cls.rarity = Rarity.Legendary
    return cls
