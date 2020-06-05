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

import pandas

from common.resources import ResourcePacket, ResourceQuantity
from economy.gains import BUDGET_SIMULATION_PARAMETERS, GAINS_DICTIONARY, Gain
# --- keep the following import to ensure that all gains exists ---
import economy.daily_rewards
import economy.weekly_rewards
import economy.daily_purchases
# ---
from utils.camelcase import camelcase_2_spaced

all_parameters = [ui_param
                  for category in BUDGET_SIMULATION_PARAMETERS
                  for ui_param in BUDGET_SIMULATION_PARAMETERS[category]]

all_gains: Set[Type[Gain]] = set.union(*(GAINS_DICTIONARY[gains_category] for gains_category in GAINS_DICTIONARY))


def update_income(*selected_parameters, weekly=True) -> pandas.DataFrame:
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
    incomes = pandas.DataFrame(
        data=[
            gain.weekly_income(**ui_parameter_values).to_pandas() if weekly
                else gain.daily_income(**ui_parameter_values).to_pandas()
            for gain in all_gains
            ],
        index=[camelcase_2_spaced(gain.__name__) for gain in all_gains],
        )
    return incomes
