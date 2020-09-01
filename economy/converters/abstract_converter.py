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
from typing import List, Union, Type, Iterable, Optional, Dict, Any, Callable

from common.resources import ResourcePacket
from economy.gains import Gain
from lang.languages import TranslatableString
from utils.class_property import classproperty
from utils.prettifying import Displayable
from utils.ui_parameters import UIParameter, T


class ConverterModeUIParameter(UIParameter):
    """
    Factor a UI parameter configuration used by almost all GainConverter
    """
    class ConversionMode(Enum):
        DISABLED = "Disabled"
        """Converter is disabled"""
        IN_PLACE = "In place"
        """Conversion are applied directly to the gain results"""
        EXTERNAL = "Separate gain"
        """Conversions appear as another separate gain"""

    def __init__(self, converter_class: Type['GainConverter'], value_range: Iterable[ConversionMode] = ConversionMode,
                 display_range: Iterable[str] = None,
                 default_value: Union[ConversionMode, int] = 0,
                 display_txt: Optional[Union[str, TranslatableString]] = None,
                 update_callback: Callable = None,
                 dependencies: Iterable['UIParameter'] = None,
                 help_txt: Optional[Union[str, TranslatableString]] = None,
                 ):
        if help_txt is None:
            help_txt = TranslatableString("{} converter possible modes:",
                                          french="Modes possibles du convertiseur {}",
                                          ).format(converter_class.display_name())
        elif not isinstance(help_txt, TranslatableString):
            help_txt = TranslatableString(help_txt)
        help_txt = (help_txt
                    + (TranslatableString(
                           "\n- **Disabled**: Do nothing.",
                           french="\n- **Disabled**: Ne fait rien.",
                           ) if self.ConversionMode.DISABLED in value_range else "")
                    + (TranslatableString(
                           "\n- **In place**: Modify existing gains records in place.",
                           french="\n- **In place**: Modifie le gain existant correspondant.",
                           ) if self.ConversionMode.IN_PLACE in value_range else "")
                    + (TranslatableString(
                           "\n- **As a separate gain**: Aggregate all consumed and produced resources into a new separated gain record.",
                           french="\n- **As a separate gain**: Additionne toutes les conversions comme un gain à part.",
                           ) if self.ConversionMode.EXTERNAL in value_range else "")
                    )
        super().__init__(
            converter_class.mode_parameter_name,
            value_range,
            display_range=display_range or [mode.value for mode in value_range],
            default_value=default_value,
            display_txt=(display_txt or (converter_class.__name__ + " conversion")),
            update_callback=update_callback,
            dependencies=dependencies,
            help_txt=help_txt,
            )


class GainConverter(Displayable):
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

    CONVERTER_CATEGORY = TranslatableString("converters", french="convertisseurs")

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
        # FIXME: converters badly behave with consumed negative values, at best they ignore them, at worst as they do
        #    not have an overall vue, they remove all positive values of a certain type which already has negative
        #    values. They cant simply apply negatively to this negative gains (at least not in IN_PLACE mode), but
        #    ignoring them make the converters convert more that what is allowed.
        #    To solve that the converter should have know before hand how many it can convert in total including the
        #    negative values in order to consume a little less on any other positive value.
        #    This can be done with the current structure... As a workaround we can fill a precomputed 'total' dict that
        #    indicate the amount of positive and negative values to anticipate but it's not pretty.
        #    A cleaner way would probably need to ask converter to apply to the entire diction at once insted of gain by
        #    gain. This need a certain quantity of rework and probably abandon the level of code factorization we now
        #    have...
        #    [As a quick fix I only forbid the Recycle converter to work in IN_PLACE mode which is the only one which
        #    currently makes ths problem to apear in practice]


        converters = converters or cls.ALL
        # Init the result dict
        #   init keys for the converter configured in EXTERNAL mode
        for converter in converters:
            if ui_parameters.get(converter.mode_parameter_name, None) is ConverterModeUIParameter.ConversionMode.EXTERNAL:
                if cls.CONVERTER_CATEGORY not in resources_dict.keys():
                    resources_dict[cls.CONVERTER_CATEGORY] = {}
                resources_dict[cls.CONVERTER_CATEGORY][converter] = ResourcePacket()

        # Apply each converter
        for converter in converters:
            converter_mode = ui_parameters.get(converter.mode_parameter_name,
                                               ConverterModeUIParameter.ConversionMode.IN_PLACE)
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
                            target_category, target_key = cls.CONVERTER_CATEGORY, converter
                        resources_dict[target_category][target_key] = resources_dict[target_category][target_key] + converter.get_diff(resources_dict[gain_category][gain], gain=gain, **ui_parameters)

