from enum import auto, Enum
from math import ceil
from typing import List

import matplotlib.pyplot as plt

from target_types import TargetType
from units.base_units import UNIT_DICTIONNARY, MAX_LEVEL, FakeMovableUnit, MovableUnit
import units.bandits as bandits
import units.guardians as guardians
import units.towers as towers
import units.vehicules as vehicules
import units.weapons as weapons


COST_DISPLAY = {'Towers': "cost", 'Weapons': "1", 'Bandits': "cost", 'Guardians': "used cell", 'Vehicules': "used cell"}

# TODO: split output scores in different labelized pandas dataframe (to sum in general case and plot in different colors in bar plot)

class XAxis(Enum):
    LEVEL = "Level", "(constant: stars={stars), enemies in AOE=[{enemies}])"
    ENEMY_NUMBER = "Enemy count inside area of effect", "(constant: level={level}, stars={stars}, enemies in AOE=Nx[{enemies}])"
    STAR = "Card stars", "(constant: level={level}, enemies in AOE=[{enemies}])"
    NONE = "", "(constant: level={level},  stars={stars}, enemies in AOE=[{enemies}], stars={stars})"

    def iter(self, constant_level=1, constant_enemy_number=1, constant_star=1, variable_range=7):
        self.cache = {"level": constant_level, "enemy_count": constant_enemy_number ,"star": constant_star}

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
            enemies=str(constant_enemy_number)+'x[' + ','.join(target.to_string() for target in targets) + ']',
            stars=constant_star,
            )


class YAxis(Enum):
    DPS = ('Towers', 'Weapons', 'Bandits', 'Guardians'), "damage / sec{divide_cost}", lambda unit_type: unit_type.dps_ratio
    HP = ('Vehicules', 'Bandits', 'Guardians'), "hp * armor * esquive {divide_cost}", lambda unit_type: unit_type.hp_ratio
    SCORE = ('Towers', 'Weapons', 'Vehicules', 'Bandits', 'Guardians'), "score", lambda unit_type: unit_type.score

    @property
    def evaluable_categories(self):
        return self.value[0]

    def get_legend(self, category: str):
        return self.value[1].format(divide_cost=" / "+COST_DISPLAY[category] if COST_DISPLAY[category] is not None else "")

    def exec(self, unit_type, targets, level):
        return self.value[2](unit_type)(targets, level)


def plot_dps(targets_sample: List[MovableUnit], x_axis=XAxis.LEVEL, y_axis: YAxis = YAxis.SCORE, **kwargs):
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
        for k, unit_type in enumerate(UNIT_DICTIONNARY[category]):
            print(unit_type)
            ys = []
            xs = []
            for x, level, num_enemy, star in x_axis.iter(**kwargs):
                targets = targets_sample * num_enemy
                y = y_axis.exec(unit_type, targets, level)
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
