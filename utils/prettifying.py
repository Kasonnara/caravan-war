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
<Module docstring>
"""
import math
import re
from typing import Optional, Union

import pandas

from lang.languages import Language, TranslatableString

_meta_unit_list = ['', 'K', 'M', 'B']
"""~= No meta unit, thousand, million, billion"""


def human_readable(value: int, erase_under: Optional[float] = None) -> str:
    """
    Return a human readable string using K, M, B units for big values.

    :param value: int, The value to prettify
    :param erase_under: Optional[float], if set, replaced by an empty string NaN values and values whose
        absolute value is inferior to that.
    :return: str
    """
    # Check for values to eraze
    abs_value = abs(value)
    if (value is pandas.NA) or (math.isnan(value)) or (erase_under is not None and abs_value <= erase_under):
        return ""

    # Find the closest meta unit
    for k, meta_unit in enumerate(_meta_unit_list):
        meta_unit_base = 1000 ** k
        if abs_value < 10 ** (3 * (k+1)) or (k == len(_meta_unit_list) - 1):
            return "{}{}{}".format('-' if value < 0 else '', round(abs_value / 10 ** (3 * k), 2), meta_unit)
    assert False


def camelcase_2_spaced(camelcase_text: str, unbreakable_spaces=False) -> str:
    """
    Convert a CamelCase name into a space separated name.

    :param camelcase_text: The text to re-space.
    :param unbreakable_spaces: if set to True, use unbreakable space instead of usual spaces.
    :return: str
    """
    return re.sub('(?!^)([A-Z][a-z]+)', r' \1' if unbreakable_spaces else r' \1', camelcase_text)


class Displayable:
    """Mixxin class that add the display_name function

    Subclass implementing Displayable must set the class attribute '__display_name' with an str or a TranslatableString.

    If '__display_name' stay undefined, the class name itself is taken by default after a little prettifying process.
    """

    # FIXME this function should only be called by class, this doesn't have real meaning for class instances.

    # TODO is there a clean way to also support ENUMs in the default code. Because at the moment many enums extends from
    #  the Displayable mixin class, but only for the symbolic meaning as they all reimplement the display_name function
    #  (always with almost the same code and without classmethod decorator)
    @classmethod
    def display_name(cls, language=Language.ENGLISH) -> str:
        """Return a default Translatable object base on the class name"""
        # Get the mangled class attribute if it has been defined
        name: Optional[Union[str, TranslatableString]] = getattr(cls, "_" + cls.__name__ + "__display_name", None)

        if name is None:
            return camelcase_2_spaced(cls.__name__)
        elif isinstance(name, TranslatableString):
            return name.translated_into(language)
        else:
            return name
