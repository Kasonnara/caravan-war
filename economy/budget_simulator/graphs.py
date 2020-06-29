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
Definition of all the graphs functions present in the application and their callback functions
"""
import os
from collections import namedtuple
from typing import List, Union, Dict, Type

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import dash
from plotly.subplots import make_subplots

from common.resources import ResourceQuantity, Resources, ResourcePacket
from economy.budget_simulator.simulation import RESOURCE_SORTING_MAP
from economy.converters.abstract_converter import GainConverter
from economy.gains import Gain
from utils.prettifying import camelcase_2_spaced, human_readable

GraphsUpdates = namedtuple('GraphsUpdates', 'update_func component_id target_attribute')

# Maybe not the best place to put this
resource_colors = {
    Resources.Gold: "gold",
    Resources.Goods: "#FF5000",
    Resources.Gem: "purple",
    Resources.Dust: "green",
    }

# (Init later when an dash.Dash instance exists)
resource_icons: Dict[Resources, List[html.Img]] = None
"""Map the resource to the corresponding html.Img tag for the icon of that resource"""

# default_colorway = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
# negative_default_colorway = ["#" + "".join(hex(int(int(i, 16)*0.5))[2:] for i in (color[1:3], color[3:5], color[5:7])) for color in default_colorway]
# _next_color_index = -1
# def _get_next_color() -> Tuple[str, str]:
#     global _next_color_index
#     _next_color_index += 1
#     return negative_default_colorway[_next_color_index % len(default_colorway)], default_colorway[_next_color_index % len(default_colorway)]
#
# gains_colors = {camelcase_2_spaced(gain.__name__): _get_next_color() for gain in list(all_gains)}


graphs_to_update: List[GraphsUpdates] = []


class ResourceTable(dbc.Table):

    EMPTY_TABLE = (html.Thead(html.Tr([])), html.Tbody([]))

    def __init__(self, app: dash.Dash, id: str, bordered=True, striped=False, hover=True, responsive=True, **kwargs):
        super().__init__(self.EMPTY_TABLE, id, bordered=bordered, striped=striped, hover=hover, responsive=responsive, **kwargs)
        # Register the graph
        graphs_to_update.append(GraphsUpdates(self.figures_updates, id, 'children'))

        # Init resource_icons
        global resource_icons
        resource_icons = {
            resource: [html.Img(
                src=app.get_asset_url(os.path.join("resources", "{}.png".format(resource.name))),
                height="20px",  # FIXME do not hard-code values like that
                )]
            for resource in Resources
            if os.path.isfile(os.path.join("..", "..", "assets", "resources", "{}.png".format(resource.name)))  # FIXME there is probably a better solution
            }

    @staticmethod
    def figures_updates(incomes: Dict[str, Dict[Union[Type[Gain], Type[GainConverter]], ResourcePacket]]) -> List[Union[html.Table, html.Tbody]]:
        # Compute total
        total = ResourcePacket()
        for gain_category in incomes:
            for key in incomes[gain_category]:
                # TODO there should be a function in ResourcePacket for that
                total = total + incomes[gain_category][key]

        incomes = incomes.copy()
        incomes['totals'] = {None: total}

        all_res_types = [res_type for res_type in RESOURCE_SORTING_MAP.keys() if res_type in total.keys()]
        """List all resource types present in incomes, sorted according to the RESOURCE_SORTING_MAP"""
        # O(n²) : There probably a better way to proceed

        def pretty_Td(value):
            """Generate a dash html Td while prettifying its content"""
            pretty_value = human_readable(value, erase_under=10**-2)
            return html.Td(
                pretty_value,
                className='text-danger' if len(pretty_value) > 0 and pretty_value[0] == '-' else 'text-success',
                )

        columns_names = [html.Th(resource_icons.get(res_type, [])  # Add the resource icon if it exists
                                 + [html.Div(camelcase_2_spaced(ResourceQuantity.prettify_type(res_type)))],
                                 className='text-center',)
                         for res_type in all_res_types]

        return [
            Thead_or_Tbody
            for k, category in enumerate(incomes)
            for Thead_or_Tbody in [
                html.Thead(html.Tr([html.Th(category.upper())]
                                   + (columns_names if k == 0 or category == 'totals' else ([html.Th()] * len(columns_names))),
                                   className='thead-light')),
                html.Tbody([
                    html.Tr(
                        [html.Td(camelcase_2_spaced(gain.__name__, unbreakable_spaces=True)
                                 if gain is not None else ''  # Special case for the total line which doesn't have gain
                                 )]
                        + [pretty_Td(incomes[category][gain][res_types])
                           for res_types in all_res_types]
                        )
                    for gain in incomes[category]
                    ]),
                ]
            ]


class ResourceBarPie(dcc.Graph):
    def __init__(self, target_resource: ResourceQuantity.VALID_RESOURCE_TYPE, id=None, **kwargs):
        # Generate the pie plot, with directly with plotly, as dash seems to not work with some parameters
        self.target_resource = target_resource
        str_target_resource = ResourceQuantity.prettify_type(self.target_resource)
        id: str = id or str_target_resource + "_plot"

        self.fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "pie"}]])
        self.fig.add_bar(
            x=[],
            y=[],
            name=str_target_resource,
            texttemplate="%{y: .2s}",
            row=1, col=1,
            marker_color=resource_colors[target_resource]
            )

        self.fig.add_pie(
            hole=0.5,
            sort=False,
            values=[],
            labels=[],
            textinfo='none',
            row=1, col=2,
            marker_line_width=2,
            )

        super().__init__(figure=self.fig, id=id, **kwargs)
        # Register the graph
        graphs_to_update.append(GraphsUpdates(self.figures_updates, id, 'figure'))

    def figures_updates(self, incomes: Dict[str, Dict[Union[Type[Gain], Type[GainConverter]], ResourcePacket]]) -> List:
        # Extract incomes for the target resource, erase too small values, prettify gains names and sort them
        target_incomes_label, target_incomes_values = zip(
            *sorted(
                [(camelcase_2_spaced(gain.__name__, unbreakable_spaces=True),  # Prettify gains names
                  incomes[category][gain][self.target_resource])
                    for category in incomes
                    for gain in incomes[category]
                    if abs(incomes[category][gain][self.target_resource]) >= 10**-2  # Erase small values
                 ],
                key=lambda x: x[1],
                reverse=True,
                )
            )

        self.fig.update_traces(
            values=[abs(x) for x in target_incomes_values],  # Pie chart doesn't like negative values
            labels=target_incomes_label,
            selector=dict(type='pie'),
            marker_line_width=[0 if x > 0 else 4 for x in target_incomes_values],
            marker_line_color=["#00C000" if x > 0 else "#C00000" for x in target_incomes_values],
            )
        self.fig.update_traces(
            y=target_incomes_values,
            x=target_incomes_label,
            selector=dict(type='bar'),
            )

        return self.fig
