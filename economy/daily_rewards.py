#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This is a personal project to understand and improve my knowledge/tactics in the game Caravan War.
# Copyright (C) 2019  Kasonnara <kasonnara@laposte.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
List gains that obtainable on a daily basis
"""
import itertools

from common.leagues import Rank
from common.resources import ResourcePacket, hero_souls
from common.resources import Resources as R
from common.vip import VIP
from economy.gains import Gain, GAINS_DICTIONARY, rank_param, vip_param, BUDGET_SIMULATION_PARAMETERS, Days
from utils.selectable_parameters import UIParameter


reset_max_count_param = UIParameter(
    'reset_max_count',
    range(8),
    display_range=[str(x) for x in range(8)],
    display_txt="Trading limit resets",
    default_value=3,
    )
BUDGET_SIMULATION_PARAMETERS['General'].append(reset_max_count_param)


class Trading(Gain):
    parameter_dependencies = [rank_param, vip_param, reset_max_count_param]
    duration: int = None
    traiding_limit = None
    goods_cost_multiplier: int = None
    gold_reward_multiplier: float = None

    @classmethod
    def goods_cost(cls, rank: Rank) -> int:
        return - rank.traiding_base * cls.goods_cost_multiplier

    @classmethod
    def gold_reward(cls, rank: Rank, vip: VIP) -> int:
        return rank.traiding_base * cls.gold_reward_multiplier * vip.traiding_profit

    @classmethod
    def daily_max_count(cls, vip: VIP, reset_max_count: float = 0) -> float:
        assert reset_max_count >= 0
        return min(
            24 / (cls.duration * vip.traiding_time),       # Max number of traiding in 24 hours with infinite resets
            cls.traiding_limit * (1 + reset_max_count),    # Max number of traiding according to resets
            )

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, vip: VIP = 1, **kwargs) -> ResourcePacket:
        return ResourcePacket(cls.goods_cost(rank), cls.gold_reward(rank, vip))

    @classmethod
    def daily_income(cls, rank: Rank = Rank.NONE, vip: VIP = 1,
                     daily_trading_count: float = None, reset_max_count: float = 0, **kwargs) -> ResourcePacket:
        max_trading = cls.daily_max_count(vip, reset_max_count)
        assert daily_trading_count is None or daily_trading_count < max_trading
        return (
            cls.iteration_income(rank=rank, vip=vip, **kwargs)
            * (max_trading if daily_trading_count is None else daily_trading_count)
            )


class Trading10Km(Trading):
    duration = 0.5
    traiding_limit = 100
    goods_cost_multiplier = 1
    gold_reward_multiplier = 1


class Trading100Km(Trading):
    duration = 1
    traiding_limit = 3
    goods_cost_multiplier = 2
    gold_reward_multiplier = 2.6


class Trading1000Km(Trading):
    duration = 2
    traiding_limit = 2
    goods_cost_multiplier = 3
    gold_reward_multiplier = 4.8


class BestTrading(Trading):
    duration = 4
    traiding_limit = 1
    goods_cost_multiplier = 4
    gold_reward_multiplier = 8


_possible_hero_combinaisons = list(itertools.combinations(hero_souls, 2))
"""List all the possible unordered combinations of 2 hero souls"""

# Declare an additional UI parameter for the lottery gains
selected_heroes_param = UIParameter(
    'selected_heroes',
    _possible_hero_combinaisons,
    display_range=["{}-{}".format(h1.name[:-4], h2.name[:-4]) for h1, h2 in _possible_hero_combinaisons],
    display_txt="Lottery heroes"
    )
BUDGET_SIMULATION_PARAMETERS["General"].append(selected_heroes_param)


class Lottery(Gain):
    parameter_dependencies = [rank_param, selected_heroes_param]

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, selected_heroes=_possible_hero_combinaisons[0], **kwargs) -> ResourcePacket:
        return ResourcePacket(
            selected_heroes[0]((30 * 1 + 5 * 4 + 1 * 7) / 100),
            selected_heroes[1]((30 * 1 + 5 * 4 + 1 * 7) / 100),
            R.CapacityToken((3 * 3 + 2 * 4 + 1 * 5) / 100),
            R.Gem((500 * 7 + 250 * 10) / 100),
            R.Goods((rank.traiding_base * 3 * 7 + rank.traiding_base * 1 * 10) / 100),
            R.Gold((rank.traiding_base * 3 * 7 + rank.traiding_base * 1 * 10) / 100),
            )

    @classmethod
    def convert_tickets(cls, ticket_number: int, rank: Rank, selected_heroes=(R.DalvirSoul, R.ZoraSoul), **kwargs) -> ResourcePacket:
        return cls.iteration_income(rank, selected_heroes=selected_heroes, **kwargs) * ticket_number

    @classmethod
    def daily_income(cls, rank: Rank, *args, selected_heroes=(R.DalvirSoul, R.ZoraSoul), **kwargs) -> ResourcePacket:
        return cls.convert_tickets(3, rank, selected_heroes=selected_heroes, **kwargs)

# TODO daily quests


GAINS_DICTIONARY['trading'] = {Trading10Km, Trading100Km, Trading1000Km, BestTrading}

GAINS_DICTIONARY['daily'] = GAINS_DICTIONARY['trading'].union({Lottery})
