from cards import Card, Rarity


class Spell(Card):
    category = "Spells"


class Arrow(Spell):
    gold_cost = 500  # or 425??
    rarity = Rarity.Common


class Landmine(Spell):
    gold_cost = 500
    rarity = Rarity.Common


class Storm(Spell):
    rarity = Rarity.Epic


class Ice(Spell):
    rarity = Rarity.Epic


class Poison(Spell):
    rarity = Rarity.Rare
    gold_cost = 1000


class Meteor(Spell):
    buy_cost = 1000  # or 850
    gem_cost = 4
    rarity = Rarity.Rare


class ConvoyBoost(Card):
    category = "ConvoyBoosts"


class AttackSpeedBoost(ConvoyBoost):
    boost = 8


class AttackBoost(ConvoyBoost):
    boost = 4


class LifeBoost(ConvoyBoost):
    boost = 4


class SpeedBoost(ConvoyBoost):
    boost = 8
