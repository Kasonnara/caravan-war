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
from collections import namedtuple
from typing import Tuple, List, Union

import dash_core_components as dcc
import dash_html_components as html
import pandas
from plotly.subplots import make_subplots

from common.resources import ResourceQuantity, Resources
import economy.weekly_rewards, economy.daily_purchases, economy.daily_rewards  # Fixme this import exist just to ensure all gains are intialized
from utils.camelcase import camelcase_2_spaced


GraphsUpdates = namedtuple('GraphsUpdates', 'update_func update_ids update_attributes')

# Maybe not the best place to put this
resource_colors = {
    Resources.Gold: "gold",
    Resources.Goods: "#FF5000",
    Resources.Gem: "purple",
    }

# default_colorway = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
# negative_default_colorway = ["#" + "".join(hex(int(int(i, 16)*0.5))[2:] for i in (color[1:3], color[3:5], color[5:7])) for color in default_colorway]
# _next_color_index = -1
# def _get_next_color() -> Tuple[str, str]:
#     global _next_color_index
#     _next_color_index += 1
#     return negative_default_colorway[_next_color_index % len(default_colorway)], default_colorway[_next_color_index % len(default_colorway)]
#
# gains_colors = {camelcase_2_spaced(gain.__name__): _get_next_color() for gain in list(all_gains)}


def pretiffy_values(value: float) -> Union[str, int, float]:
    #  TODO add color
    if value == 0 or value is pandas.NA:
        return ""
    elif -0.1 < value < 0.1:
        return value
    else:
        return round(value, 1)


graphs_to_update: List[GraphsUpdates] = []


class ResourceTable(html.Table):

    EMPTY_TABLE = (html.Thead(html.Tr([])), html.Tbody([]))

    def __init__(self, id: str, className='table-bordered', **kwargs):
        super().__init__(self.EMPTY_TABLE, id, className=className, **kwargs)
        # Register the graph
        graphs_to_update.append(GraphsUpdates(self.figures_updates, id, 'children'))

    @staticmethod
    def figures_updates(data: pandas.DataFrame) -> Tuple[html.Table, html.Tbody]:
        # TODO add color
        # TODO add human readable units (K, M, B, etc)
        all_res_types = data.columns  # TODO sort columns
        prettified_res_types = [camelcase_2_spaced(res_type) for res_type in all_res_types]

        totals: pandas.Series = data.sum()
        totals.name = "totals"
        data_with_total = data.append(totals)

        return (
            html.Thead(html.Tr([html.Th("")] + [
                html.Th(res_types_str)
                for res_types_str in prettified_res_types
                ])),
            html.Tbody([
                html.Tr([html.Td(line_key)] + [
                    html.Td(pretiffy_values(data_with_total.loc[line_key].get(res_types, 0)))
                    for res_types in all_res_types
                    ])
                for line_key in data_with_total.index
                ]),
            )


class ResourceBarPie(dcc.Graph):
    def __init__(self, target_resource: ResourceQuantity.VALID_RESOURCE_TYPE, id=None, **kwargs):
        # Generate the pie plot, with directly with plotly, as dash seems to not work with some parameters
        self.str_target_resource = ResourceQuantity.prettify_type(target_resource)
        id: str = id or self.str_target_resource + "_plot"

        self.fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "pie"}]])
        self.fig.add_bar(
            x=[],
            y=[],
            name=self.str_target_resource,
            texttemplate="%{y: .2s}",
            #textposition='outside',
            row=1, col=1,
            marker_color=resource_colors[target_resource]
            )
        #self.fig.update_layout(xaxis={'categoryorder': 'total descending'})


        #'x': data[plot_label][0],
        #                'y': data[plot_label][1],
        #                'type': 'bar',
        #                'name': plot_label,
        #                'texttemplate': "%{y: .2s}",
        #                'textposition': 'outside',

        self.fig.add_pie(
            hole=0.5,
            sort=False,
            values=[],
            labels=[],
            textinfo='none',
            #marker={'colors': ['green', 'red', 'blue'],
            #        'line': {'color': 'white', 'width': 1}}
            row=1, col=2,
            marker_line_width=2,
            )

        super().__init__(figure=self.fig, id=id, **kwargs)
        # Register the graph
        graphs_to_update.append(GraphsUpdates(self.figures_updates, id, 'figure'))

    def figures_updates(self, data: pandas.DataFrame) -> List:
        # Drop useless value and manually sort the values
        target_data=data[self.str_target_resource].dropna().sort_values(ascending=False)
        self.fig.update_traces(
            values=target_data.abs(),
            labels=target_data.index,
            #pull=[0.07 if x < 0 else 0 for x in target_data],
            #marker_colors = [gains_colors[res_str][target_data[res_str] > 0]
            #                                            for res_str in target_data.index],
            selector=dict(type='pie'),
            marker_line_color=["#00C000" if x > 0 else "#C00000" for x in target_data],
            )
        self.fig.update_traces(
            y=target_data,
            x=target_data.index,
            selector=dict(type='bar'),
            )

        #self.fig.update_layout(color_discrete_sequence=, selector=dict(type='pie'),)
        #print(self.pie.to_plotly_json())
        return self.fig
