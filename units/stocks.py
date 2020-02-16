from collections import namedtuple
from typing import Type

from cards import Card
from spells import Ice, Storm, Meteor, Poison, Landmine, Arrow, VehiculeBoost, ModuleBoost, SpeedBoost, \
    AttackSpeedBoost, AttackBoost, LifeBoost
from units.bandits import Demon, Djin, Inferno, VikingLeg, StealerLeg, Chaman, DarkKnightLeg, Mecha, DarkKnight, Lich, \
    Viking, Stealer, Berserk, Spider, Hunter, Brute, Alchimist, Maraudeur, Lutin, Drone, Archer, Condor, Momie, LichLeg, \
    MomieLeg, CondorLeg
from units.base_units import MovableUnit
from units.equipments import Weapon, Armor
from units.guardians import Seraphin, Golem, DemonSlayer, Canonner, Paladin, Hammer, Sparte, Griffon, Marchal, Sword, \
    Jetpack, Shield, Knight, Healer, Guard, Scout, Follet, Wizard, SparteLeg, GriffonLeg, HammerLeg, PaladinLeg
from units.heroes import Zora, Dalvir
from units.vehicules import Train, Dirigeable, Helicopter, Wagon, Chariot, Charrette
from units.weapons import Shotgun, Mortar, Chaingun, Laser, Tesla, FlameTrower, Balista

CardStock = namedtuple('CardStock', 'card quantity')


class ObjectStock(CardStock):
    pass


QG_LEVEL = 11
#                wave width |          waves number        |       wave length
GUARDIAN_POWER =      6     * min(5, (QG_LEVEL + 1) * 0.5) * max(10, min(20, QG_LEVEL))

guardians = [
    CardStock(Seraphin(11, armor_item=Armor(3)), 4),
    CardStock(Wizard(11), 2),
    CardStock(Golem(11), 4),
    CardStock(Canonner(11), 5),
    CardStock(SparteLeg(11, stars=5, weapon_item=Weapon(3)), 20),
    CardStock(GriffonLeg(11), 3),
    CardStock(DemonSlayer(11, weapon_item=Weapon(3)), 2),
    CardStock(HammerLeg(11, weapon_item=Weapon(3), armor_item=Armor(3)), 2),
    CardStock(PaladinLeg(11, armor_item=Armor(3)), 4),

    CardStock(Griffon(10, armor_item=Armor(3)), 1),
    CardStock(Sparte(9, stars=1, weapon_item=Weapon(3)), 10),
    CardStock(Paladin(10, armor_item=Armor(3)), 1),
    CardStock(Marchal(11, weapon_item=Weapon(3), armor_item=Armor(3)), 8),
    CardStock(Hammer(9, armor_item=Armor(3)), 1),

    CardStock(Knight(9, stars=2, weapon_item=Weapon(3)), 50),
    CardStock(Shield(8, stars=2, armor_item=Armor(3)), 30),
    CardStock(Jetpack(10, stars=1, weapon_item=Weapon(3)), 40),
    CardStock(Sword(8, stars=1, weapon_item=Weapon(3), armor_item=Armor(3)), 20),
    CardStock(Healer(9, stars=1), 40),

    CardStock(Guard(7, stars=5, weapon_item=Weapon(3), armor_item=Armor(3)), 100),
    CardStock(Scout(6, stars=5, weapon_item=Weapon(3), armor_item=Armor(3)), 100),
    CardStock(Follet(6, stars=5, weapon_item=Weapon(3), armor_item=Armor(3)), 100),
]

TAVERNE_LEVEL = 11
BANDIT_POWER = 25 + TAVERNE_LEVEL * 15

bandits = [
    CardStock(Demon(10, armor_item=Armor(3)), 4),
    CardStock(Djin(10, weapon_item=Weapon(3)), 1),
    CardStock(Inferno(10), 2),
    CardStock(Chaman(10), 1),
    CardStock(MomieLeg(10, weapon_item=Weapon(3), armor_item=Armor(3)), 4),
    CardStock(VikingLeg(8, weapon_item=Weapon(3), armor_item=Armor(3)), 6),
    CardStock(StealerLeg(10, stars=1, weapon_item=Weapon(3), armor_item=Armor(3)), 2),
    CardStock(LichLeg(10, weapon_item=Weapon(3), armor_item=Armor(3)), 3),
    CardStock(DarkKnightLeg(8, weapon_item=Weapon(3)), 3),
    CardStock(Mecha(10, stars=5), 32),
    CardStock(CondorLeg(8), 6),

    CardStock(Condor(8), 1),
    CardStock(DarkKnight(8), 1),
    CardStock(Momie(8, weapon_item=Weapon(3), armor_item=Armor(3)), 1),
    CardStock(Viking(6, armor_item=Armor(3)), 2),
    CardStock(Lich(8, stars=1, weapon_item=Weapon(3), armor_item=Armor(3)), 2),
    CardStock(Stealer(8), 7),

    CardStock(Berserk(8, stars=1, armor_item=Armor(3)), 30),
    CardStock(Spider(8, weapon_item=Weapon(3), armor_item=Armor(3)), 30),
    CardStock(Hunter(7, stars=2, armor_item=Armor(3)), 30),
    CardStock(Brute(5, stars=1), 30),
    CardStock(Alchimist(8, stars=1, weapon_item=Weapon(3)), 50),
    CardStock(Lutin(8, stars=2, weapon_item=Weapon(3), armor_item=Armor(3)), 40),

    CardStock(Maraudeur(6, stars=5, armor_item=Armor(3)), 100),
    CardStock(Archer(6, stars=5, armor_item=Armor(3)), 100),
    CardStock(Drone(5, stars=5, weapon_item=Weapon(3), armor_item=Armor(3)), 100),
    ]


vehicules = [
    CardStock(Train(9), 1),
    CardStock(Dirigeable(9), 1),
    CardStock(Helicopter(9), 2),
    CardStock(Wagon(9, armor_item=Armor()), 3),
    CardStock(Charrette(6, stars=1, armor_item=Armor()), 30),
    CardStock(Chariot(9, armor_item=Armor()), 30),
    ]

modules = [
    CardStock(Tesla(9), 2),
    CardStock(Laser(9), 1),
    CardStock(Chaingun(9), 4),
    CardStock(FlameTrower(9), 1),
    CardStock(Mortar(7), 20),
    CardStock(Shotgun(7), 30),
    CardStock(Balista(6, stars=2), 30),
    ]


spells = [
    CardStock(Ice(6), 1),
    CardStock(Storm(6), 1),
    CardStock(Meteor(6), 1),
    CardStock(Poison(6), 1),
    CardStock(Landmine(6), 1),
    CardStock(Arrow(6), 1),
    ]

convoy_boosts = [
    CardStock(VehiculeBoost(6), 1),
    CardStock(ModuleBoost(6), 1),
    CardStock(SpeedBoost(6), 1),
    CardStock(AttackSpeedBoost(6), 1),
    CardStock(AttackBoost(6), 1),
    CardStock(LifeBoost(6), 1),
    ]

heroes = [
    CardStock(Zora(12), 1),
    CardStock(Dalvir(2), 1),
    ]
