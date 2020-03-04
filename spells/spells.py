from common.cards import Card
from common.rarity import Rarity
from utils.class_property import classproperty


class Spell(Card):
    category = "Spells"

    def __init__(self, level: int):
        super().__init__(level, 0)

    @classproperty
    def gem_cost(cls):
        return cls.rarity.spell_gem_cost

    @classmethod
    def gold_cost(cls, ligue: 'Ligue'):
        return cls.rarity.spell_gold_cost(ligue)


class Arrow(Spell):
    rarity = Rarity.Common


class Landmine(Spell):
    rarity = Rarity.Common


class Storm(Spell):
    rarity = Rarity.Epic


class Ice(Spell):
    rarity = Rarity.Epic


class Poison(Spell):
    rarity = Rarity.Rare


class Meteor(Spell):
    rarity = Rarity.Rare


class ConvoyBoost(Card):
    category = "ConvoyBoosts"


class AttackSpeedBoost(ConvoyBoost):
    boost = 8
    rarity = Rarity.Rare


class AttackBoost(ConvoyBoost):
    boost = 4
    rarity = Rarity.Common


class LifeBoost(ConvoyBoost):
    boost = 4
    rarity = Rarity.Common


class SpeedBoost(ConvoyBoost):
    boost = 8
    rarity = Rarity.Rare


class VehiculeBoost(ConvoyBoost):
    boost = 15
    rarity = Rarity.Epic


class ModuleBoost(ConvoyBoost):
    boost = 15
    rarity = Rarity.Epic
