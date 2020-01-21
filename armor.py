from math import sqrt, log

import matplotlib.pyplot as plt

armor_table = {0: 0, 2: 10.83, 3: 15, 4: 18.57, 5: 21.67, 6: 24.37, 8: 28.89}


def armor_reduction(armor_level: int) -> float:
    return (100 - armor_table[max(0, armor_level)]) / 100


def f(x):
    #return sqrt(x) * armor_table[2]/sqrt(2)
    #return x**(5/7) * armor_table[2] / 2**(5/7)
    #return log(x+1) * armor_table[2] / log(2+1)

    # Wolfram Alpha
    # fit {{0, 0}, {2, 10.83}, {3, 15}, {4, 18.57}, {5, 21.67}, {6, 24.37}, {8, 28.89}}
    #return 0.0187255 * x ** 3 - 0.484128 * x ** 2 + 6.28577 * x
    #return -0.259422 * x**2 + 5.63037 * x
    #return 13.0218 * log(0.883713 * x)

    return -0.20119 * x**2 + 5.00148 * x + 1.712
    #return 0.0143478 * x**3 - 0.416408 * x**2 + 5.96852 * x + 0.446522
    #return -0.000762579 * x**4 + 0.0291352 * x**3 - 0.516533 * x**2 + 6.24645 * x + 0.182736


print(armor_table)

if __name__ == '__main__':
    plt.plot(sorted(list(armor_table.keys())), sorted(list(armor_table.values())), "+", label="real values")
    plt.plot(range(30), list(f(x) for x in range(30)), label="f(x)")
    plt.xlabel("level")
    plt.ylabel("Damage reduction (%)")
    plt.legend()
    plt.show()

for k in range(30):
    armor_table.setdefault(k, f(min(k, 10)))

