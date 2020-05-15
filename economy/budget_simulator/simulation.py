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
from collections import defaultdict
from typing import Type, Dict, Set

from common.resources import ResourcePacket, ResourceQuantity
from economy.gains import BUDGET_SIMULATION_PARAMETERS, GAINS_DICTIONNARY, Gain
# --- keep the following import to ensure that all gains exists ---
import economy.daily_rewards
import economy.weekly_rewards
import economy.daily_purchases
# ---
from utils.camelcase import camelcase_2_spaced

all_parameters = [ui_param
                  for category in BUDGET_SIMULATION_PARAMETERS
                  for ui_param in BUDGET_SIMULATION_PARAMETERS[category]]

all_gains: Set[Type[Gain]] = set.union(*(GAINS_DICTIONNARY[gains_category] for gains_category in GAINS_DICTIONNARY))


def income_dict(*selected_parameters, weekly=True) -> Dict[str, ResourcePacket]:
    assert len(selected_parameters) == len(all_parameters)

    # Generate the parameter value dict
    # TODO add category filtering
    ui_parameter_values = {
        ui_parameter.parameter_name: (bool(raw_value) if ui_parameter.is_bool
                                      else (int(raw_value) if ui_parameter.is_integer
                                      else ui_parameter.value_range[int(raw_value)]))
        for ui_parameter, raw_value in zip(all_parameters, selected_parameters)
        }

    # Recompute all gains
    incomes = {
        camelcase_2_spaced(gain.__name__): gain.weekly_income(**ui_parameter_values) if weekly else gain.daily_income(**ui_parameter_values)
        for gain in all_gains
        }
    return incomes


# TODO I don't really like the mess around the data from here. We have the result from income_dict(), then revert it
#  with this function into another one, and some graphs use even more weird pre-formatting functions. There is clearly
#  an unification and cleaning work to be done here.
#  (maybe with pandas dataframe for example)
def reverse_income_dict(res_dict: Dict[str, ResourcePacket]) -> Dict[str, Dict[str, float]]:
    """
    Invert the resource dict index levels  dict[str_key][res_type] --> dict[res_type][str_key]
    """
    result = defaultdict(dict)
    for str_key in res_dict:
        for res_type in res_dict[str_key]:
            result[camelcase_2_spaced(ResourceQuantity.prettify_type(res_type))][str_key] = res_dict[str_key][res_type]
    return result
