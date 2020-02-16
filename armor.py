from math import sqrt, log, log10

import matplotlib.pyplot as plt

armor_table = {0: 0, 0.5: 3.10, 1: 5.91, 1.5: 8.48, 2: 10.83, 3: 15.00, 4: 18.57, 4.5: 20.17, 5: 21.67, 6: 24.37, 7:26.78, 8: 28.89, 9.5: 31.67}


def armor_reduction(armor_level: int) -> float:
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
    #return 13.0218 * log(0.883713 * x)

    #return -0.20119 * x**2 + 5.00148 * x + 1.712
    #return 0.0143478 * x**3 - 0.416408 * x**2 + 5.96852 * x + 0.446522
    #return -0.000762579 * x**4 + 0.0291352 * x**3 - 0.516533 * x**2 + 6.24645 * x + 0.182736

    # Geogebra:
    # 0.01 x * y - 0.99x + 0.15 y = 0 (sorte de fonction a/(x-b) + c?)
    # 0.01 x2 y - 0.38x2 + 0.21 xy - 0.89x - 0.02y2 + 0.14y = 0 (idem)
    # poly2 : -0.23x2 + 5.38x + 0.59
    # poly3 : 0.02x3 -0.45x2 +6.18x +0.1
    # poly4 : 0x4 + 0.04x3 - 0.58x2 +6.43x +0.01
    return x/0.15

print(armor_table)



if __name__ == '__main__':
    plt.plot(sorted(list(armor_table.keys())), sorted(list(armor_table.values())), "+", label="real values")
    xs = range(20)
    ys = list(f(x) for x in xs)
    plt.plot(xs, ys, label="f(x)")
    print(ys)
    plt.xlabel("level")
    plt.ylabel("Damage reduction (%)")
    plt.legend()
    plt.show()

#print(f(0))

for k in range(30):
    armor_table.setdefault(k, f(min(k, 10)))


