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


"""
Record data and attempt to find exact armor formula
"""

from math import sqrt, log, log10

import matplotlib.pyplot as plt

armor_table = {0: 0, 0.5: 3.10, 1: 5.91, 1.5: 8.48, 2: 10.83, 3: 15.00, 4: 18.57, 4.5: 20.17, 5: 21.67, 6: 24.37,
               6.5: 25.61, 7: 26.78, 8: 28.89, 9: 30.79, 9.5: 31.67, 10: 32.50}
"""Known armor value"""

def armor_reduction(armor_level: int) -> float:
    """
    :param armor_level: int, level of armor to apply (after subtraction of the attacker armor piercing)
    :return: float, damage reduction factor for the corresponding armor value
    """
    return (100 - armor_table[max(0, armor_level)]) / 100


def g(x, a, b):
    return x**(a/b) * armor_table[2] / 2**(a/b)


#b = (len(armor_table) * sum([armor_table[k] * log(k + 1) for k in armor_table]) - sum(armor_table.values()) * sum([log(k + 1) for k in armor_table])
#     ) / (len(armor_table) * sum([log(k + 1)**2 for k in armor_table]) - sum([log(k + 1) for k in armor_table])**2)
#a = (sum(armor_table.values()) - b*sum([log(k + 1) for k in armor_table])) / len(armor_table)
#print(a, b)

def f(x):
    #return sqrt(x) * armor_table[2]/sqrt(2)
    #return x**(5/7) * armor_table[2] / 2**(5/7)
    #return log(x+1) * armor_table[2] / log(2+1)
    #return log10(x + 1) * armor_table[2] / log10(2 + 1)
    #return log(x + 1, 0.1) * armor_table[9.5] / log(9.5 + 1, 0.1)
    #return a + b*log(x+1)

    #return sum([3.1*0.913**i for i in range(2*x)])



    # Wolfram Alpha
    # fit {{0, 0}, {2, 10.83}, {3, 15}, {4, 18.57}, {5, 21.67}, {6, 24.37}, {8, 28.89}}
    #return 0.0187255 * x ** 3 - 0.484128 * x ** 2 + 6.28577 * x
    #return -0.259422 * x**2 + 5.63037 * x
    #return 20 * log(0.4 * x + 1)
    #return 23 * log(0.3 * x + 1)
    #return 24.221188606718492 * log(0.28587109374999997 * x + 1)  # minimum by first dicotomy
    # return 24.0954206844332 * log(0.2886886886886887 * x + 1)  # minimum by first brute force
    return 23.648706120050402 * log(0.29522394769958915 * x + 1)   # minimum by second dicotomy
    #return 24.11859783964244 * log(0.2883883883883884 * x + 1)  # minimum by second brute force

    #return -0.20119 * x**2 + 5.00148 * x + 1.712
    #return 0.0143478 * x**3 - 0.416408 * x**2 + 5.96852 * x + 0.446522
    #return -0.000762579 * x**4 + 0.0291352 * x**3 - 0.516533 * x**2 + 6.24645 * x + 0.182736

    # Geogebra:
    # 0.01 x * y - 0.99x + 0.15 y = 0 (sorte de fonction a/(x-b) + c?)
    # 0.01 x2 y - 0.38x2 + 0.21 xy - 0.89x - 0.02y2 + 0.14y = 0 (idem)
    # poly2 : -0.23x2 + 5.38x + 0.59
    # poly3 : 0.02x3 -0.45x2 +6.18x +0.1
    # poly4 : 0x4 + 0.04x3 - 0.58x2 +6.43x +0.01
    # return x/0.15


if __name__ == '__main__':
    # We guess that armor formula has this form. It always satify our first point g(0) = 0
    def g(a, b, x):
        return a * log(b * x + 1)


    def deduce_a(new_b):
        # Compute the correct value of a to match another point g(3) = 15
        new_a = armor_table[3] / g(1, new_b, 3)
        # Now check a third point
        error = armor_table[8] - round(g(new_a, new_b, 8), 2)
        return error, new_a

    if False:

        # We iteratively try multiples values of b by dicotomy
        b_min, b_max = 0.001, 1
        assert deduce_a(b_min)[0] < 0
        assert deduce_a(b_max)[0] > 0

        close_enough = False
        EXPECTED_PRECISION = 0.5 * 10**-2
        while not close_enough:
            new_b = (b_min + b_max) / 2
            print(new_b)
            error, new_a = deduce_a(new_b)
            true_error = max(abs(armor_table[x] - round(g(new_a, new_b, x), 2)) for x in armor_table)
            if true_error <= EXPECTED_PRECISION:
                close_enough = True
                print("found close match")
            elif error < 0:
                b_min = new_b
            else:
                b_max = new_b

            if abs(b_max - b_min) <= 10**-10:
                print("force stop")
                close_enough = True
        best_a, best_b = new_a, new_b
    else:
        # Brute force
        import numpy
        best_a, best_b, best_error = None, None, None
        for b in numpy.linspace(0.2, 0.3, 1000):
            #print(b)
            estimated_a = deduce_a(b)[1]
            for a in numpy.linspace(estimated_a - 5, estimated_a + 5, 1000):
                error = sum((armor_table[x] - round(g(a, b, x), 2))**2 for x in armor_table)
                if best_error is None or best_error > error:
                    best_a, best_b, best_error = a, b, error


    print("Formla found: g(x) = {a} * log({b} * x + 1)".format(a=best_a, b=best_b))
    def f(x):
        return best_a * log(best_b * x + 1)


if __name__ == '__main__':
    # print(armor_table)

        plt.plot(sorted(list(armor_table.keys())), sorted(list(armor_table.values())), "+", label="real values")
        xs = range(20)
        ys = list(f(x) for x in xs)
        plt.plot(xs, ys, label="f(x)")
        print(ys)
        plt.xlabel("level")
        plt.ylabel("Damage reduction (%)")
        plt.legend()
        plt.show()

        xs = sorted(list(armor_table.keys()))
        ys = [armor_table[x] - f(x) for x in xs]
        plt.bar(xs, ys, label="error")
        plt.show()

#print(f(0))

for k in range(30):
    armor_table.setdefault(k, f(k))


