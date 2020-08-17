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
from economy.chests import ALL_CHESTS, RecycleChest

from economy.converters.abstract_converter import GainConverter, ConverterModeUIParameter
from economy.gains.abstract_gains import rank_param, Gain, MeasurementPeriod
from economy.gains.daily_rewards import selected_heroes_param, BestTrading, Trading10Km, Trading100Km, Trading1000Km, \
    TransportStationProduction
from lang.languages import TranslatableString
from spells.common_spell import Spell
from units.base_units import MovableUnit
from utils.ui_parameters import UIParameter


class Lottery(GainConverter):
    """Convert Lottery tickets to resources rewarded by running the lottery"""
    parameter_dependencies = [rank_param, selected_heroes_param]

    @classmethod
    def get_diff(cls, resource_packet: ResourcePacket,
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

    __display_name = TranslatableString("Lottery", french="Lotterie")


lottery_convert_mode_param = ConverterModeUIParameter(Lottery, display_txt="Convert Lottery Tickets")
GainConverter.ALL.append(Lottery)  # TODO use a Metaclass for that


class LegendarySoulExchange(GainConverter):
    """Convert legendary souls to unit cards"""

    @classmethod
    def get_diff(cls, resource_packet: ResourcePacket, **kwargs) -> ResourcePacket:
        if resource_packet[R.LegendarySoul] <= 0:
            return ResourcePacket()
        return ResourcePacket(
            R.LegendarySoul(-1000),
            # TODO, check precisely which epic and legendary card can be obtained (ex no spells; vehicle? modules? all?)
            ResourceQuantity(Rarity.Epic, 2),
            ResourceQuantity(Rarity.Legendary, 1),
            ) * (resource_packet[R.LegendarySoul] / 1000)

    __display_name = TranslatableString("Souls exchanges", french="Échanges d'âmes")


legendary_soul_convert_mode_param = ConverterModeUIParameter(LegendarySoulExchange, display_txt="Convert legendary souls")
GainConverter.ALL.append(LegendarySoulExchange)


class DefenseLost(GainConverter):
    """Modify trading gain incomes to take lost defenses into account

    To simplify this implementation assume you lost with 100% and your biggest convoys first
    """

    @classmethod
    def get_diff(cls, resource_packet: ResourcePacket, gain: Type[Gain] = None,
                 daily_10km_trading_count: float = None,
                 daily_100km_trading_count: float = 0,
                 daily_1000km_trading_count: float = 0,
                 daily_best_trading_count: float = 0,
                 defense_lost: float = 0,
                 vip: VIP = 1,
                 mesurement_range=MeasurementPeriod.DAY,
                 **kwargs) -> ResourcePacket:
        # Stop for gains that are not convoys
        if gain not in [BestTrading, Trading1000Km, Trading100Km, Trading10Km, TransportStationProduction]:
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
            if gain is convoy:
                # We found the current trading gain
                convoy_lost = min(count, defense_lost)
                return ResourcePacket(
                    R.Gold(convoy.iteration_income(vip=vip, **kwargs)[R.Gold] * -0.5),
                    # TODO include gold reward for defeating bandits
                    R.Trophy(-8),
                    ) * (convoy_lost * mesurement_range.value)
            defense_lost = max(0, defense_lost - count)
        assert False

    __display_name = TranslatableString("Attacks received", french="Embuscades subies")


defense_lost_convert_mode_param = ConverterModeUIParameter(
    DefenseLost,
    value_range=[ConverterModeUIParameter.ConversionMode.IN_PLACE, ConverterModeUIParameter.ConversionMode.EXTERNAL],
    display_txt="Resource stolen display",
    )
GainConverter.ALL.append(DefenseLost)


class ChestOpening(GainConverter):

    @classmethod
    def get_diff(cls, resource_packet: ResourcePacket, gain: Type[Gain] = None, rank=Rank.NONE,
                 mesurement_range=MeasurementPeriod.DAY, **kwargs) -> ResourcePacket:
        result = ResourcePacket()
        for chest_type in ALL_CHESTS:
            if resource_packet[chest_type] > 0:
                result = result + (chest_type.average_loot(rank=rank)
                                   + ResourceQuantity(chest_type, -1)) * resource_packet[chest_type]
                # Workaround: to count the reincarnation token that are limited on a daily basis
                #   seems ugly to compute that here, but i couldn't find a clean way to introduce this.
                if chest_type.max_reincarnation_token is not None:
                    result = result + R.ReincarnationToken(min(chest_type.max_reincarnation_token * mesurement_range.value,
                                                               2 * resource_packet[chest_type]))
                # FIXME: BUG the daily limit only apply on current gain, so if multiple gains provide the same chests
                #  the limit will be boggy... currently it isn't a problem, the only chest that can apear multiple times
                #  is the recycle chest which doesn't provide tokens.

        return result


chest_opener_convert_mode_param = ConverterModeUIParameter(
    ChestOpening,
    value_range=[ConverterModeUIParameter.ConversionMode.DISABLED, ConverterModeUIParameter.ConversionMode.IN_PLACE],
    display_txt="Open Chests",
    )
GainConverter.ALL.append(ChestOpening)


class CardUnpacker(GainConverter):
    # Workaround to enable recycling the Rarity types that also includes spells
    # FIXME: it's a rough approximation, the ratio usually depend of the gain so ultimately we should
    #  always do the separation from the beginning. And thus Rarity as types shouldn't mean to include spells.
    SPELL_UNIT_RATIO = 0.1

    @classmethod
    def get_diff(cls, resource_packet: ResourcePacket, gain: Type[Gain] = None, **kwargs) -> ResourcePacket:
        result = ResourcePacket()
        for resource_type, resource_quantity in resource_packet.items():
            # FIXME also include (Card, rarity) or ban it from VALID TYPES
            if resource_type is Rarity.Common or resource_type is Rarity.Rare or resource_type is Rarity.Epic:
                spells_count, card_count = cls.SPELL_UNIT_RATIO * resource_quantity, (1 - cls.SPELL_UNIT_RATIO) * resource_quantity

                # Split between spells and Movable units
                result = result + ResourcePacket(
                    ResourceQuantity(resource_type, -resource_quantity),
                    ResourceQuantity((MovableUnit, resource_type), card_count),
                    ResourceQuantity((Spell, resource_type), spells_count),
                    )
        return result


# DO not have an UIParameter mode yet as it is ALWAYS IN_PLACE mode
GainConverter.ALL.append(CardUnpacker)


recycle_target_type_param = UIParameter(
    'recycle_target_type',
    [RecycleChest.recyclable_types[:1], RecycleChest.recyclable_types],  # Todo add more choices
    display_range=["All Common", "All Common and Rare"],
    display_txt="Cards to recycle",
    )


class Recycle(GainConverter):
    @classmethod
    def get_diff(cls, resource_packet: ResourcePacket, gain: Type[Gain] = None, rank=Rank.NONE,
                 chest_opener_convert_mode_param=ConverterModeUIParameter.ConversionMode.IN_PLACE,
                 recycle_target_type=RecycleChest.recyclable_types, **kwargs) -> ResourcePacket:
        result = ResourcePacket()
        # Iterate over all the resource type of the input ResourcePacket
        for resource_type, resource_quantity in resource_packet.items():
            # Iterate over all the resource type we want to recycle
            for targeted_types, sacrifice_score in recycle_target_type:
                # Check if the resources types are compatible
                if ResourceQuantity.compatible_types(targeted_types, resource_type):
                    chest_quantity = resource_quantity * sacrifice_score / RecycleChest.required_sacrifice
                    #if chest_quantity > 0:
                    if True:  # FIXME, as long as the the negative value bug exist and IN_PLACE mode is forbidden, we also must accept negative values
                        # Check if the chest opener converter is enabled, if yes we must do the conversion because
                        # this converter is processed after the chest opener.
                        if chest_opener_convert_mode_param is ConverterModeUIParameter.ConversionMode.DISABLED:
                            result = result + ResourceQuantity(RecycleChest, chest_quantity)
                        else:
                            result = result + RecycleChest.average_loot(rank=rank) * chest_quantity
                        result = result + ResourceQuantity(resource_type, -resource_quantity)
        return result

    __display_name = TranslatableString("Recycle chests", french="Coffres de recyclage")


recycle_convert_mode_param = ConverterModeUIParameter(
    Recycle,
    value_range=[ConverterModeUIParameter.ConversionMode.DISABLED, ConverterModeUIParameter.ConversionMode.EXTERNAL],
    # FIXME: WORKAROUND, converters currently badly behave with negative values in IN_PLACE mode
    #  (see AbstractConverter.apply_all for more details) so as long as this bug exists IN_PLACE mode is forbidden.
    display_txt="Recycle cards",
    )
GainConverter.ALL.append(Recycle)


# TODO converter that expand unspecified cards loots into all possible cards or on the contrary that compact any card
#   looted into a reduced set of unspecified cards count
