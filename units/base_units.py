#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This is a personal project to understand and improve my knowledge/tactics in the game Caravan War.
# Copyright (C) 2019  Kasonnara <kasonnara@laposte.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from statistics import mean
from typing import Union, List, Optional, Type

import collections.abc

from common.armor import armor_reduction
from common.cards import Card
from common.rarity import Rarity
from common.target_types import TargetType
from units.equipments import Weapon, Armor
from utils.class_property import classproperty

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
    """Damage value (at level 1)"""
    hit_frequency: int = None
    """Hit frequency"""
    range: int = None
    """Attack reach range"""
    shoot_to: TargetType = None
    """Types of movable unit this unit can shoot to"""
    armor_piercing: int = None
    """Armor piercing value"""
    cost: int = None  # TODO: Refactor this attribute which is ambiguous (slot_cost? use_cost? army_cost?)
    """Cost value (exact meaning may vary from a unit type to another, but it's used to compute fair scores 
    between small and big units)"""
    multiple_target_limit = 1
    """Maximum number of simultaneous target"""
    can_miss = True
    """If false the unit is not affected by evasion abilities (deamon slayer, fire tower, etc)"""

    level_grow_factor = 1.15
    """Damage and heath exponential increase factor earned with each unit level"""
    star_factor = .05
    """Damage and heath linear increase earned with each unit star"""

    consecutive_hit_attack_boost = 0.
    """Damage boost with consecutive attack combo on the same target 
    (0.0 means no increase; 0.1 means +10% damage increase of base damage each time)"""
    max_consecutive_boost = 1.
    """Maximum damage boost obtainable with combo on the same target 
    (1.0 means normal damage; 2.0 mean double damages)"""

    def __init__(self, level: int, stars=0, weapon: Weapon=None):
        super().__init__(level)
        self.stars = stars
        self.weapon = weapon

    @property
    def attack(self) -> int:
        """
        :return: int, the raw attack value (taking into account: level, stars and weapons)
        """
        if self.attack_base is None:
            return None
        return round(
            self.attack_base                            # base stat
            * self.level_grow_factor ** (self.level-1)  # exponential grows with level
            * (1 + self.star_factor * self.stars)       # linear grows with stars
            + (0 if self.weapon is None else self.weapon.bonus_factor * self.attack_base) # equipment bonus
            )

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

    def damage_formule(self, target: 'MovableUnit', target_index=0, hit_combo=0):
        if target_index >= self.multiple_target_limit:
            return None
        atk = self.attack
        if atk is None:
            return None
        return (
            atk
            * armor_reduction(target.armor - self.armor_piercing)
            * (min(1 + self.consecutive_hit_attack_boost * hit_combo, self.max_consecutive_boost))
            )

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
                internal_values.append("lvl=" + str(self.level))
            if self.stars > 0:
                internal_values.append("stars=" + str(self.stars))
            if self.weapon is not None:
                internal_values.append("weapon=" + str(self.weapon.level))
            self._repr = self.__class__.__name__.lower() + ('['+','.join(internal_values)+']' if len(internal_values) > 0 else "")
        return self._repr


