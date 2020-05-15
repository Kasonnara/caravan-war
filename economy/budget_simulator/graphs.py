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
from typing import Dict, Tuple, Type, List, Optional

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from common.resources import ResourcePacket, ResourceQuantity, Resources
from economy.gains import Gain, GAINS_DICTIONNARY
from utils.camelcase import camelcase_2_spaced

Graph = namedtuple('Graph', 'build_func update_func update_id update_attribute')

# Maybe not the best place to put this
resource_colors = {
    Resources.Gold: "gold",
    Resources.Goods: "#FF5000",
    Resources.Gem: "purple",
    }

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
            html.Tr([html.Td(line_key, )] + [
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


def extract_one_resource_and_sort(reverse_resource_dict: Dict[str, Dict[str, float]], target_resource_name: str,
                                  ) -> Dict[str, Tuple[List[str], List[float]]]:
    return {target_resource_name: tuple(zip(*sorted(zip(reverse_resource_dict[target_resource_name].keys(),
                                                        reverse_resource_dict[target_resource_name].values(),
                                                        ), key=lambda x: x[1], reverse=True)))}


def value_dict_2_bar_plot(data: Dict[str, Tuple[List[str], List[float]]], colors: Dict[str, str]= {}) -> Dict:
    """
    Generate the dict data to inject into dcc.graph object to generate a bar plot
    :param data: a dictionay of tuple. Each entry in this dict represent one plot on the graph. The key with be the
        legend label of this plot, while the tuple contains respectively the x labels and the y values and optionally
        an HTML color code.
    """
    graph_content = {
        'data': [
            {
                'x': data[plot_label][0],
                'y': data[plot_label][1],
                'type': 'bar',
                'name': plot_label,
                'texttemplate': "%{y: .2s}",
                'textposition': 'outside',
                }
            for plot_label in data
            ],
        'layout': {
            # FIXME implement default color in case it isn't in the dict
            'colorway': [colors.get(bar_label) for bar_label in data],
            }}
    return graph_content


def value_dict_2_pie_plot(data: Tuple[List[str], List[float]], colors: Dict[str, str]= {}) -> Dict:
    """
    Generate the dict data to inject into dcc.graph object to generate a bar plot
    :param data: a dictionay of tuple. Each entry in this dict represent one plot on the graph. The key with be the
        legend label of this plot, while the tuple contains respectively the x labels and the y values and optionally
        an HTML color code.
    """
    graph_content = {
        'data': [{
            'labels': data[0],
            'values': data[1],
            'textinfo ': "none",
            'hole ': .5,
            'type': 'pie',
            'textposition': 'outside',
            }],
        #'layout': {
        #    # FIXME implement default color in case it it's in the dict
        #    'colorway': [colors.get(pie_label) for pie_label in data[0]],
        #    },
        }
    return graph_content


def build_plot(id: str, animate=False):
    return dcc.Graph(
        figure={'data': []},
        id='{}_plot'.format(id),
        style={'height': '100vh'},
        animate=animate,
        )


gold_bar_plot = Graph(
    lambda: build_plot("gold_bar"),
    lambda res_dict, reverse_resource_dict: value_dict_2_bar_plot(
        extract_one_resource_and_sort(reverse_resource_dict, "Gold"), colors=resource_colors),
    'gold_bar_plot',
    'figure',
    )

gold_pie_plot = Graph(
    lambda: build_plot("gold_pie", animate=True),
    lambda res_dict, reverse_resource_dict: value_dict_2_pie_plot(
        extract_one_resource_and_sort(reverse_resource_dict, "Gold")["Gold"], colors=resource_colors),
    'gold_pie_plot',
    'figure',
    )

goods_bar_plot = Graph(
    lambda: build_plot("goods_bar"),
    lambda res_dict, reverse_resource_dict: value_dict_2_bar_plot(
        extract_one_resource_and_sort(reverse_resource_dict, "Goods"), colors=resource_colors),
    'goods_bar_plot',
    'figure',
    )

goods_pie_plot = Graph(
    lambda: build_plot("goods_pie", animate=True),
    lambda res_dict, reverse_resource_dict: value_dict_2_pie_plot(
        extract_one_resource_and_sort(reverse_resource_dict, "Goods")["Goods"], colors=resource_colors),
    'goods_pie_plot',
    'figure',
    )

gems_bar_plot = Graph(
    lambda: build_plot("gems_bar"),
    lambda res_dict, reverse_resource_dict: value_dict_2_bar_plot(
        extract_one_resource_and_sort(reverse_resource_dict, "Gem"), colors=resource_colors),
    'gems_bar_plot',
    'figure',
    )

gems_pie_plot = Graph(
    lambda: build_plot("gems_pie", animate=True),
    lambda res_dict, reverse_resource_dict: value_dict_2_pie_plot(
        extract_one_resource_and_sort(reverse_resource_dict, "Gem")["Gem"], colors=resource_colors),
    'gems_pie_plot',
    'figure',
    )

all_graphs = [
    global_table_graph,
    gold_bar_plot, gold_pie_plot,
    goods_bar_plot, goods_pie_plot,
    gems_bar_plot, gems_pie_plot,
    ]
