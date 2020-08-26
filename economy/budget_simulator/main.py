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
from typing import List

import dash
# TODO see if bootstrap is really helpfull (currently use for sidebar and eventually its design)
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

from common.resources import Resources
from economy.budget_simulator import heroku_footer
from economy.budget_simulator.bs_ui_parameters import get_parameter_selector_id, get_parameter_selector_value_attibute, \
    get_parameter_value, build_parameters_selectors_list
from economy.budget_simulator.graphs import graphs_to_update, ResourceTable, ResourceBarPie
from economy.budget_simulator.simulation import update_income, all_parameters
from economy.budget_simulator.style import external_stylesheets, HEADER_STYLE, SIDEBAR_STYLE

# Detect if we run in standalone mode or on heroku (because heroku import this file not run it)
production_mode_on_heroku: bool = not (__name__ == '__main__')
# FIXME: it's simple but this isn't probably the most clever way to do. It may be safer and more controlable to
#   package everything in a main(args) function that takes configuration argument and an heroku_main() function or an
#   heroku_main script for heroku specific configuration changes. (and an argparse command line if we are motivated)

# Init the main application object (initialized early in order to allow creating callbacks)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
"""The main dash application object"""

# Register all persistent elements in order to build a callback that can disable all of them if the user disagree
persistent_components_ids: List[str] = []
"""Store all persistent elements ids"""

# Build the application TODO: move to another file
header = html.Div(
    children=[
        dbc.Container(
            children=[
                html.H1(children='CaravanWar Budget Simulator'),

                dcc.Markdown(children='''
                A web application for planning your resource earnings and losses in the game CaravanWar *(by [Kasonnara](https://github.com/Kasonnara/caravan-war-center))*  
                *(This is NOT an official application from Hiker Games)*
                '''),
                ],
                )],
    style=HEADER_STYLE,
    )

side_bar = html.Div(
    children=(
        # Sidebar title
        [html.H3('Configuration')]
        # Parameters categories and selectors
        + build_parameters_selectors_list(app, persistent_components_ids)
        ),
    id='configurationSideBar',
    className="bg-light border-right col-lg-3",
    style=SIDEBAR_STYLE,
    )

content = html.Div(
    children=[
        dcc.Markdown("## Global weekly incomes"),
        ResourceTable(app, 'global_resource_table'),
        ] + [elt
             for resource_type in (Resources.Gold, Resources.Goods, Resources.Gem)
             for elt in (dcc.Markdown("## {}".format(resource_type.name)), ResourceBarPie(resource_type))
             ],
    id='mainContent',
    className="col-lg-9",
    )

if production_mode_on_heroku:
    legal_footer = heroku_footer.build(app, persistent_components_ids)
else:
    # No need to put legal notice on standalone mode
    legal_footer = html.Div()


# Assemble the main components into the app
app.layout = html.Div(children=[
    header,
    html.Div(
        children=[
            side_bar,
            content,
            ],
        className='d-flex',
        id='wrapper'),
    legal_footer,
    ], )


@app.callback(
    [Output(graph.component_id, graph.target_attribute)
     for graph in graphs_to_update],
    [Input(get_parameter_selector_id(ui_param),
           get_parameter_selector_value_attibute(ui_param))
     for ui_param in all_parameters],
    )
def update_simulation(*ui_parameters_raw_values):
    """
    Main call back that update every graph as soon as any parameter changes
    :param ui_parameters_raw_values:
    :param weekly: bool
    :return: the new data for every graphs
    """
    # Generate the parameter value dict
    # TODO add category filtering
    ui_parameter_values = {
        ui_parameter.parameter_name: get_parameter_value(ui_parameter, raw_value)
        for ui_parameter, raw_value in zip(all_parameters, ui_parameters_raw_values)
        }
    # Get the new resources incomes
    incomes = update_income(ui_parameter_values)
    return [graph.update_func(incomes) for graph in graphs_to_update]


if production_mode_on_heroku:
    # Define the variable collected by Heroku to know what to use as web application
    server = app.server
else:
    app.run_server(debug=False)
