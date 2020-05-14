"""
This can be modified to represent the full inventory of card that you have: buidings, units, number of copies,
their levels, their stars, theirs equipments, etc.

You must a least replace all occurrences of "FILL_*" for example <FILL_BUILDING_LEVEL>

To simplify filling value I suggest that you Find+ReplaceAll occurrences of <FILL_BUILDING_LEVEL>, <FILL_ITEM_LEVEL>,
<FILL_BANDIT_LEVEL>, <FILL_GUARDIAN_LEVEL>, <FILL_VEHICLE_LEVEL> and <FILL_TOWER_LEVEL> to the value that correspond to
the majority of your units, then finish by manually setting remaining values.

"""

from collections import namedtuple
from typing import Type

from buildings.buildings import Mill, TransportStation, Bank, Storage, Laboratory, Tavern, Camp, Academy, Weaponsmith, \
    Garage, WorkShop, Forge, HeroTemple, Altar
from buildings.headquarters import HQ
from common.card_categories import CardCategories
from spells.spells import Ice, Storm, Meteor, Poison, Landmine, Arrow
from spells.convoy_boosts import AttackSpeedBoost, AttackBoost, LifeBoost, SpeedBoost, VehicleArmor, ModuleBoost
from units.bandits import Demon, Djin, Inferno, VikingLeg, StealerLeg, Chaman, DarkKnightLeg, Mecha, DarkKnight, Lich, \
    Viking, Stealer, Berserk, Spider, Hunter, Brute, Alchimist, Maraudeur, Lutin, Drone, Archer, Condor, Momie, LichLeg, \
    MomieLeg, CondorLeg
from units.equipments import Weapon, Armor
from units.guardians import Seraphin, Golem, DemonSlayer, Canonner, Paladin, Hammer, Sparte, Griffon, Marchal, Sword, \
    Jetpack, Shield, Knight, Healer, Guard, Scout, Follet, Wizard, SparteLeg, GriffonLeg, HammerLeg, PaladinLeg, \
    MarchalLeg
from units.heroes import Zora, Dalvir
from units.towers import Sentinelle, Arbalete, Eolance, Sniper, HeavySniper, Mage, Lightning, Stormspire, Fire, Bomber, \
    Canon, Hydra, MissileLaucher, Hospital, Armory, Tambour, Garnison
from units.vehicles import Train, Dirigeable, Helicopter, Wagon, Chariot, Charrette, Speeder, Buggy, WagonLeg, \
    HelicopterLeg, BuggyLeg
from units.modules import Shotgun, Mortar, Chaingun, Laser, Tesla, FlameTrower, Balista, LaserLeg, ChaingunLeg, \
    FlameTrowerLeg, Barrier, Harpon

CardStock = namedtuple('CardStock', 'card quantity')
"""A named tuple containing a unit type and the number of copies owned for units of which more than one copy c
an be obtained."""

buildings = {
    HQ(FILL_BUILDING_LEVEL),
    Mill(FILL_BUILDING_LEVEL),
    TransportStation(FILL_BUILDING_LEVEL),
    Bank(FILL_BUILDING_LEVEL),
    Storage(FILL_BUILDING_LEVEL),
    Laboratory(FILL_BUILDING_LEVEL),
    Tavern(FILL_BUILDING_LEVEL),
    Camp(FILL_BUILDING_LEVEL),
    Academy(FILL_BUILDING_LEVEL),
    Weaponsmith(FILL_BUILDING_LEVEL),
    Garage(FILL_BUILDING_LEVEL),
    WorkShop(FILL_BUILDING_LEVEL),
    Forge(FILL_BUILDING_LEVEL),
    HeroTemple(FILL_BUILDING_LEVEL),
    Altar(FILL_BUILDING_LEVEL),
    }

buildings_dict = {
    type(building).__name__: building
    for building in buildings
    }

