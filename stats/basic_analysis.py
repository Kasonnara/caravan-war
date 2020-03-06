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
from enum import auto, Enum
from math import ceil
from typing import List

import matplotlib.pyplot as plt

from units.base_units import MAX_LEVEL, FakeMovableUnit, MovableUnit, BaseUnit
from common.cards import CARD_DICTIONNARY
import units.bandits as bandits
from config.my_cards import MY_CARDS, CardStock

COST_DISPLAY = {'Towers': "cost", 'Weapons': "1", 'Bandits': "cost", 'Guardians': "used cell", 'Vehicules': "used cell"}

# TODO: split output scores in different labelized pandas dataframe (to sum in general case and plot in different colors in bar plot)


class XAxis(Enum):
    LEVEL = "Level", "(constant: stars={stars), enemies in AOE=[{enemies}])"
    ENEMY_NUMBER = "Enemy count inside area of effect", "(constant: level={level}, stars={stars}, enemies in AOE=Nx[{enemies}])"
    STAR = "Card stars", "(constant: level={level}, enemies in AOE=[{enemies}])"
    NONE = "", "(constant: level={level},  stars={stars}, enemies in AOE=[{enemies}], stars={stars})"

    def iter(self, constant_level=1, constant_enemy_number=1, constant_star=1, variable_range=7):
        self.cache = {"level": constant_level, "enemy_count": constant_enemy_number,"star": constant_star}

        if self is self.NONE:
            return [(None, constant_level, constant_enemy_number, constant_star,)]
        else:
            return zip(
                range(1, variable_range + 1) if self is not self.STAR else range(variable_range),
                (constant_level,) * variable_range       if self is not self.LEVEL else range(1, variable_range + 1),
                (constant_enemy_number,) * variable_range if self is not self.ENEMY_NUMBER else range(1, variable_range + 1),
                (constant_star,) * variable_range        if self is not self.STAR else range(variable_range),
                )

    def get_legend(self):
        return self.value[0]

    def get_subtitle(self, targets, constant_level=1, constant_enemy_number=1, constant_star=1):
        return self.value[1].format(
            level=constant_level,
            enemies=str(constant_enemy_number)+'x[' + ','.join(target.__repr__() for target in targets) + ']',
            stars=constant_star,
            )


class YAxis(Enum):
    DPS = (('Towers', 'Weapons', 'Bandits', 'Guardians'),
           "damage / sec{divide_cost}",
           lambda unit_type, targets: unit_type.dps_score(targets))
    HP = (('Vehicules', 'Bandits', 'Guardians'),
          "hp * armor * esquive {divide_cost}",
          lambda unit_type, targets: unit_type.hp_score(targets))
    SCORE = (('Towers', 'Weapons', 'Vehicules', 'Bandits', 'Guardians'),
             "score",
             lambda unit_type, targets: unit_type.score(targets))

    def __init__(self, evaluable_categories, legend_string, exec_func):
        self.evaluable_categories = evaluable_categories
        self.legend_string = legend_string
        self.exec_func = exec_func

    def get_legend(self, category: str):
        return self.legend_string.format(divide_cost=" / "+COST_DISPLAY[category] if COST_DISPLAY[category] is not None else "")

    def exec(self, unit: BaseUnit, targets):
        return self.exec_func(unit, targets)


def plot_dps(targets_sample: List[MovableUnit], x_axis=XAxis.ENEMY_NUMBER, y_axis: YAxis = YAxis.SCORE, use_stock=False, **kwargs):
    # Check incompatible configurations
    assert (not use_stock) or (x_axis is not XAxis.LEVEL and x_axis is not XAxis.STAR), "You can't use your card stock (that define level and star of card) when using LEVEL or STAR as X avis variable"

    # Select the unit reference set (e.g. your own card stock or the absolute unit class list)
    unit_dictionnary = MY_CARDS if use_stock else CARD_DICTIONNARY

    figures = []
    for category in y_axis.evaluable_categories:
        # generate plot window
        fig = plt.figure()
        ax = plt.subplot(1, 1, 1, title=category + '\n' + x_axis.get_subtitle(targets_sample, **kwargs))
        ax.set_xlabel(x_axis.get_legend())
        ax.set_ylabel(y_axis.get_legend(category))

        y_max = 0
        xs_if_no_x_axis = []
        ys_if_no_x_axis = []
        for k, unit_type in enumerate(unit_dictionnary[category]):
            print(unit_type)
            ys = []
            xs = []
            for x, level, num_enemy, stars in x_axis.iter(**kwargs):
                if isinstance(unit_type, CardStock):
                    # assert (x_axis is not XAxis.LEVEL and x_axis is not XAxis.STAR), "You can't use your card stock (that define level and star of card) when using LEVEL or STAR as X avis variable"
                    unit = unit_type.card
                elif isinstance(unit_type, BaseUnit):
                    unit = unit_type
                else:
                    assert issubclass(unit_type, BaseUnit)
                    # unit_type is a class, subclass of BaseUnit
                    unit = unit_type(level, stars)
                targets = targets_sample * num_enemy

                y = y_axis.exec(unit, targets)
                if y is not None:
                    ys.append(y)
                    xs.append(x)
            if len(ys) > 0:
                if x_axis is not XAxis.NONE:
                    ax.plot(xs, ys, ["+-", "+-.", "+:"][k//10], label=unit_type.__name__)
                else:
                    xs_if_no_x_axis.append(unit_type.__name__)
                    ys_if_no_x_axis.append(y)
                y_max = max(y_max, max(ys))
        if x_axis is XAxis.NONE:
            ax.bar(*(list(t) for t in zip(*sorted(zip(xs_if_no_x_axis, ys_if_no_x_axis), key=lambda x: x[1]))))
            plt.xticks(rotation=70)
        ax.set_ylim(0, y_max * 1.05)
        ax.legend(ncol=2, fontsize='xx-small')
        figures.append(fig)
    return figures


if __name__ == '__main__':
    # Generate target sample

    #targets_sample = [FakeMovableUnit(TargetType.AIR_GROUND, armor=0, armor_piercing=0, can_miss=True)]
    targets_sample = [bandits.Mecha(1, stars=4)]


    #figures = plot_dps(targets_sample, x_axis=XAxis.ENEMY_NUMBER)
    figures = plot_dps(targets_sample, x_axis=XAxis.ENEMY_NUMBER, y_axis=YAxis.SCORE)
    plt.show()
