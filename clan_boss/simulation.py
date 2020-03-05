#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    This is a personal project to understand and improve my knowledge/tactics in the game Caravan War.
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
from time import sleep
from typing import List, Tuple

from target_types import TargetType
from units import stocks
from units.bandits import Berserk, Demon, Chaman, Bandit
from units.base_units import MovableUnit
from units.guardians import Guardian
from units.stocks import CardStock
from units.vehicules import Vehicule

PATH_LENGHT = 85  # Not used yet
FIRST_BUSH_DISTANCE = 15  # Not used yet

ALLOW_SKIPPING_LARGER_UNITS = False
"""Enabling this may slow the process by checking new cases were a high dps unit isn't used. 
It's probably useless in most case if you have ALLOWED_WORST_ATTEMPT set wel"""
ALLOWED_WORST_ATTEMPT = 2
"""Accelerate the process by skipping removing larger units to introduce more smaller units after after N unsuccesfull attempts"""
UNIT_COUNT_LIMIT = 10
"""Accelerate the process by skipping army compositions of a lot a small units"""


class ClanBoss(Vehicule):
    move_speed = 1  # TODO verify
    shooted_as = TargetType.GROUND
    armor = 0
    is_immune_to_effect = True


def rec_choice(damage_table: List[Tuple[Bandit, int, float]], remaining_space=stocks.BANDIT_POWER, remaining_slots=8, allowed_worst_compo_attempts=ALLOWED_WORST_ATTEMPT):
    #print(dpss, remaining_space, remaining_slots)
    assert remaining_space >= 0, "Problem in space managment"
    assert remaining_slots >= 0, "Problem in slot managment"
    #sleep(1)
    if len(damage_table) == 0:
        #print("No more units to check")
        return [], 0
    if remaining_slots == 0:
        #print("No enough slots")
        return [], 0
    _allowed_worst_compo_attempts = allowed_worst_compo_attempts

    best_compo, best_damage = [], 0.
    for k in range(min(damage_table[0][1], remaining_space // damage_table[0][0].cost), -1, -1):
        if _allowed_worst_compo_attempts == 0 and (k > 0 or not ALLOW_SKIPPING_LARGER_UNITS):
            #print("{} worst compo: skip".format(allowed_worst_compo_attempts))
            continue

        if damage_table[0][0].cost * k > remaining_space:
            #print("Not enough power")
            continue

        sub_best_compo, sub_best_damage = rec_choice(
            damage_table[1:],
            remaining_space - damage_table[0][0].cost * k,
            remaining_slots - (1 if k > 0 else 0),
            allowed_worst_compo_attempts=allowed_worst_compo_attempts,
            )
        sub_best_compo, sub_best_damage = [damage_table[0][0]] * k + sub_best_compo, damage_table[0][2] * k + sub_best_damage

        if sub_best_damage > best_damage :
            best_compo, best_damage = sub_best_compo, sub_best_damage
        else:
            _allowed_worst_compo_attempts -= 1

    return best_compo, best_damage


def evaluate(bandit_stocks: List[CardStock] = stocks.bandits):
    boss_unit = ClanBoss(1)
    # Get damage par metter for all units
    chase_damage = [
        (stock.card,
         stock.quantity,
         stock.card.chase_damage(boss_unit,
                                 (PATH_LENGHT if isinstance(stock.card, (Demon, Chaman)) else (PATH_LENGHT-FIRST_BUSH_DISTANCE))))
        for stock in bandit_stocks
        ]
    # Remove the unit too slow (dmg == None)
    chase_damage = [
        (card, quantity, dmg)
        for card, quantity, dmg in chase_damage
        if dmg is not None
        ]
    # Sort
    chase_damage = sorted(chase_damage, key=lambda x: x[2]/x[0].cost, reverse=True)

    print("Damage predicted per unit type:",{card.__class__.__name__: dpm/card.cost for card, quantity, dpm in chase_damage})

    best_compo, best_damage = rec_choice(chase_damage)
    # TODO plots
    return best_compo, best_damage


if __name__ == '__main__':
    best_compo, best_damage = evaluate()
    print("Best composition found:", ", ".join(type(unit).__name__ for unit in best_compo))
    print("Total damages =", best_damage)
