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
Main scrit of the dash application to simulate regular earnings and losses.
"""

import dash
# TODO see if bootstrap is really helpfull (currently use for sidebar and eventually its design)
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
from dash.dependencies import Input, Output

from common.leagues import Rank
from common.resources import ResourcePacket, Resources
from economy.budget_simulator.graphs import all_graphs, global_table_graph, gold_bar_plot, goods_bar_plot, \
    gems_bar_plot, gold_pie_plot, goods_pie_plot, gems_pie_plot
from economy.budget_simulator.simulation import all_parameters, income_dict, reverse_income_dict
from economy.gains import BUDGET_SIMULATION_PARAMETERS
from utils.selectable_parameters import UIParameter

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

HEADER_STYLE = {
    "background-color": "#f8f9fa",
    "padding": "1rem",
    }

SIDEBAR_STYLE = {
    #"width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    }

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    }

header = html.Div(
    children=[
        dbc.Container(
            children=[
                html.H1(children='CaravanWar Budget Simulator'),

                dcc.Markdown(children='''
                A web application for planning your resource earnings and losses in the game CaravanWar *(by [Kasonnara](https://github.com/Kasonnara/caravan-war-center))*
                '''),
                ],
                )],
    style=HEADER_STYLE,
    )

LABEL_SETTING_BOOTSTRAP_COL = {
    "int": (7, 4),
    "bool": (10, 1),
    "default": (4, 8),
    }


def build_parameter_selector(parameter: UIParameter):
    """Generate a bootstrap row containing a label and a selector for the given SimulationParameter"""
    if parameter.is_integer:
        bootstrap_cols = LABEL_SETTING_BOOTSTRAP_COL['int']
        selector = dcc.Input(
            type="number",
            value=parameter.default_value,
            className="col-sm-{}".format(bootstrap_cols[1]),
            id = parameter.parameter_name + "_selector",
            )
    elif parameter.is_bool:
        bootstrap_cols = LABEL_SETTING_BOOTSTRAP_COL['bool']
        selector = dbc.Checkbox(
            checked=parameter.default_value,
            className="col-sm-{}".format(bootstrap_cols[1]),
            id=parameter.parameter_name+"_selector",)
    else:
        bootstrap_cols = LABEL_SETTING_BOOTSTRAP_COL["default"]
        selector = html.Div([
            dcc.Dropdown(
                options=[{'label': txt, 'value': str(i)}
                         for i, txt in enumerate(parameter.display_range)
                         ],
                value=str(parameter.default_value),
                clearable=False,
                id=parameter.parameter_name+"_selector",
                )],
            className="col-sm-{}".format(bootstrap_cols[1]),
            )

    return dbc.Row([
        html.Label(parameter.display_txt + ":",
                   className="col-sm-{}".format(bootstrap_cols[0]),
                   ),
        selector,
        ],
        )


side_bar = html.Div(
    children=(
        # Sidebar title
        [html.H3('Configuration')]
        # Parameters categories
        + [
            line
            for category_title in BUDGET_SIMULATION_PARAMETERS
            for line in ([
                # For each category put
                #   - an horizontal line
                html.Hr(),
                #   - its title and optionaly the disabling checkbox
                #dbc.Row([html.H4(category_title, className="col-sm-11"),
                #         dbc.Checkbox(checked=True, className="col-sm-1")])
                #if category_title != "General"
                #else html.H4(category_title)
                html.H4(category_title),
             ]
            #       - Followed by the selectors of its parameters
             + [build_parameter_selector(parameter) for parameter in BUDGET_SIMULATION_PARAMETERS[category_title]])

            ]
        ),
    id='configurationSideBar',
    className="bg-light border-right col-lg-3",
    style=SIDEBAR_STYLE,
    )

content = html.Div(
    children=[
        dcc.Markdown("## Global weekly incomes"),
        global_table_graph.build_func(),
        dbc.Row([
            html.Div([
            gold_bar_plot.build_func(),
            goods_bar_plot.build_func(),
            gems_bar_plot.build_func(),
                ],
                className="col-lg-8",
                ),
            html.Div([
            gold_pie_plot.build_func(),
            goods_pie_plot.build_func(),
            gems_pie_plot.build_func(),
                ],
                className="col-lg-4",
                ),
            ]),
        ],
    id='mainContent',
    className="col-lg-9",
    )

app.layout = html.Div(children=[
    header,
    html.Div(
        children=[
            side_bar,
            content,
            ],
        className='d-flex',
        id='wrapper')

    ], )


@app.callback(
    [Output(graph_id, grph_target_attr)
     for _, _, graph_id, grph_target_attr in all_graphs],
    [Input(ui_param.parameter_name + "_selector", 'value' if not ui_param.is_bool else 'checked')
     for ui_param in all_parameters],
    )
def update_simulation(*simulation_parameter, weekly=True):
    """
    Main call back that update every graph as soon as any parameter changes
    :param simulation_parameter:
    :param weekly: bool
    :return: the new data for every graphs
    """
    # Get the new resources
    resourcepacket_dict = income_dict(*simulation_parameter, weekly=weekly)
    reverse_resourcepacket_dict = reverse_income_dict(resourcepacket_dict)

    resourcepacket_dict['Total'] = sum(resourcepacket_dict.values(), ResourcePacket())

    return tuple(graph_update_func(resourcepacket_dict, reverse_resourcepacket_dict)
                 for _, graph_update_func, _, _ in all_graphs)


if __name__ == '__main__':
    app.run_server(debug=True)
