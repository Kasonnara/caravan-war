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
from typing import List


def get_index_greather_than(target_value: int, ascending_list: List[int]):
    """Assuming the input list is sorted in ascending order, return the index of the first element greather than the target value
    WARNING: if the target value is greater than any value of the array, it will return an invalid key, e.g. len(array)
    """
    for index, element in enumerate(ascending_list):
        if element > target_value:
            return index
    else:
        return len(ascending_list)
