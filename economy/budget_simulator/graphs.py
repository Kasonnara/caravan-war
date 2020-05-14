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
from typing import Dict, Tuple, Type

import dash_core_components as dcc
import dash_html_components as html

from common.resources import ResourcePacket, ResourceQuantity
from economy.gains import Gain
from utils.camelcase import camelcase_2_spaced

Graph = namedtuple('Graph', 'build_func update_func update_id update_attribute')


def pretiffy_values(value: float) -> str:
    #  TODO add color
    if value == 0:
        return ""
    elif -0.1 < value < 0.1:
        return value
    else:
        return round(value, 1)


def resourcepackets_to_table(resource_packets: Dict[str, ResourcePacket]) -> Tuple[html.Table, html.Tbody]:
    """
    Represent resource packets in a table by, generate the children attribute of a dash_html_components.Table object

    :param resource_packets: A dictionary of ResourcePacket to display in a table
    :return: return a tuple to put as `children` attribute of an dash_html_components.Table object
    """
    # TODO add color
    # TODO add human readable units (K, M, B, etc)
    all_res_types = ResourcePacket.get_all_resource_types(resource_packets.values(), sort=True)
    prettified_res_types = [camelcase_2_spaced(ResourceQuantity.prettify_type(res_type)) for res_type in all_res_types]

    return (
        html.Thead(html.Tr([html.Th("")] + [
            html.Th(res_types_str)
            for res_types_str in prettified_res_types
            ])),
        html.Tbody([
            html.Tr([html.Td(line_key)] + [
                html.Td(pretiffy_values(resource_packets[line_key].get(res_types, 0)))
                for res_types in all_res_types
                ])
            for line_key in resource_packets
            ]),
        )


global_table_graph = Graph(
    lambda: html.Table(resourcepackets_to_table({"Total": ResourcePacket()}),
                       id='global_resource_table',
                       #style={'border-collapse': 'collapse'},
                       className='table-bordered',
                       ),
    lambda res_dict, reverse_resource_dict: resourcepackets_to_table(res_dict),
    'global_resource_table',
    'children',
    )


def value_dict_2_bar_plot(data: Dict[str, Dict[str, float]]):
    return {
        'data': [
            {
                'x': [resource_type
                      for resource_type in data[plot_label].keys()],
                'y': tuple(data[plot_label].values()),
                'type': 'bar',
                'name': plot_label,
                }
            for plot_label in data
            ]}


gold_goods_bar_plot = Graph(
    lambda: dcc.Graph(
        figure={'data': []},
        id='gold_goods_bar_plot',
        style={'height': '100vh'}
        ),
    lambda res_dict, reverse_resource_dict: print(tuple(reverse_resource_dict.keys())) or value_dict_2_bar_plot(
        {'Gold': reverse_resource_dict['Gold'], 'Goods': reverse_resource_dict['Goods']}),
    'gold_goods_bar_plot',
    'figure',
    )

all_graphs = [global_table_graph, gold_goods_bar_plot]
