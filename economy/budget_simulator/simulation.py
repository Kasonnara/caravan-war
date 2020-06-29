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
Manage the parameters of the simulator
"""
from typing import Type, Dict, Set, Union

from common.card_categories import CardCategories
from common.rarity import Rarity
from common.resources import Resources, ResourcePacket
from economy.budget_simulator.bs_ui_parameters import BUDGET_SIMULATION_PARAMETERS
from economy.converters.abstract_converter import GainConverter
from economy.gains import GAINS_DICTIONARY
from economy.gains.abstract_gains import Gain

all_parameters = [ui_param
                  for category in BUDGET_SIMULATION_PARAMETERS
                  for ui_param in BUDGET_SIMULATION_PARAMETERS[category]]


def update_income(selected_parameters) -> Dict[str, Dict[Union[Type[Gain], Type['GainConverter']], ResourcePacket]]:
    assert len(selected_parameters) == len(all_parameters)

    # Generate the parameter value dict
    # TODO add category filtering
    ui_parameter_values = {
        ui_parameter.parameter_name: (bool(raw_value) if ui_parameter.value_range is bool
                                      else (int(raw_value) if ui_parameter.value_range is int
                                      else ui_parameter.value_range[int(raw_value)]))
        for ui_parameter, raw_value in zip(all_parameters, selected_parameters)
        }
    # Recompute all gains
    incomes = {
        gain_category: {
            gain: gain.average_income(**ui_parameter_values)
            for gain in GAINS_DICTIONARY[gain_category]
            }
        for gain_category in GAINS_DICTIONARY
        }
    # Apply converters
    GainConverter.apply_all(incomes, ui_parameter_values)

    return incomes

RESOURCE_SORTING_MAP = {
    resource_type: order
    for order, resource_type in enumerate(
        [native_resource_type for native_resource_type in Resources]    # Prioritize native resources in the order of the enum
        + [rarity_type for rarity_type in Rarity]                       # then unspecified rarity
        + [(card_category.card_base_class, rarity_type) for rarity_type in Rarity for card_category in CardCategories]  # then (category,rarity) tuples
        + [card_category.card_base_class for card_category in CardCategories]  # Then unspecified card categories
        + [specific_card for card_category in CardCategories for specific_card in card_category]  # And finally very targeted card type
        )
    }
