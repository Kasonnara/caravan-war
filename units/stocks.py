from collections import namedtuple
from typing import Type

from cards import Card
from units.bandits import Demon, Djin, Inferno, VikingLeg, StealerLeg, Chaman, DarkKnightLeg, Mecha, DarkKnight, Lich, \
    Viking, Stealer, Berserk, Spider, Hunter, Brute, Alchimist, Maraudeur, Lutin, Drone, Archer, Condor, Momie
from units.base_units import MovableUnit
from units.guardians import Seraphin, Golem, DemonSlayer, Canonner, Paladin, Hammer, Sparte, Griffon, Marchal, Sword, \
    Jetpack, Shield, Knight, Healer, Guard, Scout, Follet


CardStock = namedtuple('CardStock', 'card quantity')


class ObjectStock(CardStock):
    pass


QG_LEVEL = 8
#                wave width |          waves number        |       wave length
GUARDIAN_POWER =      6     * min(5, (QG_LEVEL + 1) * 0.5) * max(10, min(20, QG_LEVEL))

guardians = [
    CardStock(Seraphin(8), 3),
    CardStock(Golem(8), 1),
    CardStock(DemonSlayer(8), 2),
    CardStock(Canonner(8), 0),

    CardStock(Paladin(8), 1),
    CardStock(Hammer(8), 4),
    CardStock(Sparte(8), 10),
    CardStock(Griffon(8), 4),
    CardStock(Marchal(8), 5),

    CardStock(Sword(8), 31),
    CardStock(Jetpack(8), 29),
    CardStock(Shield(8), 34),
    CardStock(Knight(8), 47),
    CardStock(Healer(8), 29),

    CardStock(Guard(7, stars=2), 100),
    CardStock(Scout(6, stars=2), 100),
    CardStock(Follet(6, stars=2), 100),
]

TAVERNE_LEVEL = 8
BANDIT_POWER = 25 + TAVERNE_LEVEL * 15

bandits = [
    CardStock(Demon(8), 4),
    CardStock(Djin(8), 1),
    CardStock(Inferno(8), 2),
    CardStock(Chaman(8), 1),
    CardStock(VikingLeg(8), 3),
    CardStock(StealerLeg(8), 2),
    CardStock(DarkKnightLeg(8), 2),
    CardStock(Mecha(8), 4),

    CardStock(Condor(8), 3),
    CardStock(DarkKnight(7), 1),
    CardStock(Momie(8), 2),
    CardStock(Viking(6), 2),
    CardStock(Lich(8), 4),
    CardStock(Stealer(8), 1),

    CardStock(Berserk(8), 32),
    CardStock(Spider(8), 16),
    CardStock(Hunter(7, stars=1), 25),
    CardStock(Brute(5, stars=1), 1),
    CardStock(Alchimist(8), 34),
    CardStock(Lutin(8), 13),

    CardStock(Maraudeur(6, stars=2), 100),
    CardStock(Archer(6, stars=2), 100),
    CardStock(Drone(5, stars=2), 100),
    ]
