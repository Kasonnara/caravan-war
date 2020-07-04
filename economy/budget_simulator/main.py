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
from economy.budget_simulator.bs_ui_parameters import BUDGET_SIMULATION_PARAMETERS
from economy.budget_simulator.graphs import graphs_to_update, ResourceTable, ResourceBarPie
from economy.budget_simulator.simulation import update_income, all_parameters
from economy.budget_simulator.style import external_stylesheets, HEADER_STYLE, SIDEBAR_STYLE, \
    LABEL_SETTING_BOOTSTRAP_COL

from utils.ui_parameters import UIParameter

# Detect if we run in standalone mode or on heroku (because heroku import this file not run it)
production_mode_on_heroku: bool = not (__name__ == '__main__')
# FIXME: it's simple but this isn't probably the most clever way to do. It may be safer and more controlable to
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


def get_parameter_selector_id(parameter: UIParameter):
    """
    Return the html id of the UIParameter's selector

    Used to define dash callbacks triggered by a change of the selector value

    :param parameter: UIParameter, the
    :return: str
    """
    return parameter.parameter_name + "_selector"


def get_parameter_selector_value_attibute(parameter: UIParameter):
    """
    For the given UIParameter's selector, return the name of the attribute to use as value.

    Used to define dash callbacks triggered by a change of the selector value

    :param parameter: UIParameter, the
    :return: str
    """
    return 'value' if parameter.value_range is not bool else 'checked'


def generate_dropdown_options(parameter: UIParameter):
    assert isinstance(parameter.value_range, tuple)
    return [{'label': txt, 'value': str(i)}
            for i, txt in enumerate(parameter.display_range)
            ]


def get_parameter_value(parameter: UIParameter, raw_value):
    if parameter.value_range is bool:
        return bool(raw_value)
    elif parameter.value_range is int:
        return int(raw_value)
    else:
        return parameter.value_range[min(len(parameter.value_range)-1, int(raw_value))]


def build_parameter_selector(parameter: UIParameter):
    """
    Generate a bootstrap row containing a title label and a selector for the given SimulationParameter

    The function is able to generate 3 types of selectors:
    - checkbox, for boolean type of UI parameter
    - number input box for int type of UI parameter
    - dropdown for list type of UI parameters

    :param parameter: UIParameter the parameter for which a selector will be generated
    :return: bcc.Row:  a Dash Bootstrap Row
    """

    parameter_selector_id = get_parameter_selector_id(parameter)
    # Generate the interactive selector component that best fit the UI parameter type
    if parameter.value_range is int:
        # An input textbox for integers parameter
        bootstrap_cols = LABEL_SETTING_BOOTSTRAP_COL['int']
        selector = dcc.Input(
            type="number",
            value=parameter.default_value_index,
            className="col-sm-{}".format(bootstrap_cols[1]),
            id=parameter_selector_id,
            persistence=True,
            )
    elif parameter.value_range is bool:
        # A checkbox for boolean parameter
        bootstrap_cols = LABEL_SETTING_BOOTSTRAP_COL['bool']
        selector = dbc.Checkbox(
            checked=parameter.default_value_index,
            className="col-sm-{}".format(bootstrap_cols[1]),
            id=parameter_selector_id,
            persistence=True,
            )
    elif isinstance(parameter.value_range, tuple):
        # A dropdown for other list like selection
        assert parameter.display_range is not None
        bootstrap_cols = LABEL_SETTING_BOOTSTRAP_COL["default"]
        selector = html.Div([
            dcc.Dropdown(
                options=generate_dropdown_options(parameter),
                value=str(parameter.default_value_index),
                clearable=False,
                id=parameter_selector_id,
                persistence=True,
                )],
            className="col-sm-{}".format(bootstrap_cols[1]),
            )
        # Setup the selector update callback if this parameter have dependencies
        if parameter.dependencies is not None:
            @app.callback(
                [Output(parameter_selector_id, 'options')],
                [Input(get_parameter_selector_id(parent_parameter),
                       get_parameter_selector_value_attibute(parent_parameter))
                 for parent_parameter in parameter.dependencies],
                )
            def update_dropdown_selector(*dependencies_raw_values):
                # Get the values of the parent parameter
                dependencies_values = [get_parameter_value(parent_parameter, raw_value)
                                       for parent_parameter, raw_value in zip(parameter.dependencies, dependencies_raw_values)]
                # Update the UIParameter attributes
                parameter.update(dependencies_values)
                # Re-generate the dropdown options
                return [generate_dropdown_options(parameter)]
    else:
        raise NotImplementedError("Cannot generate a selector for {} UIParameter of type {}".format(parameter.display_txt, type(parameter.value_range)))

    # Register the persistent element
    persistent_components_ids.append(parameter_selector_id)

    # Generate a title label
    label = html.Label(
        parameter.display_txt + ":",
        className="col-sm-{}".format(bootstrap_cols[0]),
        )

    # Build a Bootstrap Row container to encapsulate the parameter label with its interactive selector component.
    return dbc.Row([label, selector])


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
        ResourceTable(app, 'global_resource_table'),
        ] + [elt
             for resource_type in (Resources.Gold, Resources.Goods, Resources.Gem)
             for elt in (dcc.Markdown("## {}".format(resource_type.name)), ResourceBarPie(resource_type)) ],
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
