import unittest

from buildings.base_buildings import Building
from buildings.buildings import Tavern, Academy, WorkShop, Mill
from buildings.headquarters import HQ
from common.card_categories import CardCategories
from common.cards import Upgradable, MAX_LEVEL, Upgrade
from common.resources import ResourcePacket, Resources
from config.my_cards import MY_CARDS, CardStock
from spells.spells import Spell
from spells.convoy_boosts import ConvoyBoost
from units.bandits import Bandit, Demon
from units.guardians import Guardian
from units.heroes import Hero, Zora
from units.modules import ModuleWeapon
from units.towers import Tower, Eolance, HeavySniper
from units.vehicles import Vehicle


class UpgradableTestCase(unittest.TestCase):
    def assertUpgradeEqual(self, upgrade_expected: Upgrade, upgrade_found: Upgrade):
        self.assertDictEqual(upgrade_expected.costs, upgrade_found.costs,
                             "Upgrade cost mismatch")
        self.assertCountEqual(upgrade_expected.requirements, upgrade_found.requirements,
                              "Upgrade Dependancies mismatch")

    def test_cards_extends_upgradable(self):
        # Test unit group abstract classes
        for category in CardCategories:
            with self.subTest(category=category.name):
                self.assertTrue(issubclass(category.card_base_class, Upgradable),
                                "{} should be a subclass of Upgradable".format(category.card_base_class.__name__))

        # Test all units
        for category in CardCategories:
            for card_type in category:
                with self.subTest(card=card_type.__name__):
                    self.assertTrue(issubclass(card_type, Upgradable),
                                    "{} should be a subclass of Upgradable".format(card_type.__name__))

    @unittest.skip("upgrade cost data not added to units yet")
    def test_previous_next_upgrade_match(self):
        # We do not make a fuzzing test: only some upgradable classes that might have different upgrade functions,
        # at some key levels (mainly minimum and maximum)

        for upgradable_type in [HQ, Mill, Demon, Eolance, Zora]:
            for level in [0, 10, 20, MAX_LEVEL - 1]:
                with self.subTest(card=upgradable_type.__name__, level=level):
                    self.assertUpgradeEqual(
                        upgradable_type(level).get_next_upgrade(),
                        upgradable_type(level + 1).get_previous_upgrade()
                        )

    def test_get_upgrade(self):
        with self.subTest(name="HQ upgrade 14 -> 15"):
            # An head-quarters upgrade from lvl 14 to 15
            self.assertUpgradeEqual(
                Upgrade(
                    ResourcePacket(Resources.Goods(-11800000), Resources.Gold(-56400000)),
                    (HQ(14), Tavern(14), Academy(14), WorkShop(14)),
                    ),
                HQ(15).get_previous_upgrade()
                )

        with self.subTest(name="HeavySniper upgrade 9 -> 10"):
            hs9 = HeavySniper(9)
            self.assertUpgradeEqual(
                Upgrade(
                    ResourcePacket(Resources.Goods(0), Resources.Gold(-710000)),
                    (WorkShop(10), hs9),
                    ),
                hs9.get_next_upgrade()
                )

    def test_cost_negativity(self):
        for category in CardCategories:
            for card in category:
                with self.subTest(card=card.__name__):
                    for upgrade_cost in card.upgrade_costs:
                        if upgrade_cost is None:
                            continue  # FIXME: remove this line as soon as we have filled all None values
                        self.assertTrue(
                            all([resource_cost <= 0 for resource_cost in upgrade_cost.values()]),
                            "An upgrade should cost resources, so its upgrade_costs ResourcePackets should contains negative values. Check if you don't missed a '-' character."
                            )


if __name__ == '__main__':
    unittest.main()
