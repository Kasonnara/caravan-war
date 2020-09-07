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
from typing import List, Union, Dict, Type, Optional

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import dash
from plotly.subplots import make_subplots

from common.resources import ResourceQuantity, Resources, ResourcePacket
from economy.budget_simulator.simulation import RESOURCE_SORTING_MAP
from economy.chests import Chest
from economy.converters.abstract_converter import GainConverter
from economy.gains import Gain
from lang.languages import Language, TranslatableString
from utils.prettifying import camelcase_2_spaced, human_readable

GraphsUpdates = namedtuple('GraphsUpdates', 'update_func component_id target_attribute')

# Maybe not the best place to put this
resource_colors = {
    Resources.Gold: "gold",
    Resources.Goods: "#FF5000",
    Resources.Gem: "purple",
    Resources.Dust: "green",
    }


def resource_icons(app: dash.Dash, resource: ResourceQuantity.VALID_RESOURCE_TYPE, fail_safe=False,
                    **dash_img_extra_parameters) -> Optional[html.Img]:
    """
    Return a dash component displaying an icon for the given resource. If no image exist on disk for this resource, None
    is returned insted, except if fail_safe is to true where in this case a dummy component (an empty html Div) is
    returned insted.

    :param app: the main dash application
    :param resource: the target resource
    :param fail_safe: (default False) if set tu True, ensure you always have a dash component returned.
    :param dash_img_extra_parameters: extra parameter to forwed to the html.Img object (like height="20px", etc)
    """
    if isinstance(resource, Resources):
        resource_icon_filename = "{}.png".format(resource.name)
    elif isinstance(resource, Type):
        if issubclass(resource, Chest):
            resource_icon_filename = "{}.png".format(resource.__name__)
        else:
            resource_icon_filename = "random_{}.png".format(resource.__name__)
    # TODO handle all other VALID_RESOURCE_TYPE
    else:
        resource_icon_filename = None
        #raise NotImplemented("Resource type not supported")

    if resource_icon_filename is not None \
       and os.path.isfile(os.path.join("assets", "resources", resource_icon_filename)):

        # Target resource exists
        return html.Img(
            src=app.get_asset_url(os.path.join("resources", resource_icon_filename)),
            **dash_img_extra_parameters,
            )
    else:
        if fail_safe:
            # return a dummy component
            return html.Div()
        else:
            return None


graphs_to_update: List[GraphsUpdates] = []


class ResourceTable(dbc.Table):

    EMPTY_TABLE = (html.Thead(html.Tr([])), html.Tbody([]))

    def __init__(self, id: str, bordered=True, striped=False, hover=True, responsive=True, **kwargs):
        super().__init__(self.EMPTY_TABLE, id, bordered=bordered, striped=striped, hover=hover, responsive=responsive, **kwargs)
        # Register the graph
        graphs_to_update.append(GraphsUpdates(self.figures_updates, id, 'children'))

    @staticmethod
    def figures_updates(incomes: Dict[Union[str, TranslatableString],
                                      Dict[Union[Type[Gain], Type[GainConverter]], ResourcePacket]],
                        language: Language, app: dash.Dash) -> List[Union[html.Table, html.Tbody]]:
        # Compute total
        total = ResourcePacket()
        for gain_category in incomes:
            for key in incomes[gain_category]:
                # TODO there should be a function in ResourcePacket for that
                total = total + incomes[gain_category][key]

        incomes = incomes.copy()
        TOTALS_CATEGORY = TranslatableString('totals', french="totaux")
        incomes[TOTALS_CATEGORY] = {None: total}

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

        columns_names = [
            # Add the resource icon if it exists
            html.Th([
                resource_icons(app, res_type, height="20px", fail_safe=True),
                html.Div(ResourceQuantity.prettify_type(res_type, language=language))
                ],
                className='text-center',)
            for res_type in all_res_types
            ]

        return [
            Thead_or_Tbody
            for k, category in enumerate(incomes)
            for Thead_or_Tbody in [
                html.Thead(html.Tr([html.Th((category if not isinstance(category, TranslatableString)
                                            else category.translated_into(language)).upper())]
                                   + (columns_names if k == 0 or category is TOTALS_CATEGORY else ([html.Th()] * len(columns_names))),
                                   className='thead-light')),
                html.Tbody([
                    html.Tr(
                        [html.Td(gain.display_name(language=language).replace(' ', ' ')
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

    def figures_updates(self, incomes: Dict[Union[str, TranslatableString],
                                            Dict[Union[Type[Gain], Type[GainConverter]], ResourcePacket]],
                        language: Language, app: dash.Dash) -> List:
        # Extract incomes for the target resource, erase too small values, prettify gains names and sort them
        target_incomes_label, target_incomes_values = zip(
            *sorted(
                [(gain.display_name(language).replace(" ", " "),  # Prettify gains names
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