guardians = {
    CardStock(Seraphin(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Wizard(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Golem(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Canonner(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(SparteLeg(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(GriffonLeg(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(DemonSlayer(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(HammerLeg(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(PaladinLeg(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(MarchalLeg(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),

    CardStock(Griffon(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Sparte(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Paladin(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Marchal(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Hammer(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),

    CardStock(Knight(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Shield(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Jetpack(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Sword(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Healer(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),

    CardStock(Guard(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Scout(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Follet(FILL_GUARDIAN_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    }

bandits = {
    CardStock(Demon(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Djin(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Inferno(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Chaman(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(MomieLeg(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(VikingLeg(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(StealerLeg(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(LichLeg(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(DarkKnightLeg(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Mecha(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(CondorLeg(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),

    CardStock(Condor(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(DarkKnight(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Momie(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Viking(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Lich(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Stealer(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),

    CardStock(Berserk(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Spider(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Hunter(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Brute(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Alchimist(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Lutin(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),

    CardStock(Maraudeur(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Archer(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Drone(FILL_BANDIT_LEVEL, stars=0, weapon_item=Weapon(FILL_ITEM_LEVEL), armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    }

vehicles = {
    CardStock(Train(FILL_VEHICLE_LEVEL, stars=0, armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Dirigeable(FILL_VEHICLE_LEVEL, stars=0, armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Helicopter(FILL_VEHICLE_LEVEL, stars=0, armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Wagon(FILL_VEHICLE_LEVEL, stars=0, armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Charrette(FILL_VEHICLE_LEVEL, stars=0, armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Chariot(FILL_VEHICLE_LEVEL, stars=0, armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Speeder(FILL_VEHICLE_LEVEL, stars=0, armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(Buggy(FILL_VEHICLE_LEVEL, stars=0, armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(WagonLeg(FILL_VEHICLE_LEVEL, stars=0, armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(HelicopterLeg(FILL_VEHICLE_LEVEL, stars=0, armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
    CardStock(BuggyLeg(FILL_VEHICLE_LEVEL, stars=0, armor_item=Armor(FILL_ITEM_LEVEL)), FILL_QUANTITY),
}

modules = {
    CardStock(Harpon(FILL_MODULE_LEVEL, stars=0), FILL_QUANTITY),
    CardStock(Tesla(FILL_MODULE_LEVEL, stars=0), FILL_QUANTITY),
    CardStock(Barrier(FILL_MODULE_LEVEL, stars=0), FILL_QUANTITY),
    CardStock(Cryomancer(FILL_MODULE_LEVEL, stars=0), FILL_QUANTITY),
    CardStock(Archidruid(FILL_MODULE_LEVEL, stars=0), FILL_QUANTITY),
    CardStock(ShieldInvoker(FILL_MODULE_LEVEL, stars=0), FILL_QUANTITY),
    CardStock(MirrorWizard(FILL_MODULE_LEVEL, stars=0), FILL_QUANTITY)
    CardStock(Laser(FILL_MODULE_LEVEL, stars=0), FILL_QUANTITY),
    CardStock(LaserLeg(FILL_MODULE_LEVEL, stars=0), FILL_QUANTITY),
    CardStock(Chaingun(FILL_MODULE_LEVEL, stars=0), FILL_QUANTITY),
    CardStock(ChaingunLeg(FILL_MODULE_LEVEL, stars=0), FILL_QUANTITY),
    CardStock(FlameTrower(FILL_MODULE_LEVEL, stars=0), FILL_QUANTITY),
    CardStock(FlameTrowerLeg(FILL_MODULE_LEVEL, stars=0), FILL_QUANTITY),
    CardStock(Mortar(FILL_MODULE_LEVEL, stars=0), FILL_QUANTITY),
    CardStock(Shotgun(FILL_MODULE_LEVEL, stars=0), FILL_QUANTITY),
    CardStock(Balista(FILL_MODULE_LEVEL, stars=0), FILL_QUANTITY),
    }

spells = {
    Ice(FILL_SPELL_LEVEL),
    Storm(FILL_SPELL_LEVEL),
    Meteor(FILL_SPELL_LEVEL),
    Poison(FILL_SPELL_LEVEL),
    Landmine(FILL_SPELL_LEVEL),
    Arrow(FILL_SPELL_LEVEL),
    }

convoy_boosts = {
    VehicleArmor(FILL_SPELL_LEVEL),
    ModuleBoost(FILL_SPELL_LEVEL),
    SpeedBoost(FILL_SPELL_LEVEL),
    AttackSpeedBoost(FILL_SPELL_LEVEL),
    AttackBoost(FILL_SPELL_LEVEL),
    LifeBoost(FILL_SPELL_LEVEL),
    }

heroes = {
    Zora(FILL_HERO_LEVEL, FILL_SPELL_1_LEVEL, FILL_SPELL_2_LEVEL, etc),
    Dalvir(FILL_HERO_LEVEL, FILL_SPELL_1_LEVEL, FILL_SPELL_2_LEVEL, etc),
    Ghohral(FILL_HERO_LEVEL, FILL_SPELL_1_LEVEL, FILL_SPELL_2_LEVEL, etc),
    AilulSnowsinger(FILL_HERO_LEVEL, FILL_SPELL_1_LEVEL, FILL_SPELL_2_LEVEL, etc),
    MardonDarkflame(FILL_HERO_LEVEL, FILL_SPELL_1_LEVEL, FILL_SPELL_2_LEVEL, etc),
    }

ARROW_TOWER_STARS = 0
MAGE_TOWER_STARS = 0
CANON_TOWER_STARS = 0
SUPPORT_TOWER_STARS = 0

towers = {
    Sentinelle(FILL_TOWER_LEVEL, stars=ARROW_TOWER_STARS),
    Arbalete(FILL_TOWER_LEVEL, stars=ARROW_TOWER_STARS),
    Eolance(FILL_TOWER_LEVEL, stars=ARROW_TOWER_STARS),
    Sniper(FILL_TOWER_LEVEL, stars=ARROW_TOWER_STARS),
    HeavySniper(FILL_TOWER_LEVEL, stars=ARROW_TOWER_STARS),

    Mage(FILL_TOWER_LEVEL, stars=MAGE_TOWER_STARS),
    Lightning(FILL_TOWER_LEVEL, stars=MAGE_TOWER_STARS),
    Stormspire(FILL_TOWER_LEVEL, stars=MAGE_TOWER_STARS),
    Fire(FILL_TOWER_LEVEL, stars=MAGE_TOWER_STARS),

    Bomber(FILL_TOWER_LEVEL, stars=CANON_TOWER_STARS),
    Canon(FILL_TOWER_LEVEL, stars=CANON_TOWER_STARS),
    Hydra(FILL_TOWER_LEVEL, stars=CANON_TOWER_STARS),
    MissileLaucher(FILL_TOWER_LEVEL, stars=CANON_TOWER_STARS),

    Hospital(FILL_TOWER_LEVEL, stars=SUPPORT_TOWER_STARS),
    Armory(FILL_TOWER_LEVEL, stars=SUPPORT_TOWER_STARS),
    Tambour(FILL_TOWER_LEVEL, stars=SUPPORT_TOWER_STARS),
    Garnison(FILL_TOWER_LEVEL, stars=SUPPORT_TOWER_STARS),
    }

MY_CARDS = {
        CardCategories.GUARDIANS: guardians,
        CardCategories.BANDITS: bandits,
        CardCategories.VEHICLES: vehicles,
        CardCategories.MODULES: modules,
        CardCategories.SPELLS: spells,
        CardCategories.CONVOY_BOOSTS: convoy_boosts,
        CardCategories.HEROES: heroes,
        CardCategories.BUILDINGS: buildings,
        CardCategories.TOWERS: towers,
    }
"""Just a dictionary to access stocks of this module using category strings"""
