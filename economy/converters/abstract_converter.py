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
from abc import abstractmethod
from collections import defaultdict
from enum import Enum, auto
from typing import List, Union, Type, Iterable, Optional, Dict, Any

import pandas

from common.resources import ResourcePacket
from utils.class_property import classproperty
from utils.ui_parameters import UIParameter, T


class ConverterModeUIParameter(UIParameter):
    """
    Factor a UI parameter configuration used by almost all GainConverter
    """
    class ConversionMode(Enum):
        DISABLED = "Disabled"
        """Converter is disabled"""
        IN_PLACE = "In place"
        """Conversion are applied directly to the gain results"""
        EXTERNAL = "As a separate gain"
        """Conversions appear as another separate gain"""

    def __init__(self, converter_class: Type['GainConverter'], value_range: Iterable[ConversionMode] = ConversionMode,
                 display_range: Iterable[str] = None,
                 default_value: Union[ConversionMode, int] = 0,
                 display_txt: Optional[str] = None, dependencies: Iterable['UIParameter'] = ()):
        super().__init__(converter_class.mode_parameter_name, value_range, display_range or [mode.value for mode in value_range], default_value,
                         (display_txt or (converter_class.__name__ + " conversion")), dependencies)


class GainConverter:
    """
    Abstract class for gain resources converters

    Converters are similar to Gains but instead of generating income independently their income depend on other gains
    and thus must be applied after.
    """

    ALL_CONVERTERS: List[Type['GainConverter']] = []
    """
    List all gain converters created
    """
    # TODO auto registering via Metaclass

    @classmethod
    @abstractmethod
    def get_diff(cls, resource_packet: ResourcePacket, gain_name: str, **kwargs) -> ResourcePacket:
        """
        Return the difference resulting from this Converter application.

        The input ResourcePacket object can be returned as is if no change are made, but it's never modified. If any
        change occur a new ResourcePacket object is created.

        :param resource_packet: ResourcePacket, the resources to convert
        :param gain_name: str, the name of the gain class
        :return: ResourcePacket, difference
        """
        raise NotImplemented()

    @classproperty
    def mode_parameter_name(cls):
        return cls.__name__.lower() + "_mode"

    @classmethod
    def apply_all(cls, resources_dict: Dict[str, ResourcePacket], ui_parameters: Dict[str, Any], converters: List[Type['GainConverter']] = None):
        """
        Apply all teh converters

        :param resources: Dict[ResourcePacket], the resources packets to eventually convert
            (WARNING: current implementation modify the dictionary in place for simplicity).
        :param ui_parameters: Dict[str, Any] the values of the UIParameter forwarded to the converters.
        :param converters: List[Type['GainConverter']], the converter to apply (default to cls.ALL_CONVERTERS).
        :return: Dict[ResourcePacket], reference to the modified <resources_dict> input parameter.
        """
        converters = converters or cls.ALL_CONVERTERS
        # Init the result dict
        #   init keys for the converter configured in EXTERNAL mode
        results = {converter.__name__: ResourcePacket()
                   for converter in converters
                   if ui_parameters.get(converter.mode_parameter_name, None) is ConverterModeUIParameter.ConversionMode.EXTERNAL}
        #   init other keys with all the values from input resources_dict (may override converter keys, ex: the lottery)
        results.update(resources_dict)

        # Apply each converter
        for converter in converters:
            converter_mode = ui_parameters.get(converter.mode_parameter_name,
                                               ConverterModeUIParameter.ConversionMode.DISABLED)
            if converter_mode is ConverterModeUIParameter.ConversionMode.DISABLED:
                pass
            else:
                for gain_key in resources_dict:
                    # if in place mode keep the same gain key, else take the converter key
                    if converter_mode is ConverterModeUIParameter.ConversionMode.IN_PLACE:
                        target_key = gain_key
                    else:  # converter_mode is ConverterModeUIParameter.ConversionMode.EXTERNAL
                        target_key = converter.__name__
                    results[target_key] = results[target_key] + converter.get_diff(resources_dict[gain_key], gain_key, **ui_parameters)

        return results
