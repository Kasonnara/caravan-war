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
This file contains the footer added when running the application in production on Heroku hosting service with
the '--heroku' option

This footer mainly contain information that are legally required (like host contact, cookie usage etc)
"""
from typing import List

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import dash
from dash.dependencies import Input, Output, State

from economy.budget_simulator.style import HEADER_STYLE

HEROKU_LEGAL_INFORMATIONS = "Salesforce.com France SAS - 3 Avenue Octave Gréard - 75007 Paris - Tél: +33 1 72 10 94 00"

COOKIE_MARKDOWN_DISCLAIMER = """
To improve user experience all **the simulator configuration entered in the left side of the page is stored into your 
browser in order to be persisted between sessions**. 

Please note that **we do not store any data on our servers**. Any persistence of the simulation parameters 
is kept on your computer only.

Please also notice that, with the exception of the simulation results which are directly displayed to you on this page, 
**no further processing of this data is performed** by us.
"""


def build(app: dash.Dash, persisting_components_ids: List[str]) -> html.Div:
    heroku_host_legal_informations = dcc.Markdown(
        children='''Hosting provider: *{heroku}*'''.format(heroku=HEROKU_LEGAL_INFORMATIONS))

    cookie_footer = dbc.Modal([
        dbc.ModalHeader("Data storage disclaimer"),
        dbc.ModalBody([
            dcc.Markdown(COOKIE_MARKDOWN_DISCLAIMER),
            ]),
        dbc.ModalFooter([
            dbc.Button("Accept", color='primary', id='persistence_accept_button'),
            dbc.Button("Do not persist configuration", id='persistence_refuse_button'),
            ])
        ],
        is_open=True,  # Open by default when the user connects
        backdrop='static',  # Cannot be skipped
        keyboard=False,  # Cannot be skipped
        id="cookie_disclamer_modal",
        )

    @app.callback(
        Output("cookie_disclamer_modal", "is_open"),
        [Input("persistence_accept_button", "n_clicks"), Input("persistence_refuse_button", "n_clicks")],
        )
    def close_persistense_disclaimer(*input_buttons):
        if any(input_buttons):
            # A button was pressed close the disclaimer for good
            return False
        else:
            # Maintain the disclaimer open
            return True
        # TODO add a way to reopen the modal to change his consent

    @app.callback(
        [Output(persisting_component_id, "persistence") for persisting_component_id in persisting_components_ids],
        [Input("persistence_accept_button", "n_clicks"), Input("persistence_refuse_button", "n_clicks")],
        )
    def set_persistense(persistence_accepted, persistence_refused):
        if persistence_accepted:
            return [True] * len(persisting_components_ids)  # useless as it's the default
            # TODO persist that the user has agreed in order to not show the modal next time.
        elif persistence_refused:
            return [False] * len(persisting_components_ids)
            # TODO add a button to delete all previously persisted data, and make everything not persistent by default.

        # By default persistence is ON  TODO: is it good? or should we opt-out by default (this alternative may destroy
        #                                  persisted value at each statup)?
        #                                  the best idea would be to maintain state, but this may cause useless loop and
        #                                  just report the problem what-ever value is set when initializing the
        #                                  component (e.g. currently True)
        return [True] * len(persisting_components_ids)

    return html.Div(
        children=[
            dbc.Container(
                children=[
                    dcc.Markdown("Contacting me: [wins@kasonnara.fr](mailto:wins@kasonnara.fr)"),
                    heroku_host_legal_informations,
                    cookie_footer,
                    ],
                style={'margin': "2em"},
                ),
            ],
        style=HEADER_STYLE,
        )
