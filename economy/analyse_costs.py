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
The purpose of this script is to plot cost evolution of upgradable object (unit, buildings, etc.)
to manually identify patterns andrelations.

The main objective is to find a relation that describe cost evolution of everything

Assumptions tested:
- [X] There is a relation between building/unit costs and HQ cost. [results: plots are similar but not identical
until level 11 where cost grow factor stabilize]
- [X] There is a relation between building/unit upgrade cost and ligue exchange gains. [results: No]
"""

from collections import defaultdict

from buildings.buildings import Mill, Laboratory, TransportStation
from common.cards import Upgradable
from common.resources import resourcepackets
from units.guardians import Sparte
from units.modules import Laser

from buildings.headquarters import HQ
from common.ligues import Ligue
from units.towers import HeavySniper, Stormspire

import matplotlib.pyplot as plt


PLOT_SIDE_BY_SIDE = False
PLOT_ERROR_BARS = True
PLOT_LIGUE = True

PLOT_RAW_VALUES = False
PLOT_RELATIVE_VALUES = True
PLOT_FIRST_RELATIVE_VALUE = False
PLOT_LIGUE_VALUE = False


def round_error(cost_value: int):
    str_value = str(cost_value)
    return 0.5 * 10 ** (len(str_value) - len(str_value.rstrip('0')))

costs_dict = defaultdict(lambda: defaultdict(list))
cost_error_dict = defaultdict(lambda: defaultdict(list))
index_dict = defaultdict(lambda: defaultdict(list))
relative_costs_dict = {}
relative_index_dict = {}
relative_error_dict = {}
first_relative_costs_dict = {}

resource_types = set()


LIGUE_LEVEL_RATIO = 1
class FakeUpgradableLigue(Upgradable):
    upgrade_costs = resourcepackets(
        *tuple((ligue.ex10km_goods_cost, ligue.ex10km_gold_reward)
               for k, ligue in enumerate(Ligue)
               if k % LIGUE_LEVEL_RATIO == 0)
        )


# Process data and store all results in some big nested dicts
for upgradable in (
        HQ,
        Stormspire,
        HeavySniper,
        Mill,
        Laboratory,
        TransportStation,
        Sparte,
        # Uncomment the following line to test correlation with ligues (Results: Doesn't seem to be correlated)
        #FakeUpgradableLigue,
        ):
    # Extract upgrade costs and process some derived measures
    for level, upgrade_cost_packet in enumerate(upgradable.upgrade_costs):
        if upgrade_cost_packet is not None:  # check for missing data (possible in development)
            for resource_type in upgrade_cost_packet:
                index_dict[upgradable][resource_type].append(level)
                costs_dict[upgradable][resource_type].append(-upgrade_cost_packet[resource_type])
                resource_types.add(resource_type)
                # - process an round error estimation
                cost_error_dict[upgradable][resource_type].append(round_error(upgrade_cost_packet[resource_type]))

    # - cost of each level relatively to the previous level
    relative_costs_dict[upgradable] = {
        resource_type: [(c2 / c1 if c1 != 0 else 0)
                        for c1, c2, i1, i2 in zip(costs_dict[upgradable][resource_type][:-1],
                                                  costs_dict[upgradable][resource_type][1:],
                                                  index_dict[upgradable][resource_type][:-1],
                                                  index_dict[upgradable][resource_type][1:],
                                                  )
                        if i2 - i1 == 1  # Ensure there is not gap
                        ]
        for resource_type in resource_types
        }
    relative_index_dict[upgradable] = {
        resource_type: [i2 for i1, i2 in zip(index_dict[upgradable][resource_type][:-1],
                                             index_dict[upgradable][resource_type][1:],)
                        if i2 - i1 == 1  # Ensure there is not gap
                        ]
        for resource_type in resource_types
        }
    relative_error_dict[upgradable] = {
        resource_type: [max(abs(c2/c1 - (c2 + e2) / (c1 - e1) if c1 != 0 and (c1 - e1) != 0 else 0),
                            abs(c2/c1 - (c2 - e2) / (c1 + e1) if c1 != 0 and (c1 + e1) != 0 else 0),
                            )
                        for c1, c2, e1, e2, i1, i2 in zip(costs_dict[upgradable][resource_type][:-1],
                                                          costs_dict[upgradable][resource_type][1:],
                                                          cost_error_dict[upgradable][resource_type][:-1],
                                                          cost_error_dict[upgradable][resource_type][1:],
                                                          index_dict[upgradable][resource_type][:-1],
                                                          index_dict[upgradable][resource_type][1:],
                                                          )
                        if i2 - i1 == 1  # Ensure there is not gap
                        ]
        for resource_type in resource_types
        }

    # - cost of each level relatively to the upgrade from level 1 to 2
    first_relative_costs_dict[upgradable] = {
        resource_type: [(c / costs_dict[upgradable][resource_type][1]) for c in costs_dict[upgradable][resource_type]]
        for resource_type in resource_types
        if any(costs_dict[upgradable][resource_type][1:])  # ignore resources that are always at zero (or at zero for all values except the first like the mill)
        }


# Display results
resource_number = len(index_dict.keys())
for data, indexes, enable, title, y_legend in [
        (costs_dict, index_dict, PLOT_RAW_VALUES, "Raw {} cost", "Raw upgrade costs of {}"),
        (relative_costs_dict, relative_index_dict, PLOT_RELATIVE_VALUES, "Relative {} cost", "upgrade {} costs of each level relatively to the previous level"),
        (first_relative_costs_dict,  index_dict, PLOT_FIRST_RELATIVE_VALUE, "first relative {} cost", "upgrade {} costs of each level relatively to the upgrade from level level 1 to 2"),
        ]:
    if enable:
        # Init plot surfaces
        plot_surfaces = {}
        if PLOT_SIDE_BY_SIDE:
            # Create one figure with many subplots, one per resource
            fig = plt.figure()
            for resource_type in resource_types:
                plot_surfaces[resource_type] = fig.add_subplot(
                    resource_number, 1, resource_number, title=title.format(resource_type.name))
        else:
            # Create many figures, one per resource
            for resource_type in resource_types:
                fig = plt.figure()
                plot_surfaces[resource_type] = fig.add_subplot(1, 1, 1, title=title.format(resource_type.name))

        # Make plots
        for card in data:
            for resource_type in data[card]:
                if not PLOT_ERROR_BARS:
                    plot_surfaces[resource_type].plot(indexes[card][resource_type], data[card][resource_type], "+-", label=card.__name__)
                else:
                    plot_surfaces[resource_type].errorbar(indexes[card][resource_type], data[card][resource_type], yerr=relative_error_dict[card][resource_type], label=card.__name__, )

        # Activate legends
        for resource_type in plot_surfaces:
            plot_surfaces[resource_type].legend()

plt.show()