class MovableUnit(BaseUnit):
    hp_base = None
    """Heath value (at level 1)"""
    shooted_as: TargetType = None
    """Basically is this unit flying or not"""
    armor: int = None
    """Armor value"""
    move_speed: float = None
    """Moving speed"""
    esquive_rate = 1
    """The accuracy factor of an attacker shooting at this unit.  
    (1 means attacker will never miss, 0.5 means they will miss one attack every two shots)
    (assert 0 < esquive_rate <= 1)"""
    is_summoned = False
    """Is this unit subject to invoked units penalties"""
    is_immune_to_effect = False
    """Is this unit immune to all indirect effects or penalties"""

    def __init__(self, level: int, stars=0, weapon_item: Weapon = None, armor_item: Armor = None):
        super().__init__(level, stars, weapon_item)
        self.armor_item = armor_item

    @property
    def hp(self):
        # TODO: is it possible to factorize the formula (also used in attack and heal property), using for exemple a
        #       decorator, without using a 'self.get_attr(<stat_base>)' to get the base and the item that depend on
        #       the runtime unit and the stat considerated?
        return round(
            self.hp_base
            * self.level_grow_factor ** (self.level-1)
            * (1 + self.star_factor * self.stars)
            + (0 if self.armor_item is None else self.armor_item.bonus_factor * self.hp_base)
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

    def chase_distance(self, target: 'MovableUnit') -> Optional[float]:
        """
        Return the distance walked by the target, between two hits while chased by self
        :param target: MovableUnit
        :return: float or None if the target is faster than self
        """
        # Distance = TargetSpeed * (ChaseTime + AttackTime) = AttackerSpeed * (ChaseTime)
        #  ==> ChaseTime = (TargetSpeed * AttackTime) / (AttackerSpeed - TargetSpeed)
        #  ==> Distance = AttackerSpeed * (TargetSpeed * AttackTime) / (AttackerSpeed - TargetSpeed)
        if self.move_speed <= target.move_speed:
            return None
        distance = self.move_speed * (target.move_speed * 1 / self.hit_frequency) / (
                    self.move_speed - target.move_speed)
        return distance

    def dpm(self, target: 'MovableUnit') -> Optional[float]:
        """
        return the damage per meter of the unit when chaising the target unit
        (its mainly usefull for simulating vehicule et clan boss damage)
        :param target: the chased unit
        :return: float = (damage dealt to the target)  / (distance walked by the target including chasing time)
        """
        distance = self.chase_distance(target)
        if distance is None:
            return None
        return (
            self.damage_formule(target)
            * (target.esquive_rate if self.can_miss else 1)
            / distance
            )

    def chase_damage(self, target: 'MovableUnit', path_length):
        """
        return the total damages dealt when chaising the target unit on the given distance
        (its similar to dpm, but take into account effect that depend on the number of hit (e.g vikings, sparte, etc))
        (its mainly usefull for simulating vehicule et clan boss damage)
        :param target: the chased unit
        :param path_length: chase length
        :return: float, damage dealt to the target over the entire path
        """
        distance = self.chase_distance(target)
        if distance is None:
            return None

        return sum(
            self.damage_formule(target, hit_combo=hit_index)
            for hit_index in range(int(path_length // distance))
            )


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
            self._repr = self.shooted_as.name.lower() + "-unit" + (
                '[' + ','.join(internal_values) + ']' if len(internal_values) > 0 else "")
        return self._repr


class Heal:
    base_heal = None
    heal_frequency = None

    @property
    def heal(self) -> float:
        return round(
            self.base_heal
            * self.level_grow_factor ** (self.level-1)
            * (1 + self.star_factor * self.stars)
            + (0 if self.weapon is None else self.weapon.bonus_factor * self.base_heal)
            )

    def hps(self, allies: Union[MovableUnit, List[MovableUnit]]) -> float:
        return self.heal * self.heal_frequency * (len(allies) if hasattr(allies, '__len__') else 1)

    def hps_score(self, allies: Union[MovableUnit, List[MovableUnit]]):
        if self.cost is None:
            return None
        return self.hps(allies) / self.cost

    def score(self, allies: Union[MovableUnit, List[MovableUnit]]):
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


def reincarnation(cls: Type[BaseUnit]):
    assert cls.rarity is Rarity.Epic, "Only Epic card can be reincarned"
    # Define new unit stats increased by 10%
    cls.attack_base = (cls.__base__.attack_base * 1.1 if cls.__base__.attack_base is not None else None)
    # In practice no reborn unit have attack_base set to None
    if issubclass(cls, MovableUnit):
        cls.hp_base = cls.__base__.hp_base * 1.1
        # In practice all reborn units are MovableUnit subclasses
    if issubclass(cls, Summon):
        cls.summon_hp_base = cls.__base__.summon_hp_base * 1.1
        cls.summon_attack_base = cls.__base__.summon_attack_base * 1.1

    # Set new unit rarity
    cls.rarity = Rarity.Legendary
    return cls
