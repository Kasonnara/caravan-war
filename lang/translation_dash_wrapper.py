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
This module add global static text translation to dash component.
"""
from collections import namedtuple
from modulefinder import Module
from typing import Type, Callable, Union, Any, Dict, Optional

from dash import dash
from dash.dependencies import Input, Output
from dash.development.base_component import Component as DashComponent
import dash_core_components as dcc

from lang.languages import TranslatableString, Language


TranslatableComponentAttribute = namedtuple('TranslatableComponentAttribute', ['id', 'attr_name', 'translations'])


class TranslatableComponentRegister(Dict[str, TranslatableComponentAttribute]):
    def __init__(self):
        super().__init__()
        self.callback_built = False  # todo change into a slot


class FakeModule(Dict[str, Callable[..., DashComponent]]):
    def __setattr__(self, component_name: str, wrapped_component_constructor: Callable[..., DashComponent]):
        self[component_name] = wrapped_component_constructor

    def __getattr__(self, component_name: str):
        return self[component_name]

    # TODO: I don't see any use for it yet, but it may be interesting to implement a more in-depth copy of the input module.
    #   By including currently ignored attributes that are not Dash component.
    #   Ultimately if we find a way to transparently replace the module instance by the result of this function without
    #   loosing any module attribute nor type hinting it would be perfect.


def wrap_dash_module_translation(
        dash_module: Union[Module, '__init__.py'],
        translatable_components: Optional[TranslatableComponentRegister] = None,
        initial_translation: Language = Language.ENGLISH,
        ) -> FakeModule:
    """
    Inspect the given Dash module, search for Dash Component class, wrap their cosntructor to support TranslatableString
    and return a dictionary containing these new constructors.

    You should run this function on all your imported dash module at the beginning of your script.

    :param dash_module: a Dash module to inspect
    :param translatable_components: Optional, globally set the dictionary in which the registered translation will be
        inserted. If it is not provided here, the dictionary will be required locally at each dash component construction.
    :param initial_translation: globally set the default language forwarded to the dash component constructor.
            This isn't really useful as it will be overridden as soon as the translation callback is setup.
    :return: An object containing all the new wrapped constructors as attributes
    """
    fake_module = FakeModule()

    # Search if there is Dash component class definition in this module
    for attr_name, module_attr in dash_module.__dict__.items():
        if isinstance(module_attr, type) and issubclass(module_attr, DashComponent):
            # Wrap the Dash component constructor
            fake_module[attr_name] = wrap_translation(module_attr,
                                                      translatable_components=translatable_components,
                                                      initial_translation=initial_translation)
    return fake_module


def wrap_translation(
        dash_component_class: Type[DashComponent],
        translatable_components: Optional[TranslatableComponentRegister] = None,
        initial_translation: Language = Language.ENGLISH,
        ) -> Callable[..., DashComponent]:
    """
    Wraps a single Dash component class constructor to allow it supporting TranslatableString.

    :param dash_component_class: that dash component class to add translation support to.
    :param translatable_components: Optional, globally set the dictionary in which the registered translation will be
        inserted. If it is not provided here, the dictionary will be required locally at each dash component construction.
    :param initial_translation: globally set the default language forwarded to the dash component constructor.
            This isn't really useful as it will be overridden as soon as the translation callback is setup.
    :return:
    """
    assert translatable_components is None or not translatable_components.callback_built, \
        "Error: once the language callback have been built you must " \
        "not register new dash component with translatable string. As a consequence, all these components must be " \
        "statically defined and the callback setup must be the last instruction."

    def register_translatable_strings(
            children: Union[TranslatableString, Any]=None,
            id=DashComponent.UNDEFINED,
            translatable_components: Dict[str, TranslatableComponentAttribute]=translatable_components,
            initial_translation: Language = initial_translation,
            **kwargs) -> DashComponent:
        """
        Wrapper for any dash component that, intercept TranslatableString, and register them into
        translatable_components for later generation of a global translation callback.

        Then the Dash component is instantiated normally using the default translation and returned.

        :param children: Provide a TranslatableString to enable translation, else children will be forwarded to the
            dash component constructor.
        :param id: The dash component id (Mandatory if a TranslatableString is provided).
        :param translatable_components: a dictionary in which the registered translation will be inserted (Mandatory
            if a TranslatableString is provided).
        :param initial_translation: set which text translation is first forwarded to the dash component constructor.
            This isn't really useful as it will be overridden as soon as the translation callback is setup. Default
            ENGLISH or whatever else that have been set globally when wrapping the constructor
        :param kwargs: Any other parameter to forward to the dash component.
        :return: the dash component generated.
        
        Initial Dash Component doc:

        """
        # TODO: Is there a way to make this function appear in type-checker with the initial component constructor
        #  exact same signature (with the addition of translatable_components)?
        #  It's not really mandatory but it help IDE users by not disrupting dash component hints.

        # Note: It's unlikely, but if this wrapper ever cause a useless performance issue (when generating many
        #   components that never provide TranslatableStrings), it may be faster to start by checking that the 'id' and
        #   'translatable_components' parameters are provided, and if not skip the expensive search for
        #   TranslatableStrings.
        #   Indeed, in the current implementation, the presence of the 'id' parameter is only asserted after a
        #   TranslatableString is found. This is done to avoid silent mistakes, if the developer truly want translation
        #   and provide a TranslatableString but forget to provide other parameters.

        # Search for TranslatableStrings
        if isinstance(children, TranslatableString):
            assert id is not DashComponent.UNDEFINED, "If you want to use TranslatableString, 'id' must be defined " \
                                                      "to allow callback creation."
            assert translatable_components is not None, "If you want to use TranslatableString, 'translatable_components'" \
                                                        " must be provided to allow send back the translation registration."
            # Register the translation
            translatable_components[id] = TranslatableComponentAttribute(id, 'children', children)
            # Replace the TranslatableString by a str to forward to the Dash component constructor.
            children = children.translated_into(initial_translation)

        # TODO: inspect other parameter too

        return dash_component_class(children=children, id=id, **kwargs)

    # FIXME comment that out in production
    if dash_component_class.__init__.__doc__ is not None:
        register_translatable_strings.__doc__ = register_translatable_strings.__doc__ + dash_component_class.__init__.__doc__

    return register_translatable_strings


# TODO: I don't see any use for it yet, but it may be interesting to implement a true class decorator that generate a
#  full subclass allowing to keep all the class attributes and completely replace the initial component class with
#  the wrapped one.

def build_language_selector(id="language_selector", persistence=True) -> dcc.Dropdown:
    return dcc.Dropdown(
        options=[{'label': lang.display_name, 'value': lang.name}
                 for lang in Language
                ],
        value=Language.ENGLISH.name,
        clearable=False,
        id=id,
        persistence=persistence,
        style={"min-width": "7em"},  # Workaround: the dropdown strangely doesn't scale according to its content
        )


def setup_language_callback(
        app: dash.Dash,
        translatable_components: TranslatableComponentRegister,
        language_selector_id="language_selector"):

    assert not translatable_components.callback_built, "Error: language callback can only be built once"

    @app.callback(
        output=[Output(id, target_attr) for id, target_attr, _ in translatable_components.values()],
        inputs=[Input('language_selector', 'value')],
        )
    def language_callback(language_name: str):
        selected_language = Language.__members__[language_name]
        return [translatable_string.translated_into(selected_language)
                for _, _, translatable_string in translatable_components.values()]

    # Flag the TranslatableComponentRegister to indicated that the language callback has been built already and
    # forbid new translation registration
    translatable_components.callback_built = True

    return language_callback

