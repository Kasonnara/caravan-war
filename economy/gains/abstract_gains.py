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
Gains common code
"""
from abc import abstractmethod
from collections import defaultdict
from enum import Enum, IntEnum
from typing import List

from common.cards import MAX_LEVEL
from common.leagues import Rank
from common.resources import ResourcePacket
from common.vip import VIP
from utils.ui_parameters import UIParameter


class Days(IntEnum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6


class MeasurementPeriod(Enum):
    DAY = 1
    # TODO include measurement of specific days
    WEEK = 7
    MONTH = 30


# ------------------------ Gains parameters ------------------------
# Used to generate parameter selection UI

# You can create new parameters were you think it's the more readable/logical. Here or directly near the Gains classes
# that use them. By convention I define global parameters here, and parameters that are specific to one or a few gains
# are defined next to them.
# Just don't forget to add them to the BUDGET_SIMULATION_PARAMETERS for the UI to find them. You can also
# creates new categories if you want just use str keys.

mesurement_range_param = UIParameter('mesurement_range', MeasurementPeriod, display_txt="Average by",
                                     help_txt="Select the period over which gains will be accumulated.")
rank_param = UIParameter('rank', Rank, display_range=[rank.name for rank in Rank], default_value=Rank.NONE,
                         help_txt="Select your rank. *(If you select NONE, gold and cargo of gains that depend on it "
                                  "will be given as X time the reward of your 10km trading)*")
vip_param = UIParameter('vip', VIP, display_range=[vip_lvl.name for vip_lvl in VIP],
                        display_txt="VIP", default_value=7, help_txt="Select your VIP level.")
hq_param = UIParameter('hq_lvl', range(1, MAX_LEVEL+1), display_range=[str(vip_lvl) for vip_lvl in range(1, MAX_LEVEL+1)],
                       display_txt="HQ", default_value=15, help_txt="Select the level of your head quarters.")


# ------------------------ Gains abstract class ------------------------

class Gain:
    """
    Abstract class for modeling regular incomes in the game

    Gains are implemented as static singletons, and thus must never be instantiated nor have instance methods, only
    static or class methods. Each new class defining a different gain.
    """
    # TODO try making Gain into a metaclass

    parameter_dependencies: List[UIParameter] = []

    def __init__(self):
        raise AssertionError("Gains classes should be static singletons and thus must not be instanced")

    @classmethod
    @abstractmethod
    def iteration_income(cls, **kwargs) -> ResourcePacket:
        """Return the resources given for one iteration of the gain.
        (This function is mostly there for its semantic meaning as of now it's always daily_income that is used)"""
        raise NotImplemented()

    @classmethod
    @abstractmethod
    def daily_income(cls, day: Days = None, **kwargs) -> ResourcePacket:
        """
        Return the daily income from this source.

        :param rank: league.Rank, The rank level of the player
        :param hq_lvl: int, The HeadQuarter level of the player
        :param vip: vip.VIP, The VIP level of the player
        :param day: gains.Days, if defined the function return the gain on this specific day
                                else the function return the average gain per day.
        :param kwargs: optional arguments that may define personal habits (e.g. the usual number of trading launched),(vary on each gain class)
        :return: ResourcePacket
        """
        raise NotImplemented()

    @classmethod
    def average_income(cls, mesurement_range=MeasurementPeriod.DAY, **kwargs) -> ResourcePacket:
        """
        Wrapper to get average income over various periods

        :param mesurement_range: MesurementRange, ther period over which we want to get the average income
        For other parameters see daily_income
        :return: ResourcePacket, the average total income for this gain over the given period
        """
        assert 'day' not in kwargs.keys()
        return cls.daily_income(**kwargs) * mesurement_range.value
