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
import collections
from typing import Type, Union, Iterable, Optional, Callable, TypeVar, List

T = TypeVar('T')


class UIParameter:
    """Define the properties of a parameter needed to generate an UI for it"""
    def __init__(self,
                 parameter_name: str,
                 value_range: Union[Type[int], Type[bool], Iterable[T]],
                 display_range: Optional[Iterable[str]] = None,
                 default_value: Union[T, int] = 0,
                 display_txt: Optional[str] = None,
                 dependencies: Iterable['UIParameter'] = (),
                 ):
        """
        :param parameter_name: str, the name of the parameter. This is used as key in the parameter dictionary.
        :param value_range: this parameter can be:
            - the type int itself, which means that the parameter is an integer (with any integer value).
            - the type bool itself, which means that the parameter is a boolean
            - a Iterable of simulation parameter possible values (probably represented in GUI as a dropdown menu).
        :param display_range: An iterable that contains the string representation of value_range values used in UI.
            If value_range is an list then this parameter must be specified, else it is omitted.
        :param display_txt: An optional string used by the UI to display this parameter. If omitted, a display name will
            be generated from parameter_name.
        :param default_value: The default value of the parameter or it's index in value_range.
        :param dependencies: The list other parameters this parameter depends on, if they change a callback is
            triggered. (Not implemented yet)
        """
        assert isinstance(default_value, (int, bool)) or isinstance(value_range, collections.abc.Iterable)

        self.parameter_name = parameter_name
        self.value_range = tuple(value_range) if isinstance(value_range, collections.abc.Iterable) else value_range
        self.display_range = display_range
        self.display_txt = display_txt or parameter_name.replace('_', ' ').title()
        self.dependencies = dependencies
        self.default_value = (
            default_value
            if isinstance(default_value, (int, bool))
            else self.value_range.index(default_value)
            )
        """The index of the value selected by default"""
