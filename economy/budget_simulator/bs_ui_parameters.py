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
This module list budget simulator user defined parameters
and their corresponding GUI selector component automatic generation.
"""
from typing import List, Dict, Union

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.dependencies import Output, Input
from dash.development.base_component import Component

from economy.budget_simulator.style import LABEL_SETTING_BOOTSTRAP_COL, TOOLTIPS_STYLE

from economy.converters.converters import lottery_convert_mode_param, defense_lost_convert_mode_param, \
    legendary_soul_convert_mode_param, recycle_target_type_param, chest_opener_convert_mode_param, \
    recycle_convert_mode_param
from economy.gains.abstract_gains import rank_param, vip_param, hq_param, mesurement_range_param
from economy.gains.adds import pub_viewed_per_day_param
from economy.gains.daily_purchases import equipment_craft_number_param
from economy.gains.daily_rewards import daily_10km_trading_count_param, \
    daily_100km_trading_count_param, daily_1000km_trading_count_param, daily_best_trading_count_param, \
    selected_heroes_param, mill_lvl_param, station_lvl_param, ambush_won_param, ask_for_donation_param, \
    average_trophy_param, temple_lvl_param, defense_lost_param, fast_ambushes_param
from economy.gains.weekly_rewards import gates_passed_param, leaderboard_rank_param, \
    opponent_rank_param, clan_rank_param, battle_ranking_param, personal_boss_kill_per_fight_param, \
    clan_boss_kills_param, clan_league_param, clanwar1v1_result_param, clan_boss_attack_count_param
from lang.languages import TranslatableString
from lang.translation_dash_wrapper import wrap_dash_module_translation, TranslatableComponentRegister
from utils.ui_parameters import UIParameter

dcct = wrap_dash_module_translation(dcc)
htmlt = wrap_dash_module_translation(html)
dbct = wrap_dash_module_translation(dbc)

# ----- List and organize simulation parameters of the UI -----

BUDGET_SIMULATION_PARAMETERS: Dict[Union[str, TranslatableString], List[UIParameter]] = {
    TranslatableString('General', french="Géneral"): [
        mesurement_range_param,
        rank_param,
        vip_param,
        hq_param,
        pub_viewed_per_day_param,
        ],
    TranslatableString('Tradings', french="Échanges"): [
        daily_10km_trading_count_param,
        daily_100km_trading_count_param,
        daily_1000km_trading_count_param,
        daily_best_trading_count_param,
        defense_lost_param,
        defense_lost_convert_mode_param,
        ],
    TranslatableString('Units', french="Unités"): [
        mill_lvl_param,
        station_lvl_param,
        temple_lvl_param,
        ],
    TranslatableString('Ambushes', french="Embuscades"): [
        ambush_won_param,
        fast_ambushes_param,
        average_trophy_param,
        ],
    TranslatableString('Challenges', french="Défis"): [
        gates_passed_param,
        leaderboard_rank_param,
        ],
    TranslatableString('Clan'): [
        clan_league_param,
        clan_rank_param,
        battle_ranking_param,
        clanwar1v1_result_param,
        opponent_rank_param,
        personal_boss_kill_per_fight_param,
        clan_boss_kills_param,
        clan_boss_attack_count_param,
        ask_for_donation_param,
        ],
    TranslatableString('Conversions'): [
        lottery_convert_mode_param,
        selected_heroes_param,
        legendary_soul_convert_mode_param,
        recycle_convert_mode_param,
        recycle_target_type_param,
        chest_opener_convert_mode_param,
        ],
    TranslatableString('Purchases', french="Achats"): [
        equipment_craft_number_param,
        ],
    }
"""Store all budget simulation UIParameters (sorted into categories)"""

# ----- Utility functions -----

def get_parameter_selector_id(parameter: UIParameter) -> str:
    """
    Deterministically generate an html ID of the given UIParameter's selector

    Used to define dash callbacks triggered by a change of the selector value
    """
    return parameter.parameter_name + "_selector"


def get_parameter_selector_value_attibute(parameter: UIParameter) -> str:
    """
    For the given UIParameter's selector, return the name of the dash component attribute to use as value.

    Used to define dash callbacks triggered by a change of the selector value
    """
    return 'value' if parameter.value_range is not bool else 'checked'


def generate_dropdown_options(parameter: UIParameter):
    """For list like parameters, generate the data structure defining their dropdown options"""
    assert isinstance(parameter.value_range, tuple)
    return [{'label': txt, 'value': str(i)}
            for i, txt in enumerate(parameter.display_range)
            ]


def get_parameter_value(parameter: UIParameter, raw_value):
    """Convert dash component selector str values to the correct type/object depending of the parameter type"""
    if parameter.value_range is bool:
        return bool(raw_value)
    elif parameter.value_range is int:
        return int(raw_value)
    else:
        return parameter.value_range[min(len(parameter.value_range)-1, int(raw_value))]


def build_parameters_selectors_list(app: Dash, persistent_components_ids: List[str],
                                    translatable_components: TranslatableComponentRegister) -> List[Component]:
    """
    Generate the list of dash components to produce the list of simulation parameters' selectors

    :param app: Dash, the main dash application (used for generating callbacks)
    :param persistent_components_ids: list of the html ids of persisting components (**modified in place** by appending new ids!).
    """

    def build_parameter_selector(parameter: UIParameter):
        """
        Auxiliary function to generate a bootstrap row containing a title label and a selector
        for the given SimulationParameter.

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
            # An input textbox for integers parameter
            bootstrap_cols = LABEL_SETTING_BOOTSTRAP_COL['int']
            selector = dcc.Input(
                type="number",
                value=parameter.default_value_index,
                className="col-sm-{}".format(bootstrap_cols[1]),
                id=parameter_selector_id,
                persistence=True,
                )
        elif parameter.value_range is bool:
            # A checkbox for boolean parameter
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
        label = htmlt.Label(
            parameter.display_txt + ":",
            className="col-sm-{}".format(bootstrap_cols[0]),
            id=parameter_selector_id+"_label",
            translatable_components=translatable_components,
            )
        if parameter.help_txt is not None:
            info_bubble = dbc.Tooltip(dcct.Markdown(parameter.help_txt, id=parameter_selector_id+"_tooltip-content",
                                                     translatable_components=translatable_components,),
                                      target=parameter_selector_id+"_label",
                                      container="body",
                                      style=TOOLTIPS_STYLE,
                                      )
        else:
            info_bubble = html.Div()

        # Build a Bootstrap Row container to encapsulate the parameter label with its interactive selector component.
        return dbc.Row([label, selector, info_bubble])

    # Generate the full parameters selectors list while intercalating category's titles
    return [
        line
        for category_title in BUDGET_SIMULATION_PARAMETERS
        for line in (
            # Put an horizontal line, the name of this category
            [html.Hr(), htmlt.H4(category_title, id="{}-parameters-category-title".format(category_title),
                                 translatable_components=translatable_components)]
            # And follow with this category's parameters selectors.
            + [build_parameter_selector(parameter) for parameter in BUDGET_SIMULATION_PARAMETERS[category_title]]
            )
        ]
