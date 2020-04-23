import unittest

from buildings.base_buildings import Building
from common.card_categories import CardCategories
from config.my_cards import CardStock, MY_CARDS


expected_to_be_CardStocks = {
    CardCategories.GUARDIANS: True,
    CardCategories.BANDITS: True,
    CardCategories.VEHICLES: True,
    CardCategories.MODULES: True,
    CardCategories.SPELLS: False,
    CardCategories.CONVOY_BOOSTS: False,
    CardCategories.HEROES: False,
    CardCategories.BUILDINGS: False,
    CardCategories.TOWERS: False,
    }


class MyCardsTestCase(unittest.TestCase):
    def test_cards_types(self):
        for category in MY_CARDS:
            for card in MY_CARDS[category]:
                with self.subTest(card=card):
                    if expected_to_be_CardStocks[category]:
                        self.assertIsInstance(card, CardStock, "{} card should stored in a CardStock instance to indicate the number of copies of the card you own".format(card.card.__class__.__name__))
                        card = card.card

                    self.assertIsInstance(card, category.card_base_class, "{} should be a subclass of {}".format(card.__class__.__name__, category.card_base_class.__name__))
                    self.assertIsNot(type(card), category.card_base_class, "{} should be a subclass of {} but not this class itself which is abstract".format(card.__class__.__name__, category.card_base_class.__name__))

    def test_card_numbers_and_levels(self):
        for category in MY_CARDS:
            if expected_to_be_CardStocks[category]:
                for card_stock in MY_CARDS[category]:
                    with self.subTest(card=card_stock.card):
                        self.assertGreaterEqual(card_stock.quantity, 0, "{} quantity should be a positive integer".format(card_stock.card.__class__.__name__))
                        self.assertGreaterEqual(card_stock.card.level, 0,
                                                "{} level should be a positive integer".format(
                                                    card_stock.card.__class__.__name__))
                        # TODO: test more precisely other parameters like: equipments, etc...

    def test_all_categories_exists(self):
        self.assertCountEqual(list(CardCategories), list(MY_CARDS.keys()),
                              msg="CardCategories and MY_CARDS categories mismatch")
        # Test categories for dict declared in this test file
        self.assertCountEqual(list(CardCategories), list(expected_to_be_CardStocks.keys()),
                              msg="Test dictionary <expected_to_be_CardStocks> is not up to date")

    def test_match_to_registered_classes(self):
        # Convert MY_CARD to a CARD_DICTIONARY like dict (containing classes instead of class instances and CardStock)
        my_cards_dictionary = {
            category: set(
                (type(card_stock.card) for card_stock in MY_CARDS[category])
                if expected_to_be_CardStocks[category]
                else (type(card) for card in MY_CARDS[category])
            )
            for category in MY_CARDS
            }

        core_cards_dictionary = {
            category: category.cards
            for category in CardCategories
            }

        self.maxDiff = None  # uncomment to print full diff
        self.assertDictEqual(core_cards_dictionary, my_cards_dictionary,
                             "Cards listed in MY_CARDS mismatch from registered cards")

    # Useless, as test_match_to_registered_classes compares to CARD_DICTIONARY that doesn't contains duplicates.
    # def test_duplicates(self):
    #    pass


if __name__ == '__main__':
    unittest.main()
