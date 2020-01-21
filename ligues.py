from enum import Enum


class Ligue(Enum):
    Dunkey1 = (0, 2000, 500)
    Dunkey2 = (1, 2600, 700)
    Dunkey3 = (2, 3200, 800)
    Wolf1 = (3, 4000, 1000)
    Wolf2 = (4, 4900, 1200)
    Wolf3 = (5, 5800, 1500)
    Horse1 = (6, 7000, 1800)
    Horse2 = (7, 8500, 2100)
    Horse3 = (8, 10000, 2500)
    Camel1 = (9, 12000, 3000)
    Camel2 = (10, 14400, 3600)
    Camel3 = (11, 16800, 4200)
    Buffalo1 = (12, 20000, 5000)
    Buffalo2 = (13, 24200, 6100)
    Buffalo3 = (14, 28400, 7100)
    Rinoceros1 = (15, 34000, 8500)
    Rinoceros2 = (16, 41200, 11900)
    Rinoceros3 = (17, 48400, 16000)
    Elephant1 = (18, 58000, 22000)
    Elephant2 = (19, 70600, 31100)
    Elephant3 = (20, 83200,)
    Dragon1 = (21, 100000,)
    Dragon2 = (22, 125000,)
    Dragon3 = (23, 160000,)
    RedDragon1 = (24, 100000,)
    RedDragon2 = (25, 200000, )
    RedDragon3 = (26, 320000, )
    BlackDragon1 = (27, 400000, )
    BlackDragon2 = (28, 500000, )
    BlackDragon3 = (29, 630000, )
    Phenix1 = (30, 1000000, )
    Phenix2 = (31, 1600000, )
    Phenix3 = (32, 2550000, )
    IcePhenix1 = (33, 4000000, )
    IcePhenix2 = (34, 6400000, )
    IcePhenix3 = (35, 10000000, )
    Kraken1 = (36, 15000000, )
    Kraken2 = (37, 23000000, )
    Kraken3 = (38, 34000000, )
    RedKraken1 = (39, 51000000, )
    RedKraken2 = (40, 77000000, )
    RedKraken3 = (41, 116000000, )
    Behemote1 = (42, 160000000, )
    Behemote2 = (43, 200000000, )
    Behemote3 = (44, 250000000, )

    def __init__(self, rank: int, exchange_base: int, raid_goods_bonus: int = None):
        self.rank = rank
        self.ex10km_goods_cost, self.ex10km_gold_reward = exchange_base, exchange_base
        self.ex100km_goods_cost, self.ex100km_gold_reward = exchange_base * 2, exchange_base * 2.6
        self.ex1000km_goods_cost, self.ex1000km_gold_reward = exchange_base * 3, exchange_base * 4.8
        self.bestex_goods_cost, self.bestex_gold_reward = exchange_base * 4, exchange_base * 8
        self.raid_goods_bonus = raid_goods_bonus or (exchange_base / 2)

