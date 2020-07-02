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

from enum import Enum
from typing import List, Union, Type, Iterable, Optional, Dict, Any

from common.resources import ResourcePacket
from economy.gains import Gain
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

    ALL: List[Type['GainConverter']] = []
    """
    List all gain converters created (doesn't guaranty the order) 
    """
    # TODO auto registering via Metaclass

    @classmethod
    @abstractmethod
    def get_diff(cls, resource_packet: ResourcePacket, gain: Type[Gain] = None, **kwargs) -> ResourcePacket:
        """
        Return the difference resulting from this Converter application.

        :param resource_packet: ResourcePacket, the resources to convert
        :param gain: Optional[Gain], the gain class if the input resource_packet come from one.
        :return: ResourcePacket, the difference
        """
        raise NotImplemented()

    @classproperty
    def mode_parameter_name(cls):
        return cls.__name__.lower() + "_mode"

    @classmethod
    def apply_all(cls, resources_dict: Dict[str, Dict[Type[Gain], ResourcePacket]],
                  ui_parameters: Dict[str, Any],
                  converters: List[Type['GainConverter']] = None):
        """
        Apply all the converters to the input resources packets.

        Note: type of resource_dict may become Dict[str, Dict[Union[Type[Gain], Type['GainConverter']], ResourcePacket]]

        :param resources_dict: Dict[ResourcePacket], the resources packets to eventually convert
            (WARNING: current implementation modify the dictionary in place for simplicity).
        :param ui_parameters: Dict[str, Any] the values of the UIParameter forwarded to the converters.
        :param converters: List[Type['GainConverter']], the converter to apply (default to cls.ALL_CONVERTERS).
        """
        converters = converters or cls.ALL
        # Init the result dict
        #   init keys for the converter configured in EXTERNAL mode
        for converter in converters:
            if ui_parameters.get(converter.mode_parameter_name, None) is ConverterModeUIParameter.ConversionMode.EXTERNAL:
                if 'converters' not in resources_dict.keys():
                    resources_dict['converters'] = {}
                resources_dict['converters'][converter] = ResourcePacket()

        # Apply each converter
        for converter in converters:
            converter_mode = ui_parameters.get(converter.mode_parameter_name,
                                               ConverterModeUIParameter.ConversionMode.DISABLED)
            if converter_mode is ConverterModeUIParameter.ConversionMode.DISABLED:
                pass
            else:
                for gain_category in resources_dict:
                    for gain in resources_dict[gain_category]:
                        if gain == converter:
                            # Avoid applying a converter to it's own results, it makes no sense
                            continue
                        # if in place mode keep the same gain key, else take the converter key
                        if converter_mode is ConverterModeUIParameter.ConversionMode.IN_PLACE:
                            target_category, target_key = gain_category, gain
                        else:  # converter_mode is ConverterModeUIParameter.ConversionMode.EXTERNAL
                            target_category, target_key = 'converters', converter
                        resources_dict[target_category][target_key] = resources_dict[target_category][target_key] + converter.get_diff(resources_dict[gain_category][gain], gain=gain, **ui_parameters)

