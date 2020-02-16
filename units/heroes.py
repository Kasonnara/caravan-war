from target_types import TargetType
from units.base_units import MovableUnit
from units.equipments import Weapon, Armor


class Hero(MovableUnit):
    level_grow_factor = 1.018
    ultimate = False


class HeroSpell:
    def __init__(self, level):
        assert 0 < level <= 5
        self.level = level


class Zora(Hero):
    hp_base = 18000
    attack_base = 3150

    atk_speed = 0.7
    range = 10
    move_speed = 1.3
    armor = 0
    armor_piercing = 0
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND

    class IceArrow(HeroSpell):
        effect_radius = 5
        slow_factor = 0.5
        slow_duration = 3
        ultimate = True

        @classmethod
        def damage_factor(self, level=1):
            return 1.5 + 0.5 * level

        @property
        def dmg_factor(self):
            return self.damage_factor(self.level)

    class ArrowFlight(HeroSpell):
        arrow_number = 10
        effect_radius = 3
        hit_chance = 0.2

        @classmethod
        def damage_factor(self, level=1):
            return 0.55 + 0.05 * level

        @property
        def dmg_factor(self):
            return self.damage_factor(self.level)

    class FastHand(HeroSpell):
        @classmethod
        def attack_speed_factor(self, level=1):
            return 15 + None * level

        @property
        def atk_speed_factor(self):
            return self.arttack_speed_factor(self.level)

    class PiercingShot(HeroSpell):
        pass

    class BounceArrow(HeroSpell):
        pass

    def __init__(self, level: int, ice_arrow=1, arrow_flight=None, fast_hand=None, percing_shot=None, bounce_arrow=None):
        super().__init__(level, 0, None, None)
        self.spells = [
            self.IceArrow(ice_arrow),
            ]
        if arrow_flight is not None:
            self.spells.append(self.ArrowFlight(arrow_flight))
        if fast_hand is not None:
            self.spells.append(self.FastHand(fast_hand))
        if arrow_flight is not None:
            self.spells.append(self.PiercingShot(percing_shot))
        if arrow_flight is not None:
            self.spells.append(self.BounceArrow(bounce_arrow))


class Dalvir(Hero):
    hp_base = 27000
    attack_base = 2750

    atk_speed = 0.5
    range = 1.5
    move_speed = 1.35
    armor = 2
    armor_piercing = 0
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND

    class WarriorRage(HeroSpell):
        aoe_lenght = 10
        stun_duration = 2
        ultimate = True
        damage_factor = {1:80, 2:90, 3:100, 4:125, 5:150}

        @property
        def dmg_factor(self):
            return self.damage_factor[self.level]

    class ButalShield(HeroSpell):
        damage_reduction = 0.85
        @classmethod
        def armor_bonus(cls, level):
            return 9 + level
        armor_bonus_duration = 5
        hit_chance = 0.15

    class StrongWill(HeroSpell):
        radius = 10
        heath_threshold = 0.5

        @classmethod
        def armor_bonus(cls, level):
            return 2 + level

    class KnightFury(HeroSpell):
        damage_reduction = 0.6
        attack_speed_factor = 2.5
        effect_duration = 7
        hit_chance = 0.1

    class IronProtection(HeroSpell):
        @classmethod
        def hp_bonus(cls, level):
            return 0.05 + None * level

    def __init__(self, level: int, warrior_rage=1, butal_shield=None, strong_will=None, knight_fury=None, iron_protection=None):
        super().__init__(level, 0, None, None)
        self.spells = [
            self.WarriorRage(warrior_rage),
            ]
        if butal_shield is not None:
            self.spells.append(self.ButalShield(butal_shield))
        if strong_will is not None:
            self.spells.append(self.StrongWill(strong_will))
        if knight_fury is not None:
            self.spells.append(self.KnightFury(knight_fury))
        if iron_protection is not None:
            self.spells.append(self.IronProtection(iron_protection))
