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
Data about adds rewards
"""
from common.resources import Resources as R, ResourcePacket
from economy.gains.abstract_gains import Gain
from lang.languages import TranslatableString
from utils.ui_parameters import UIParameter

gold_adds_per_day = 10
gem_adds_per_day = 1
max_adds_per_day = gold_adds_per_day + gem_adds_per_day

adds_delay = 60*60  # 1 hour
adds_max_stacking = 3

adds_reward_per_hq_level = [
    ResourcePacket(
        R.Gem(20 * (gem_adds_per_day/max_adds_per_day)),
        R.Gold(gold_reward * (gold_adds_per_day/max_adds_per_day))
        )
    for gold_reward in [
        0.0,
        0, 1500, 1500, 3000, 5250,
        9000, 15000, 25500, 36300, 52950,
        71250, 105000, 210000, 450000, 592500,
        937500, 1500000, 2392500, 3750000, 6000000,
        7875000, 10406250, 14662500, 19125000, 26775000,
        40425000, 60900000, 84000000, 105000000, 131250000
        ]
    ]


pub_viewed_per_day_param = UIParameter(
    'pub_viewed_per_day',
    range(max_adds_per_day + 1),
    display_txt="Daily adds",
    help_txt="Select the average number of adds you view per day.",
    )


class Adds(Gain):
    __display_name = TranslatableString("Adds", french="Publicités")

    @classmethod
    def iteration_income(cls, hq_lvl: int = 1, **kwargs) -> ResourcePacket:
        return adds_reward_per_hq_level[hq_lvl]

    @classmethod
    def daily_income(cls, hq_lvl: int = 1, pub_viewed_per_day: int = None, **kwargs) -> ResourcePacket:
        pub_viewed_per_day = pub_viewed_per_day or 0
        assert 0 <= pub_viewed_per_day <= 12
        return cls.iteration_income(hq_lvl=hq_lvl, **kwargs) * pub_viewed_per_day
