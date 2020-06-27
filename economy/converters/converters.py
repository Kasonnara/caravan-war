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
List final converters classes
"""
from typing import Tuple, List, Type

from common.leagues import Rank
from common.rarity import Rarity
from common.resources import ResourcePacket, hero_pair_combinaisons, ResourceQuantity
from common.resources import Resources as R
from common.vip import VIP

from economy.converters.abstract_converter import GainConverter, ConverterModeUIParameter
from economy.gains.abstract_gains import rank_param, Gain, MeasurementPeriod
from economy.gains.daily_rewards import selected_heroes_param, BestTrading, Trading10Km, Trading100Km, Trading1000Km, \
    TransportStationProduction


class Lottery(GainConverter):
    """Convert Lottery tickets to resources rewarded by running the lottery"""
    parameter_dependencies = [rank_param, selected_heroes_param]

    @classmethod
    def get_diff(cls, resource_packet: ResourcePacket, gain_name: str,
                 rank: Rank = Rank.NONE, selected_heroes=hero_pair_combinaisons[0], **kwargs) -> ResourcePacket:
        if resource_packet[R.LotteryTicket] <= 0:
            return ResourcePacket()

        return ResourcePacket(
            R.LotteryTicket(-1),
            selected_heroes[0]((30 * 1 + 5 * 4 + 1 * 7) / 100),
            selected_heroes[1]((30 * 1 + 5 * 4 + 1 * 7) / 100),
            R.CapacityToken((3 * 3 + 2 * 4 + 1 * 5) / 100),
            R.Gem((500 * 7 + 250 * 10) / 100),
            R.Goods((rank.traiding_base * 3 * 7 + rank.traiding_base * 1 * 10) / 100),
            R.Gold((rank.traiding_base * 3 * 7 + rank.traiding_base * 1 * 10) / 100),
            ) * resource_packet[R.LotteryTicket]


lottery_convert_mode_param = ConverterModeUIParameter(Lottery, display_txt="Convert Lottery Tickets")
GainConverter.ALL_CONVERTERS.append(Lottery)  # TODO use a Metaclass for that


class LegendarySoulExchange(GainConverter):
    """Convert legendary souls to unit cards"""

    @classmethod
    def get_diff(cls, resource_packet: ResourcePacket, gain_name: str, **kwargs) -> ResourcePacket:
        if resource_packet[R.LegendarySoul] <= 0:
            return ResourcePacket()
        return ResourcePacket(
            R.LegendarySoul(-1000),
            # TODO, check precisely which epic and legendary card can be obtained (ex no spells; vehicle? modules? all?)
            ResourceQuantity(Rarity.Epic, 2),
            ResourceQuantity(Rarity.Legendary, 1),
            ) * (resource_packet[R.LegendarySoul] / 1000)


legendary_soul_convert_mode_param = ConverterModeUIParameter(LegendarySoulExchange, display_txt="Convert legendary souls")
GainConverter.ALL_CONVERTERS.append(LegendarySoulExchange)


class DefenseLost(GainConverter):
    """Modify trading gain incomes to take lost defenses into account

    To simplify this implementation assume you lost with 100% and your biggest convoys first
    """

    @classmethod
    def get_diff(cls, resource_packet: ResourcePacket, gain_name: str,
                 daily_10km_trading_count: float = None,
                 daily_100km_trading_count: float = 0,
                 daily_1000km_trading_count: float = 0,
                 daily_best_trading_count: float = 0,
                 defense_lost: float = 0,
                 vip: VIP = 1,
                 mesurement_range=MeasurementPeriod.DAY,
                 **kwargs) -> ResourcePacket:
        # Stop for gains that are not convoys
        if gain_name not in [gain.__name__ for gain in [BestTrading, Trading1000Km, Trading100Km, Trading10Km, TransportStationProduction]]:
            return ResourcePacket()

        # Check inputs
        daily_10km_trading_count = daily_10km_trading_count or (Trading10Km.daily_max_count(vip=vip))
        assert daily_10km_trading_count + daily_100km_trading_count + daily_1000km_trading_count + daily_best_trading_count >= defense_lost

        # List targetable convoys and their number of runs sorted by descending order of good quantity
        convoys_counts: List[Tuple[Type[Gain], int]] = [
            (TransportStationProduction, 12),
            (BestTrading, daily_best_trading_count),
            (Trading1000Km, daily_1000km_trading_count),
            (Trading100Km, daily_100km_trading_count),
            (Trading10Km, daily_10km_trading_count),
            ]
        convoys_counts.sort(key=lambda x: x[0].iteration_income(vip=vip, **kwargs)[R.Gold], reverse=True)

        # Count how many convoys of each
        for convoy, count in convoys_counts:
            if gain_name == convoy.__name__:
                # We found the current trading gain
                convoy_lost = min(count, defense_lost)
                return ResourcePacket(
                    R.Gold(convoy.iteration_income(vip=vip, **kwargs)[R.Gold] * -0.5),
                    # TODO include gold reward for defeating bandits
                    R.Trophy(-8),
                    ) * (convoy_lost * mesurement_range.value)
            defense_lost = max(0, defense_lost - count)
        assert False


defense_lost_convert_mode_param = ConverterModeUIParameter(
    DefenseLost,
    value_range=[ConverterModeUIParameter.ConversionMode.IN_PLACE, ConverterModeUIParameter.ConversionMode.EXTERNAL],
    display_txt="Resource stolen display",
    )
GainConverter.ALL_CONVERTERS.append(DefenseLost)


# TODO converter that expand unspecified cards loots into all possible cards or on the contrary that compact any card
#   looted into a reduced set of unspecified cards count
