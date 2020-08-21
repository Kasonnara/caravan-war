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
List purchases possible on a daily basis
"""
from common.leagues import Rank
from common.rarity import Rarity
from common.resources import ResourcePacket, ResourceQuantity
from common.resources import Resources as R
from common.vip import VIP

from economy.gains.abstract_gains import Gain, vip_param

# TODO: daily shop
from units.bandits import Bandit
from units.equipments import Equipment
from utils.ui_parameters import UIParameter


def update_craft_number_range(vip: VIP):
    return (
        [None] + list(range(vip.equipment_building_limit + 1)),
        ["Auto (Max)"] + [str(x) for x in range(vip.equipment_building_limit + 1)],
    )


equipment_craft_number_param = UIParameter(
    'equipment_craft_number',
    update_craft_number_range(VIP.lvl0)[0],
    display_range=update_craft_number_range(VIP.lvl0)[1],
    display_txt="Equipment forging",
    update_callback=update_craft_number_range,
    dependencies=[vip_param],
    help_txt="Select the average number of equipment you forge per day.",
    )


class EquipmentCrafting(Gain):
    common_card_costs = [-3, -3, -4, -5, -6] + [-6]*10
    common_spell_costs = [-1, -1, -2, -2, -3] + [-3]*10  # Fixme not used
    rare_card_costs = [-1, -1, -2, -2, -3] + [-3]*10
    rare_spell_costs = [-1, -1, -1, -2, -2] + [-2]*10  # Fixme not used
    equipment_gold_costs = [-0.4, -0.8, -1.2, -1.6, -2] + [-2]*10
    # TODO add crafting limit reset with gems

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, vip: VIP = 1, equipment_crafting_index=0, **kwargs) -> ResourcePacket:
        if equipment_crafting_index >= vip.equipment_building_limit:
            return ResourcePacket()
        return ResourcePacket(
            R.Gold(sum(cls.equipment_gold_costs[equipment_crafting_index] * rank.traiding_base)),
            ResourceQuantity(Equipment, 1),
            ResourceQuantity(Rarity.Rare, cls.rare_card_costs[equipment_crafting_index]),
            ResourceQuantity(Rarity.Common, cls.common_card_costs[equipment_crafting_index]),
            # Fixme: card costs are different for spells than other cards, and doesn't include vehicles
            )

    @classmethod
    def daily_income(cls, rank: Rank = Rank.NONE, vip: VIP = 1, equipment_craft_number: int = None,
                     **kwargs) -> ResourcePacket:
        if equipment_craft_number is None:
            equipment_craft_number = vip.equipment_building_limit
        else:
            equipment_craft_number = min(equipment_craft_number, vip.equipment_building_limit)

        return ResourcePacket(
            R.Gold(sum(cls.equipment_gold_costs[:equipment_craft_number] * rank.traiding_base)),
            ResourceQuantity(Equipment, equipment_craft_number),
            ResourceQuantity(Rarity.Rare, -5 * equipment_craft_number),  # Fixme, check average values
            ResourceQuantity(Rarity.Common, -5 * equipment_craft_number),  # Fixme, check average values
            )

# TODO: recycle chest

# TODO: premium chest/offers
