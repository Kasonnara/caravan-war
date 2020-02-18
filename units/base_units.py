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


class BaseUnit(Card):
    attack_base = None
    hit_frequency: int = None
    range: int = None
    shoot_to: TargetType = None
    armor_piercing: int = None
    cost: int = None
    multiple_target_limit = 1
    """Maximum number of simultaneous target"""
    can_miss = True
    """If false the unit is not affected by evasion abilities (deamon slayer, fire tower, etc)"""

    level_grow_factor = 1.15
    star_grow_factor = 1.05

    def __init__(self, level: int, stars=0, weapon: Weapon=None):
        super().__init__(level, stars)
        self.weapon = weapon

    @property
    def attack(self) -> int:
        """
        :return: int, the raw attack value (taking into account: level, stars and weapons)
        """
        if self.attack_base is None:
            return None
        return round(self.attack_base * self.level_grow_factor ** (self.level-1) * self.star_grow_factor ** self.stars) \
               + (0 if self.weapon is None else self.weapon.bonus_factor * self.attack_base)

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

    def damage_formule(self, target: 'MovableUnit', target_index=0):
        if target_index >= self.multiple_target_limit:
            return None
        return self.attack * armor_reduction(target.armor - self.armor_piercing)

    def dps(self, targets: Union['MovableUnit', List['MovableUnit']]) -> Optional[float]:
        # WARNING: if modified report changes to the classes :Lightning
        targets: List['MovableUnit'] = self.get_reachable_targets(targets)

        damages = [(self.damage_formule(target, target_index=k), target)
                   for k, target in enumerate(targets)]
        damages = [damage * (target.esquive_rate if self.can_miss else 1)
                   for damage, target in damages
                   if damage is not None]
        if len(damages) == 0 or self.hit_frequency is None:
            return None
        return sum(damages) * self.hit_frequency

    def dps_score(self, targets: Union['MovableUnit', List['MovableUnit']]) -> Optional[float]:
        dps = self.dps(targets)
        if dps is None or self.cost is None:
            return None
        return dps / self.cost

    def score(self, enemies: Union['MovableUnit', List['MovableUnit']]):
        return (self.dps_score(enemies) or 0) / DPS_SCORE_FACTOR

    def __repr__(self):
        if self._repr is None:
            # Compute and cache representation value
            internal_values = []
            if self.level > 1:
                internal_values.append("lvl=" + self.level)
            if self.stars > 0:
                internal_values.append("stars=" + self.stars)
            if self.weapon is not None:
                internal_values.append("weapon=" + self.weapon.level)
            self._repr = self.__class__.__name__.lower() + ('['+','.join(internal_values)+']' if len(internal_values) > 0 else "")
        return self._repr


class MovableUnit(BaseUnit):
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

    @property
    def hp(self):
        return (
            self.hp_base * self.level_grow_factor ** (self.level-1)
            * self.star_grow_factor ** self.stars
            + (0 if self.armor_item is None else Armor.bonus_factor * self.hp_base)
            )

    def hp_score(self, attackers: List[BaseUnit]) -> float:
        # TODO take into account that multiple small units are more sensible to AOE? or that faster units take less attacks
        # TODO: sum or mean or ... ? Do we want the hp part of the score to change when fighting multiple units?
        armor_esquive_factor = mean([armor_reduction(self.armor - attacker.armor_piercing) / (self.esquive_rate if attacker.can_miss else 1)
                                     for attacker in attackers])
        return self.hp * armor_esquive_factor / self.cost

    def score(self, enemies: Union['MovableUnit', List['MovableUnit']]):
        return (
                super().score(enemies)  # dps score
                + self.hp_score(enemies) / HP_SCORE_FACTOR  # hp score
            )

    def __repr__(self):
        if self._repr is None:
            # Compute and cache representation value
            internal_values = []
            if self.level > 1:
                internal_values.append("lvl={}".format(self.level))
            if self.stars > 0:
                internal_values.append("stars={}".format(self.stars))
            if self.weapon is not None:
                internal_values.append("weapon={}".format(self.weapon.level))
            if self.weapon is not None:
                internal_values.append("armor={}".format(self.weapon.level))
            self._repr = self.__class__.__name__.lower() + ('['+','.join(internal_values)+']' if len(internal_values) > 0 else "")
        return self._repr

    def dpm(self, target: 'MovableUnit') -> Optional[float]:
        """
        return the damage per meter of the unit when chaising the target unit
        (its mainly usefull for simulating vehicule et clan boss damage)
        :param target: the chased unit
        :return: float = (damage dealt to the target)  / (distance walked by the target including chasing time)
        """
        # Distance = TargetSpeed * (ChaseTime + AttackTime) = AttackerSpeed * (ChaseTime)
        #  ==> ChaseTime = (TargetSpeed * AttackTime) / (AttackerSpeed - TargetSpeed)
        #  ==> Distance = AttackerSpeed * (TargetSpeed * AttackTime) / (AttackerSpeed - TargetSpeed)
        if self.move_speed <= target.move_speed:
            return None
        distance = self.move_speed * (target.move_speed * 1 / self.hit_frequency) / (self.move_speed - target.move_speed)
        return (
            self.damage_formule(target)
            * (target.esquive_rate if self.can_miss else 1)
            / distance
            )

    @classmethod
    def chase_damage(self, target: 'MovableUnit', path_length):
        """
        return the total damages dealt when chaising the target unit on the given distance
        (its similar to dpm, but take into account effect that depend on the number of hit (e.g vikings, sparte, etc))
        (its mainly usefull for simulating vehicule et clan boss damage)
        :param target: the chased unit
        :param path_length: chase length
        :return: float, damage dealt to the target over the entire path
        """
        return path_length * self.dpm(target)


class FakeMovableUnit(MovableUnit):
    def __init__(self, shooted_as=TargetType.AIR_GROUND, armor=0, armor_piercing=0, can_miss=True):
        super().__init__(1, 0, None, None)
        self.shooted_as = shooted_as
        self.armor = armor
        self.armor_piercing = armor_piercing
        self.can_miss = can_miss

    def __repr__(self):
        if self._repr is None:
            # Compute and cache representation value
            internal_values = []
            if self.level > 1:
                internal_values.append("lvl=" + self.level)
            if self.stars > 0:
                internal_values.append("stars=" + self.stars)
            if self.weapon is not None:
                internal_values.append("weapon=" + self.weapon.level)
            if self.weapon is not None:
                internal_values.append("armor=" + self.weapon.level)
            self._repr = self.shooted_as.__name__.lower() + "-unit" + (
                '[' + ','.join(internal_values) + ']' if len(internal_values) > 0 else "")
        return self._repr


class Heal:
    base_heal = None
    heal_frequency = None

    @property
    def heal(self) -> float:
        return (
            self.base_heal * self.level_grow_factor ** (self.level-1)
            * self.star_grow_factor**self.stars \
            + (0 if self.weapon is None else self.weapon.bonus_factor * self.base_heal)
            )

    def hps(self, allies: Union['MovableUnit', List['MovableUnit']]) -> float:
        return self.heal * self.heal_frequency * (len(allies) if hasattr(allies, '__len__') else 1)

    def hps_score(self, allies: Union['MovableUnit', List['MovableUnit']]):
        if self.cost is None:
            return None
        return self.hps(allies) / self.cost

    def score(self, allies: Union['MovableUnit', List['MovableUnit']]):
        # FIXME: heal doesn't apply to ennemy but to allies!
        return (
                self.hps_score(allies) / DPS_SCORE_FACTOR
                + (self.hp_score(allies) / HP_SCORE_FACTOR if isinstance(self, MovableUnit) else 0)
            )


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


def reincarnation(cls: Type[BaseUnit]):
    assert cls.rarity is Rarity.Epic, "Only Epic card can be reincarned"
    cls.attack_base = (cls.__base__.attack_base * 1.1 if cls.__base__.attack_base is not None else None)

    if issubclass(cls, MovableUnit):
        cls.hp_base = cls.__base__.hp_base * 1.1

    if issubclass(cls, Summon):
        cls.summon_hp_base = cls.__base__.summon_hp_base * 1.1
        cls.summon_attack_base = cls.__base__.summon_attack_base * 1.1

    cls.rarity = Rarity.Legendary
    return cls
